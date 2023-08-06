import collections
import os
import threading

from django.db.backends.mysql import base as mysql
from django.db.utils import DatabaseError
from django.utils import module_loading

try:
    from django.db.backends.mysql.base import Database
except ImportError as e:
    raise ImportError('Error loading DB-API 2.0 module: %s' % e)

from sqlalchemy.pool import Pool

from .conf import DjangoPoolParams
from .pool import HashableDict


class DatabaseWrapper(mysql.DatabaseWrapper):
    db_proxy_lock = threading.Lock()
    db_proxy_by_pid = dict()

    def creator(self):
        conn_params = self.get_connection_params()
        return Database.connect(**conn_params)

    def create_db_proxy(self):
        pool_params = self.django_pool_params
        pool_class = pool_params.django_pool_class
        if isinstance(pool_class, str):
            pool_class = module_loading.import_string(pool_class)
        if not issubclass(pool_class, Pool):
            raise Exception('`pool_class` must be a subclass of sqlalchemy.pool.Pool or a import string of it')

        pool_kwargs = pool_params.get_pool_kwargs(pool_class)
        pool = pool_class(self.creator, **pool_kwargs)
        return pool

    @property
    def db_proxy(self):
        cls = self.__class__
        pid = os.getpid()
        db_proxy_by_pid = cls.db_proxy_by_pid
        db_proxy = db_proxy_by_pid.get(pid, {})
        db_proxy = db_proxy.get(self.alias)

        if db_proxy is not None:
            return db_proxy
        with cls.db_proxy_lock:
            db_proxy = db_proxy_by_pid.get(pid, None)

            if db_proxy is None:
                db_proxy_by_pid[pid] = {}
                db_proxy = db_proxy_by_pid[pid]

            db_proxy = db_proxy.get(self.alias)
            if db_proxy is not None:
                return db_proxy

            db_proxy = self.create_db_proxy()

            db_proxy_by_pid[pid].update({
                self.alias: db_proxy
            })
        if db_proxy is None:
            raise Exception('unable to initialize the database proxy')
        return db_proxy

    @property
    def django_pool_params(self):
        """
        :rtype: DjangoPoolParams
        """
        return DjangoPoolParams(self.settings_dict['POOL'])

    def get_connection_params(self):
        raw_params = super(DatabaseWrapper, self).get_connection_params()
        new_params = dict()
        for raw_key, raw_value in raw_params.items():
            new_value = raw_value
            if not isinstance(raw_value, collections.Hashable):
                if isinstance(raw_value, dict):
                    new_value = HashableDict(raw_value)
                elif isinstance(raw_value, list):
                    new_value = tuple(raw_value)
                elif isinstance(raw_value, set):
                    new_value = frozenset(raw_value)
            if not isinstance(new_value, collections.Hashable):
                raise Exception('unhashable connection parameter %s' % raw_key)
            new_params[raw_key] = new_value
        return new_params

    def get_new_connection(self, conn_params):
        return self.db_proxy.connect()

    def connect(self):

        super(DatabaseWrapper, self).connect()

        if not (
                self.connection is not None and
                self.django_pool_params.django_pre_ping
        ):
            return

        is_usable = False
        ex_message = None
        ex_default = 'unable to connect to the database'
        try:
            is_usable = self.is_usable()  # ping
        except Exception as ex:
            ex_message = str(ex)
        finally:
            if not is_usable:
                try:
                    self.errors_occurred = True
                    self.close()
                finally:
                    raise DatabaseError(ex_message or ex_default)

    def _close(self):

        conn = self.connection  # type: sqlalchemy.pool._ConnectionFairy

        if conn is None:
            return

        with self.wrap_database_errors:
            try:
                if self.in_atomic_block:
                    pool_params = self.django_pool_params
                    if pool_params.django_reset_on_return:
                        conn.rollback()
            finally:
                if self.errors_occurred:
                    conn.invalidate()
                else:
                    conn.close()
