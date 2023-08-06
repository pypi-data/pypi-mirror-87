#!/usr/bin/env python

import logging
import threading
import time

from readerwriterlock import rwlock
from typing import Callable, Dict, List, Optional, Union

LOG = logging.getLogger(__name__)

class SettingCapsule():
    __name = None
    __load = None
    __data = None
    __on_access = None
    __on_pre_load = None
    __on_post_load = None
    __on_load_error = None
    __on_reset = None
    #
    #
    def __init__(self, name: str, load: Callable,
            on_access:Optional[Callable]=None,
            on_pre_load:Optional[Callable]=None,
            on_post_load:Optional[Callable]=None,
            on_load_error:Optional[Callable]=None,
            on_reset:Optional[Callable]=None):
        assert isinstance(name, str) and name, "[name] must be a string and not empty"
        self.__name = name
        #
        assert callable(load), "[load] must be a function"
        self.__load = load
        #
        if callable(on_access):
            self.__on_access = on_access
        #
        if callable(on_pre_load):
            self.__on_pre_load = on_pre_load
        else:
            self.__on_pre_load = default_on_pre_load
        #
        if callable(on_post_load):
            self.__on_post_load = on_post_load
        else:
            self.__on_post_load = default_on_post_load
        #
        if callable(on_load_error):
            self.__on_load_error = on_load_error
        else:
            self.__on_load_error = default_on_load_error
        #
        if callable(on_reset):
            self.__on_reset = on_reset
        else:
            self.__on_reset = default_on_reset
        #
        self.__load_lock = threading.RLock()
        self.__rwhandler = rwlock.RWLockFairD()
    #
    #
    @property
    def name(self):
        return self.__name
    #
    #
    @property
    def data(self):
        with self.__rwhandler.gen_rlock():
            if callable(self.__on_access):
                self.__on_access(self.__name, time.time())
            if self.__data is None:
                with self.__load_lock:
                    if self.__data is None:
                        self.__data = self.__reload()
            return self.__data
    #
    #
    def reset(self, parameters: Optional[Union[Dict,List]] = None, lazy_load:bool=False, **kwargs):
        with self.__rwhandler.gen_wlock():
            if callable(self.__on_reset):
                self.__on_reset(self.__name, time.time())
            if lazy_load:
                self.__data = None
            else:
                args = []
                kwargs = {}
                if isinstance(parameters, dict):
                    kwargs = parameters
                elif isinstance(parameters, list):
                    args = parameters
                self.__data = self.__reload(*args, **kwargs)
        return self
    #
    #
    def __reload(self, *args, **kwargs):
        try:
            if callable(self.__on_pre_load):
                self.__on_pre_load(self.__name, time.time())
            #
            result = self.__load(*args, **kwargs)
            #
            if callable(self.__on_post_load):
                self.__on_post_load(self.__name, time.time())
            #
            return result
        except Exception as exception:
            if callable(self.__on_load_error):
                self.__on_load_error(self.__name, time.time(), exception)
            raise exception


def default_on_reset(name, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] reset the [data] to None', name)

def default_on_pre_load(name, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] invoke the load() to load the data', name)

def default_on_post_load(name, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] save result of load() to the store', name)

def default_on_load_error(name, timestamp, error):
    if LOG.isEnabledFor(logging.ERROR):
        LOG.log(logging.ERROR, 'SettingCapsule[%s] error on call to load() function', name)
