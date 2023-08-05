#!/usr/bin/env python3

import logging
import redis, os

from configator.utils.datatype import str_to_int

DEFAULT_CHANNEL_GROUP = 'configator'
DEFAULT_ENV_PREFIX = 'CONFIGATOR'

LOG = logging.getLogger(__name__)

class RedisClient(object):
    #
    def __init__(self, channel_group=None, env_prefix=None, **connection_kwargs):
        #
        self.CHANNEL_GROUP = channel_group if isinstance(channel_group, str) else DEFAULT_CHANNEL_GROUP
        #
        self.ENV_PREFIX = env_prefix if isinstance(env_prefix, str) else DEFAULT_ENV_PREFIX
        env_prefix_lodash = self.ENV_PREFIX + '_'
        #
        self.__connection_kwargs = connection_kwargs
        #
        host = os.getenv(env_prefix_lodash + 'REDIS_HOST')
        if host:
            self.__connection_kwargs['host'] = host
        #
        if not self.__connection_kwargs.get('host'):
            self.__connection_kwargs['host'] = 'localhost'
        #
        port = os.getenv(env_prefix_lodash + 'REDIS_PORT')
        if port:
            port, err = str_to_int(port)
            if err is None and port > 0:
                self.__connection_kwargs['port'] = port
        if not self.__connection_kwargs.get('port'):
            self.__connection_kwargs['port'] = 6379
        #
        db = os.getenv(env_prefix_lodash + 'REDIS_DB')
        if db:
            db, err = str_to_int(db)
            if err is None and type(db) == type(0):
                self.__connection_kwargs['db'] = db
        if 'db' not in self.__connection_kwargs:
            self.__connection_kwargs['db'] = 0
        #
        username = os.getenv(env_prefix_lodash + 'REDIS_USERNAME')
        if username:
            self.__connection_kwargs['username'] = username
        #
        password = os.getenv(env_prefix_lodash + 'REDIS_PASSWORD')
        if password:
            self.__connection_kwargs['password'] = password
        #
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "redis connection kwargs: %s", str(self.__connection_kwargs))
    #
    ##
    def connect(self, ping:bool=False):
        waiting = True
        while waiting:
            try:
                connection = self._connection
                if ping:
                    connection.ping()
                waiting = False
                return connection
            except redis.ConnectionError:
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.log(logging.DEBUG, "redis.ConnectionError")
                pass
    #
    #
    def reconnect(self):
        self._destroy()
        return self.connect()
    #
    #
    __r = None
    #
    #
    @property
    def _connection(self):
        if self.__r is None:
            pool = redis.ConnectionPool(**self.__connection_kwargs)
            self.__r = redis.Redis(connection_pool=pool)
        return self.__r
    #
    #
    def _destroy(self):
        if self.__r is not None:
            self.__r.close()
            self.__r = None
