import copy
import json
import multiprocessing
import operator as ops
import os
import platform
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime

import numpy as np
import psutil
import sqlalchemy
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy.orm
import sqlalchemy.sql as sa
import sqlalchemy_utils.functions as sql_utils
import toolz as t
import wrapt
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.migration import MigrationContext
from memoized_property import memoized_property
from sqlalchemy.schema import CreateSchema

from . import _commonstore as cs, models as db, serializers as s, utils
from ._commonstore import find_first
from .hashing import hash, value_repr


def _host_info():
    return {
        'machine': platform.machine(),
        'nodename': platform.node(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'cpu_count': multiprocessing.cpu_count(),
        'release': platform.release(),
        'system': platform.system(),
        'version': platform.version(),
    }


def _process_info():
    pid = os.getpid()
    p = psutil.Process(pid)
    return {
        'cmdline': p.cmdline(),
        'cwd': p.cwd(),
        'exe': p.exe(),
        'name': p.name(),
        'num_fds': p.num_fds(),
        'num_threads': p.num_threads(),
    }


def _alembic_config(connection):
    root = t.pipe(__file__, os.path.realpath, os.path.dirname)
    config = AlembicConfig(os.path.join(root, 'alembic.ini'))
    config.set_main_option('script_location', os.path.join(root, 'migrations'))
    config.attributes['connection'] = connection
    return config


def _create_db_if_needed(db_conn_str):
    if not sql_utils.database_exists(db_conn_str):
        sql_utils.create_database(db_conn_str)


class Config:

    _current = None

    @classmethod
    def current(cls):
        return cls._current

    @classmethod
    def set_current(cls, registry):
        cls._current = registry

    def __init__(
        self,
        blobstores,
        repos,
        default_repo,
        run_info_fn=None,
        use_cache=True,
        read_only=False,
        check_mutations=False,
    ):
        self.blobstores = blobstores
        self.repos = repos
        self.set_default_repo(default_repo)
        self._run_info = None
        self.run_info_fn = run_info_fn or t.identity
        self.use_cache = use_cache
        self.read_only = read_only
        self.check_mutations = check_mutations

    def set_default_repo(self, repo):
        if isinstance(repo, str):
            if repo not in self.repos:
                raise Exception("There is no registered repo named '{}'.".format(repo))
            self.default_repo = self.repos[repo]
        else:
            self.default_repo = repo

    def set_run_info_fn(self, fn):
        self.run_info_fn = fn or t.identity
        self._run_info = None

    def run_info(self):
        if self._run_info is None:
            run_info = self.run_info_fn(
                {
                    'host': _host_info(),
                    'process': _process_info(),
                    'created_at': datetime.utcnow(),
                }
            )
            run_info['id'] = hash(run_info)
            self._run_info = run_info
        return self._run_info


Config.set_current(Config({}, {}, None))


def current_config():
    return Config.current()


def set_default_repo(repo_or_name):
    current_config().set_default_repo(repo_or_name)


def get_default_repo():
    return current_config().default_repo


def set_run_info_fn(fn):
    """
    This hook allows you to provide a function that will be called once with a process's
    `run_info` default dictionary. The provided function can then update this dictionary
    with other useful information you wish to track, such as git ref or build server id.
    """
    current_config().set_run_info_fn(fn)


def get_use_cache():
    return current_config().use_cache


def set_use_cache(setting):
    current_config().use_cache = setting


def get_read_only():
    return current_config().read_only


def set_read_only(setting):
    current_config().read_only = setting


def get_check_mutations():
    return current_config().check_mutations


def set_check_mutations(setting):
    current_config().check_mutations = setting


def get_repo_by_name(repo_name):
    return current_config().repos[repo_name]


@contextmanager
def using_repo(repo_or_name):
    prev_repo = get_default_repo()
    set_default_repo(repo_or_name)
    try:
        yield
    finally:
        set_default_repo(prev_repo)


def load_artifact(artifact_id):
    """Loads and returns the ``Artifact`` with the ``artifact_id`` from the default repo.

    Parameters
    ----------
    artifact_id : string

    See Also
    --------
    load_proxy
    """
    return get_default_repo().get_by_id(artifact_id)


def load_proxy(artifact_id):
    """Loads and returns the ``ArtifactProxy`` with the ``artifact_id`` from the default repo.

    Parameters
    ----------
    artifact_id : string

    See Also
    --------
    load_artifact
    """
    return get_default_repo().get_by_id(artifact_id).proxy()


def load_set_by_id(set_id):
    """Loads and returns the ``ArtifactSet`` with the ``set_id`` from the default repo.

    Parameters
    ----------
    set_id : string

    See Also
    --------
    load_set_by_name
    """
    return get_default_repo().get_set_by_id(set_id)


def load_set_by_labels(labels):
    """Loads and returns the ``ArtifactSet`` with the ``labels`` from the default repo.

    Parameters
    ----------
    labels : string or dictionary

    See Also
    --------
    load_set_by_id
    load_set_by_labels
    """
    return get_default_repo().get_set_by_labels(labels)


def load_set_by_name(set_name):
    """Loads and returns the ``ArtifactSet`` with the ``set_name`` from the default repo.

    Parameters
    ----------
    set_name : string

    See Also
    --------
    load_set_by_id
    load_set_by_labels
    """
    return get_default_repo().get_set_by_labels({'name': set_name})


def _check_labels_name(labels):
    if isinstance(labels, str):
        return {'name': labels}
    return labels


def create_set(artifact_ids, labels=None):
    labels = _check_labels_name(labels)
    return ArtifactSet(artifact_ids, labels).put()


def label_set(artifact_set_or_id, labels):
    repo = get_default_repo()
    if isinstance(artifact_set_or_id, ArtifactSet):
        artifact_set = artifact_set_or_id
    else:
        artifact_set = repo.get_set_by_id(artifact_set_or_id)

    return artifact_set.relabel(labels).put(repo)


def transform_value(proxy_artifact, transformer_fn):
    """
    Transforms the underlying value of the ``proxy_artifact`` with
    the provided ``transformer_fn``. A new ``ArtifactProxy`` is returned
    with the transformed value but with the original artifact.

    The motivation behind this function is to allow archived files
    to be loaded into memory and passed around while preserving
    the provenance of the artifact. It could be used in any other
    situation where you want a different representation of an
    artifact value while allowing the provenance to be tracked.

    Care should be taken when using this function however because
    it will prevent you from reproducing exact artifacts from
    the lineage since this transformer_fn will not be tracked.
    """
    transformed = copy.copy(proxy_artifact)
    transformed.__wrapped__ = transformer_fn(transformed)
    return transformed


class Proxy:

    def value_repr(self):
        return value_repr(self.artifact.value)

    def transform_value(self, transformer_fn):
        return transform_value(self, transformer_fn)

    def __next__(self):
        # note, that every proxy is always identified as an
        # iterable anyways: https://github.com/GrahamDumpleton/wrapt/issues/93
        # this just forwards the method to the wrapped version since
        # it wasn't doing that for somereason
        return next(self.__wrapped__)


class ArtifactProxy(wrapt.ObjectProxy, Proxy):

    def __init__(self, value, artifact):
        super(ArtifactProxy, self).__init__(value)
        self._self_artifact = artifact

    @property
    def artifact(self):
        return self._self_artifact

    def __repr__(self):
        return '<provenance.ArtifactProxy({}) {} >'.format(self.artifact.id, repr(self.__wrapped__))

    def __reduce__(self):
        return (load_proxy, (self.artifact.id,))

    def __reduce_ex__(self, protocol_version):
        return self.__reduce__()

    def __copy__(self):
        return ArtifactProxy(copy.copy(self.__wrapped__), self._self_artifact)

    def __deepcopy__(self, memo=None):
        return ArtifactProxy(copy.deepcopy(self.__wrapped__, memo), self._self_artifact)


class CallableArtifactProxy(wrapt.CallableObjectProxy, Proxy):

    def __init__(self, value, artifact):
        super(CallableArtifactProxy, self).__init__(value)
        self._self_artifact = artifact

    @property
    def artifact(self):
        return self._self_artifact

    def __repr__(self):
        return '<provenance.ArtifactProxy({}) {} >'.format(self.artifact.id, repr(self.__wrapped__))

    def __reduce__(self):
        return (load_proxy, (self.artifact.id,))

    def __reduce_ex__(self, protocol_version):
        return self.__reduce__()

    def __copy__(self):
        return CallableArtifactProxy(copy.copy(self.__wrapped__), self._self_artifact)

    def __deepcopy__(self, memo=None):
        return CallableArtifactProxy(copy.deepcopy(self.__wrapped__, memo), self._self_artifact)


def artifact_proxy(value, artifact):
    if callable(value):
        return CallableArtifactProxy(value, artifact)
    return ArtifactProxy(value, artifact)


def is_proxy(obj):
    return type(obj) == ArtifactProxy or type(obj) == CallableArtifactProxy


class Artifact:

    def __init__(self, repo, props, value='not provided', inputs=None, run_info=None):
        assert 'id' in props, "props must contain 'id'"
        assert 'value_id' in props, "props must contain 'value_id'"
        self.__dict__ = props.copy()
        self.repo = repo

        if not isinstance(value, str) or value != 'not provided':
            self._value = value
        if inputs is not None:
            self._inputs = inputs
        if run_info is not None:
            self._run_info = run_info

    @memoized_property
    def value(self):
        return self.repo.get_value(self)

    @memoized_property
    def inputs(self):
        return self.repo.get_inputs(self)

    @memoized_property
    def run_info(self):
        return self.repo.run_info(self.id)

    @property
    def tags(self):
        if self.custom_fields:
            return self.custom_fields.get('tags', None)

    def proxy(self):
        if self.composite:
            value = lazy_dict(t.valmap(lambda a: lambda: a.proxy(), self.value))
        else:
            value = self.value
        return artifact_proxy(value, self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(('--artifact--', self.id))

    def __repr__(self):
        return '<provenance.Artifact({})>'.format(self.id)

    def __reduce__(self):
        return (load_artifact, (self.id,))


@value_repr.register(Artifact)
def _(artifact):
    return ('artifact', artifact.id)


def _artifact_id(artifact_or_id):
    if isinstance(artifact_or_id, str):
        return artifact_or_id
    if hasattr(artifact_or_id, 'id'):
        return artifact_or_id.id
    if hasattr(artifact_or_id, 'artifact'):
        return artifact_or_id.artifact.id
    raise Exception('Unable to coerce into an artifact id: {}'.format(artifact_or_id))


def _artifact_from_record(repo, record):
    if isinstance(record, Artifact):
        return record
    return Artifact(
        repo,
        t.dissoc(record._asdict(), 'value', 'inputs', 'run_info'),
        value=record.value,
        inputs=record.inputs,
        run_info=record.run_info,
    )


class ArtifactRepository:

    def __init__(self, read=True, write=True, read_through_write=True, delete=False):
        self._read = read
        self._write = write
        self._read_through_write = read_through_write
        self._delete = delete

    def __getitem__(self, artifact_id):
        return self.get_by_id(artifact_id)

    def batch_get_by_id(self, artifact_ids):
        cs.ensure_read(self)
        return [self.get_by_id(id) for id in artifact_ids]


class MemoryRepo(ArtifactRepository):

    def __init__(
        self,
        artifacts=None,
        read=True,
        write=True,
        read_through_write=True,
        delete=True,
    ):
        super(MemoryRepo, self).__init__(
            read=read, write=write, read_through_write=read_through_write, delete=delete
        )
        self.artifacts = artifacts if artifacts else []
        self.sets = []

    def __contains__(self, artifact_or_id):
        cs.ensure_contains(self)
        artifact_id = _artifact_id(artifact_or_id)
        if find_first(lambda a: a.id == artifact_id, self.artifacts):
            return True
        else:
            return False

    def put(self, record, read_through=False):
        artifact_id = _artifact_id(record)
        cs.ensure_put(self, artifact_id, read_through)
        self.artifacts.append(record)
        return _artifact_from_record(self, record)

    def get_by_id(self, artifact_id):
        cs.ensure_read(self)
        record = find_first(lambda a: a.id == artifact_id, self.artifacts)
        if record:
            return _artifact_from_record(self, record)
        else:
            raise KeyError(artifact_id, self)

    def get_by_value_id(self, value_id):
        cs.ensure_read(self)
        record = find_first(lambda a: a.value_id == value_id, self.artifacts)
        if record:
            return _artifact_from_record(self, record)
        else:
            raise KeyError(value_id, self)

    def get_value(self, artifact, composite=False):
        cs.ensure_read(self)
        return find_first(lambda a: a.id == artifact.id, self.artifacts).value

    def get_inputs(self, artifact):
        cs.ensure_read(self)
        return find_first(lambda a: a.id == artifact.id, self.artifacts).inputs

    def delete(self, artifact_or_id):
        artifact_id = _artifact_id(artifact_or_id)
        cs.ensure_delete(self)
        new_artifacts = list(t.filter(lambda a: a.id != artifact_id, self.artifacts))
        if len(new_artifacts) == len(self.artifacts):
            raise KeyError(artifact_id, self)
        else:
            self.artifacts = new_artifacts

    def contains_set(self, set_id):
        art_set = find_first(lambda s: s.id == set_id, self.sets)
        return True if art_set else False

    def get_set_by_id(self, set_id):
        cs.ensure_read(self)
        art_set = find_first(lambda s: s.id == set_id, self.sets)
        if not art_set:
            raise KeyError(self, set_id)

        return art_set

    def get_set_by_labels(self, labels):
        cs.ensure_read(self)
        labels = _check_labels_name(labels)
        versions = [s for s in self.sets if s.labels == labels]
        if not versions:
            raise KeyError(labels, self)
        return sorted(versions, key=lambda s: s.created_at, reverse=True)[0]

    def put_set(self, artifact_set, read_through=False):
        cs.ensure_write(self, 'put_set')
        self.sets.append(artifact_set)
        return artifact_set

    def delete_set(self, set_id):
        cs.ensure_delete(self, check_contains=False)
        prev_count = len(self.sets)
        self.sets = [s for s in self.sets if s.id != set_id]
        if len(self.sets) == prev_count:
            raise KeyError(set_id, self)


def _transform(val):
    if isinstance(val, (Artifact)):
        return {'id': val.id, 'type': 'Artifact', 'name': val.name}
    elif type(val) in {ArtifactProxy, CallableArtifactProxy}:
        return {
            'id': val.artifact.id,
            'type': 'ArtifactProxy',
            'name': val.artifact.name,
        }
    else:
        return val


def _inputs_json(inputs):
    expanded = t.valmap(_transform, inputs['kargs'])
    expanded['__varargs'] = list(t.map(_transform, inputs['varargs']))

    return expanded


def _ping_postgres(conn, branch):
    """
    Code taken from example here: http://docs.sqlalchemy.org/en/latest/core/pooling.html#dealing-with-disconnects
    """
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = conn.should_close_with_result
    conn.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        conn.scalar(sqlalchemy.select([1]))
    except sqlalchemy.exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            conn.scalar(sqlalchemy.select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        conn.should_close_with_result = save_should_close_with_result


def _record_pid(dbapi_connection, connection_record):
    connection_record.info['pid'] = os.getpid()


def _check_pid(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise sqlalchemy.exc.DisconnectionError(
            'Connection record belongs to pid %s, '
            'attempting to check out in pid %s' % (connection_record.info['pid'], pid)
        )


@t.curry
def _set_search_path(schema, dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    cursor.execute('SET search_path TO {};'.format(schema))
    dbapi_connection.commit()
    cursor.close()


def _db_engine(conn_string, schema, persistent_connections=True):
    poolclass = None if persistent_connections else sqlalchemy.pool.NullPool
    db_engine = sqlalchemy.create_engine(
        conn_string, json_serializer=Encoder().encode, poolclass=poolclass
    )
    sqlalchemy.event.listens_for(db_engine, 'engine_connect')(_ping_postgres)
    sqlalchemy.event.listens_for(db_engine, 'connect')(_record_pid)
    sqlalchemy.event.listens_for(db_engine, 'checkout')(_check_pid)
    if schema:
        sqlalchemy.event.listens_for(db_engine, 'checkout')(_set_search_path(schema))
    return db_engine


def _insert_set_members_sql(artifact_set):
    pairs = [(artifact_set.id, id) for id in artifact_set.artifact_ids]
    return """
INSERT INTO artifact_set_members (set_id, artifact_id)
VALUES
{}
ON CONFLICT DO NOTHING
    """.strip().format(',\n'.join(t.map(str, pairs)))


class Encoder(json.JSONEncoder):

    def default(self, val):
        if isinstance(val, (datetime)):
            return str(val)
        elif isinstance(val, np.integer):
            return int(val)
        elif isinstance(val, np.floating):
            return float(val)
        elif isinstance(val, np.bool_):
            return bool(val)
        elif isinstance(val, np.ndarray):
            return val.tolist()
        elif is_proxy(val) or isinstance(val, Artifact):
            return repr(val)
        elif callable(val):
            try:
                return utils.fn_info(val)
            except:
                pass
        else:
            try:
                return super(Encoder, self).default(val)
            except Exception:
                print('Could not serialize type: {}'.format(type(val)))
                return str(type(val))


class PostgresRepo(ArtifactRepository):
    # TODO: add the upgrade_db param back once upgrade is working
    # upgrade_db=True
    def __init__(
        self,
        db,
        store,
        read=True,
        write=True,
        read_through_write=True,
        delete=True,
        create_db=False,
        schema=None,
        create_schema=True,
        persistent_connections=True,
    ):
        upgrade_db = False
        super(PostgresRepo, self).__init__(
            read=read, write=write, read_through_write=read_through_write, delete=delete
        )

        if not isinstance(db, str) and schema is not None:
            raise ValueError('You can only provide a schema with a DB url.')

        init_db = False
        if create_db and isinstance(db, str):
            _create_db_if_needed(db)
            init_db = True
            upgrade_db = False

        self._run = None
        if isinstance(db, str):
            if create_db:
                init_db = True

            self._db_engine = _db_engine(db, schema, persistent_connections)
            self._sessionmaker = sqlalchemy.orm.sessionmaker(bind=self._db_engine)
        else:
            self._session = db

        if create_schema and schema is not None:
            with self.session() as session:
                q = sa.exists(
                    sa.select([sa.text('schema_name')]).select_from(
                        sa.text('information_schema.schemata')
                    ).where(sa.text('schema_name = :schema').bindparams(schema=schema))
                )
                if not session.query(q).scalar():
                    session.execute(CreateSchema(schema))
                    session.commit()
                    init_db = True
                    upgrade_db = False

        if init_db:
            self._db_init()

        if upgrade_db:
            self._db_upgrade()

        self.blobstore = store

    @contextmanager
    def session(self):
        if hasattr(self, '_session'):
            close = False
        else:
            self._session = self._sessionmaker()
            close = True

        try:
            yield self._session
        except:
            self._session.rollback()
            raise
        finally:
            if close:
                self._session.close()
                del self._session

    def __contains__(self, artifact_or_id):
        cs.ensure_contains(self)
        artifact_id = _artifact_id(artifact_or_id)
        with self.session() as s:
            return (s.query(db.Artifact).filter(db.Artifact.id == artifact_id).count() > 0)

    def _upsert_run(self, session, info):
        sql = (
            pg.insert(db.Run).values(
                id=info['id'],
                info=info,
                hostname=info['host']['nodename'],
                created_at=info['created_at'],
            ).on_conflict_do_nothing(index_elements=['id'])
        )

        session.execute(sql)

        return db.Run(info)

    @property
    def db_revision(self):
        with self.session() as session:
            context = MigrationContext.configure(session.connection())
            return context.get_current_revision()

    def _db_init(self):
        db.Base.metadata.create_all(self._db_engine)
        with self.session() as session:
            conn = session.connection()
            # the below doesn't work for some reason
            # db.Base.metadata.create_all(conn)
            cfg = _alembic_config(conn)
            command.stamp(cfg, 'head')

    def _db_upgrade(self):
        with self.session() as session:
            conn = session.connection()
            cfg = _alembic_config(conn)
            command.upgrade(cfg, 'head')

    def put(self, artifact_record, read_through=False):
        with self.session() as session:
            cs.ensure_put(self, artifact_record.id, read_through)
            self.blobstore.put(
                artifact_record.id, artifact_record.inputs, s.DEFAULT_INPUT_SERIALIZER
            )
            self.blobstore.put(
                artifact_record.value_id,
                artifact_record.value,
                s.serializer(artifact_record),
            )

            inputs_json = _inputs_json(artifact_record.inputs)
            run = self._upsert_run(session, artifact_record.run_info)
            db_artifact = db.Artifact(artifact_record, inputs_json, run)

            session.add(db_artifact)
            session.commit()

            return _artifact_from_record(self, artifact_record)

    def get_by_id(self, artifact_id):
        cs.ensure_read(self)
        with self.session() as session:
            result = (session.query(db.Artifact).filter(db.Artifact.id == artifact_id).first())

        if result:
            return Artifact(self, result.props)
        else:
            raise KeyError(artifact_id, self)

    def batch_get_by_id(self, artifact_ids):
        cs.ensure_read(self)
        with self.session() as session:
            results = (session.query(db.Artifact).filter(db.Artifact.id.in_(artifact_ids)).all())

        if len(results) == len(artifact_ids):
            return [Artifact(self, result.props) for result in results]
        else:
            ids = set(artifact_ids)
            found = set([a.id for a in results])
            missing = ids - found
            raise KeyError(missing, self)

    def get_by_value_id(self, value_id):
        cs.ensure_read(self)
        with self.session() as session:
            result = (session.query(db.Artifact).filter(db.Artifact.value_id == value_id).first())

        if result:
            return Artifact(self, result.props)
        else:
            raise KeyError(value_id, self)

    def get_value(self, artifact):
        cs.ensure_read(self)
        return self.blobstore.get(artifact.value_id, s.serializer(artifact))

    def get_inputs(self, artifact):
        cs.ensure_read(self)
        return self.blobstore.get(artifact.id, s.DEFAULT_INPUT_SERIALIZER)

    def delete(self, artifact_or_id):
        with self.session() as session:
            cs.ensure_delete(self)
            artifact = self.get_by_id(artifact_or_id)
            (session.query(db.Artifact).filter(db.Artifact.id == artifact.id).delete())
            self.blobstore.delete(artifact.id)
            self.blobstore.delete(artifact.value_id)
            session.commit()

    def put_set(self, artifact_set, read_through=False):
        with self.session() as session:
            cs.ensure_write(self, 'put_set')
            db_set = db.ArtifactSet(artifact_set)
            session.add(db_set)
            session.execute(_insert_set_members_sql(artifact_set))
            session.commit()

            return artifact_set

    def _db_to_mem_set(self, result):
        with self.session() as session:
            members = (
                session.query(db.ArtifactSetMember
                             ).filter(db.ArtifactSetMember.set_id == result.set_id).all()
            )
            props = result.props
            props['artifact_ids'] = [m.artifact_id for m in members]
            return ArtifactSet(**props)

    def contains_set(self, set_id):
        with self.session() as session:
            if (session.query(db.ArtifactSet).filter(db.ArtifactSet.set_id == set_id).count() > 0):
                return True
            else:
                return False

    def get_set_by_id(self, set_id):
        cs.ensure_read(self)
        with self.session() as session:
            result = (session.query(db.ArtifactSet).filter(db.ArtifactSet.set_id == set_id).first())

        if result:
            return self._db_to_mem_set(result)
        else:
            raise KeyError(set_id, self)

    def get_set_by_labels(self, labels):
        cs.ensure_read(self)
        labels = _check_labels_name(labels)

        with self.session() as session:
            result = (
                session.query(db.ArtifactSet).filter(db.ArtifactSet.labels == labels
                                                    ).order_by(db.ArtifactSet.created_at.desc()
                                                              ).first()
            )

        if result:
            return self._db_to_mem_set(result)
        else:
            raise KeyError(labels, self)

    def delete_set(self, set_id):
        cs.ensure_delete(self, check_contains=False)
        with self.session() as session:
            num_deleted = (
                session.query(db.ArtifactSet).filter(db.ArtifactSet.set_id == set_id).delete()
            )
            (
                session.query(db.ArtifactSetMember).filter(db.ArtifactSetMember.set_id == set_id
                                                          ).delete()
            )

        if num_deleted == 0:
            raise KeyError(set_id, self)

    def run_info(self, artifact_id):
        with self.session() as session:
            result = (
                session.query(db.Run).filter(db.Run.id == db.Artifact.run_id
                                            ).filter(db.Artifact.id == artifact_id).first()
            )
            return result.info_with_datetimes

    def _filename(self, artifact_id):
        return self.blobstore._filename(artifact_id)


DbRepo = PostgresRepo


def _put_only_value(store, id, value, **kargs):
    return store.put(value, **kargs)


def _put_set(store, id, value, **kargs):
    return store.put_set(value, **kargs)


def _contains_set(store, id):
    return store.contains_set(id)


def _delete_set(store, id):
    return store.delete_set(id)


class ChainedRepo(ArtifactRepository):

    def __init__(self, repos):
        self.stores = repos

    def __contains__(self, id):
        return cs.chained_contains(self, id)

    def put(self, record):
        return cs.chained_put(self, record.id, record, put=_put_only_value)

    def put_set(self, artifact_set, read_through=False):
        return cs.chained_put(self, None, artifact_set, contains=_contains_set, put=_put_set)

    def get_by_id(self, artifact_id):

        def get(store, id):
            return store.get_by_id(id)

        return cs.chained_get(self, get, artifact_id, put=_put_only_value)

    def contains_set(self, id):
        return cs.chained_contains(self, id, contains=_contains_set)

    def get_set_by_id(self, set_id):

        def get(store, id):
            return store.get_set_by_id(id)

        return cs.chained_get(self, get, set_id, put=_put_set)

    def get_set_by_labels(self, set_name):

        def get(store, name):
            return store.get_set_by_labels(name)

        return cs.chained_get(self, get, set_name, put=_put_set)

    def delete_set(self, id):
        return cs.chained_delete(self, id, contains=_contains_set, delete=_delete_set)

    def get_by_value_id(self, value_id):

        def get(store, id):
            return store.get_by_value_id(id)

        return cs.chained_get(self, get, value_id, put=_put_only_value)

    def get_value(self, artifact):
        for store in self.stores:
            try:
                return store.get_value(artifact)
            except KeyError:
                pass
        raise KeyError(artifact, self)

    def delete(self, id):
        return cs.chained_delete(self, id)

    def _filename(self, id):
        return cs.chained_filename(self, id)


### ArtifactSet logic


def _set_op(operator, *sets, labels=None):
    new_ids = t.reduce(operator, t.map(lambda s: s.artifact_ids, sets))
    return ArtifactSet(new_ids, labels)


set_union = t.partial(_set_op, ops.or_)
set_difference = t.partial(_set_op, ops.sub)
set_intersection = t.partial(_set_op, ops.and_)

artifact_set_properties = ['id', 'artifact_ids', 'created_at', 'labels']


class ArtifactSet(namedtuple('ArtifactSet', artifact_set_properties)):

    def __new__(cls, artifact_ids, labels=None, created_at=None, id=None):
        artifact_ids = t.map(_artifact_id, artifact_ids)
        labels = _check_labels_name(labels)
        ids = frozenset(artifact_ids)
        if id:
            set_id = id
        else:
            set_id = hash(ids)
        created_at = created_at if created_at else datetime.utcnow()
        return super(ArtifactSet, cls).__new__(cls, set_id, ids, created_at, labels)

    @property
    def name(self):
        if self.labels is not None:
            return self.labels.get('name')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def artifacts_named(self, artifact_name):
        pass
        # return all artifacts found wrapped in list

    def add(self, artifact_or_id, labels=None):
        artifact_id = _artifact_id(artifact_or_id)
        return ArtifactSet(self.artifact_ids | {artifact_id}, labels)

    def remove(self, artifact_or_id, labels=None):
        artifact_id = _artifact_id(artifact_or_id)
        return ArtifactSet(self.artifact_ids - {artifact_id}, labels)

    def union(self, *sets, labels=None):
        return set_union(self, *sets, labels=labels)

    def __or__(self, other_set):
        return set_union(self, other_set)

    def difference(self, *sets, labels=None, repo=None):
        return set_difference(self, *sets, labels=labels)

    def __sub__(self, other_set):
        return set_difference(self, other_set)

    def intersection(self, *sets, labels=None):
        return set_intersection(self, *sets, labels=labels)

    def __and__(self, other_set):
        return set_intersection(self, other_set)

    def relabel(self, labels):
        labels = _check_labels_name(labels)
        return self._replace(labels=labels)

    def rename(self, name):
        return self.relabel({'name': name})

    def put(self, repo=None):
        repo = repo if repo else get_default_repo()
        return repo.put_set(self)

    def proxy_dict(self, group_artifacts_of_same_name=False):
        """
        Returns a lazy_proxy_dict of the artifacts that are contained in this set.

        See the documentation for lazy_proxy_dict for more information.
        """
        return lazy_proxy_dict(self.artifact_ids, group_artifacts_of_same_name)


def save_artifact(f, artifact_ids):

    def wrapped(*args, **kargs):
        artifact = f(*args, **kargs)
        artifact_ids.add(artifact.id)
        return artifact

    return wrapped


class RepoSpy(wrapt.ObjectProxy):

    def __init__(self, repo):
        super(RepoSpy, self).__init__(repo)
        self.artifact_ids = set()
        self.put = save_artifact(repo.put, self.artifact_ids)
        self.get_by_id = save_artifact(repo.get_by_id, self.artifact_ids)
        self.get_by_value_id = save_artifact(repo.get_by_value_id, self.artifact_ids)


@contextmanager
def capture_set(labels=None, initial_set=None):
    if initial_set:
        initial = set(t.map(_artifact_id, initial_set))
    else:
        initial = set()

    repo = get_default_repo()
    spy = RepoSpy(repo)
    with using_repo(spy):
        result = []
        yield result
        artifact_ids = spy.artifact_ids | initial
    result.append(ArtifactSet(artifact_ids, labels=labels).put(repo))


def coerce_to_artifact(artifact_or_id, repo=None):
    repo = repo if repo else get_default_repo()
    if isinstance(artifact_or_id, str):
        return repo.get_by_id(artifact_or_id)
    if isinstance(artifact_or_id, Artifact):
        return artifact_or_id
    if is_proxy(artifact_or_id):
        return artifact_or_id.artifact
    raise ValueError('Was unable to coerce object into an Artifact: {}'.format(artifact_or_id))


def coerce_to_artifacts(artifact_or_ids, repo=None):
    repo = repo if repo else get_default_repo()
    # TODO: bring this back when/if batch_get_by_id is added to chained repo
    # if all(isinstance(a, str) for a in artifact_or_ids):
    #     return repo.batch_get_by_id(artifact_or_ids)
    return [coerce_to_artifact(a, repo) for a in artifact_or_ids]


class lazy_dict:

    def __init__(self, thunks):
        self.thunks = thunks
        self.realized = {}

    def __getstate__(self):
        return self.thunks

    def __setstate__(self, thunks):
        self.__init__(thunks)

    def __getitem__(self, key):
        if key in self.thunks:
            if key not in self.realized:
                self.realized[key] = self.thunks[key]()
            return self.realized[key]
        else:
            raise KeyError(key, self)

    def __setitem__(self, key, value):
        self.thunks[key] = lambda: value
        self.realized[key] = value

    def __delitem__(self, key):
        if key in self.thunks:
            del self.thunks[key]
            if key in self.realized:
                del self.realized[key]
        else:
            KeyError(key, self)

    def __contains__(self, key):
        return key in self.thunks

    def items(self):
        return ((key, self[key]) for key in self.thunks.keys())

    def keys(self):
        return self.thunks.keys()

    def values(self):
        return (self[key] for key in self.thunks.keys())

    def __repr__(self):
        return 'lazy_dict({})'.format(
            t.merge(t.valmap(lambda _: '...', self.thunks), self.realized)
        )


def lazy_proxy_dict(artifacts_or_ids, group_artifacts_of_same_name=False):
    """
    Takes a list of artifacts or artifact ids and returns a dictionary whose
    keys are the names of the artifacts. The values will be lazily loaded into
    proxies as requested.

    Parameters
    ----------
    artifacts_or_ids : collection of artifacts or artifact ids (strings)

    group_artifacts_of_same_name: bool (default: False)
    If set to True then artifacts of the same name will be grouped together in
    one list. When set to False an exception will be raised
    """
    if isinstance(artifacts_or_ids, dict):
        artifacts = t.valmap(coerce_to_artifact, artifacts_or_ids)
        lambdas = {name: (lambda a: lambda: a.proxy())(a) for name, a in artifacts.items()}
        return lazy_dict(lambdas)

    # else we have a collection
    artifacts = coerce_to_artifacts(artifacts_or_ids)
    by_name = t.groupby(lambda a: a.name, artifacts)
    singles = t.valfilter(lambda l: len(l) == 1, by_name)
    multi = t.valfilter(lambda l: len(l) > 1, by_name)

    lambdas = {name: (lambda a: lambda: a.proxy())(a[0]) for name, a in singles.items()}

    if group_artifacts_of_same_name and len(multi) > 0:
        lambdas = t.merge(
            lambdas,
            {
                name: (lambda artifacts: (lambda: [a.proxy() for a in artifacts]))(artifacts)
                for name, artifacts in multi.items()
            },
        )

    if not group_artifacts_of_same_name and len(multi) > 0:
        raise ValueError(
            """Only artifacts with distinct names can be used in a lazy_proxy_dict.
Offending names: {}
Use the option `group_artifacts_of_same_name=True` if you want a list of proxies to be returned under the respective key.
        """.format({n: len(a) for n, a in multi.items()})
        )

    return lazy_dict(lambdas)
