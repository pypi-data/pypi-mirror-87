#!/usr/bin/env python

import logging
import threading
import time

from readerwriterlock import rwlock
from typing import Callable, Dict, List, Optional, Union

LOG = logging.getLogger(__name__)

class SettingCapsule():
    __label = None
    __payload = None
    __loader = None
    __on_access = None
    __on_pre_load = None
    __on_post_load = None
    __on_load_error = None
    __on_refresh = None
    #
    #
    def __init__(self, label: str, loader: Callable,
            on_access:Optional[Callable]=None,
            on_pre_load:Optional[Callable]=None,
            on_post_load:Optional[Callable]=None,
            on_load_error:Optional[Callable]=None,
            on_refresh:Optional[Callable]=None):
        assert isinstance(label, str) and label, "[label] must be a string and not empty"
        self.__label = label
        #
        assert callable(loader), "[loader] must be a function"
        self.__loader = loader
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
        if callable(on_refresh):
            self.__on_refresh = on_refresh
        else:
            self.__on_refresh = default_on_refresh
        #
        self.__load_lock = threading.RLock()
        self.__rwhandler = rwlock.RWLockFairD()
    #
    #
    @property
    def name(self):
        return self.label
    #
    @property
    def data(self):
        return self.content
    #
    def reset(self, parameters: Optional[Union[Dict,List]] = None, lazy_load:bool=False, **kwargs):
        return self.refresh(parameters, lazy_load=lazy_load, **kwargs)
    #
    #
    @property
    def label(self):
        return self.__label
    #
    @property
    def content(self):
        return self.payload()
    #
    def payload(self):
        with self.__rwhandler.gen_rlock():
            if callable(self.__on_access):
                self.__on_access(self.__label, time.time())
            if self.__payload is None:
                with self.__load_lock:
                    if self.__payload is None:
                        self.__payload = self.__reload()
            return self.__payload
    #
    def refresh(self, parameters: Optional[Union[Dict,List]] = None, lazy_load:bool=False, **kwargs):
        with self.__rwhandler.gen_wlock():
            if callable(self.__on_refresh):
                self.__on_refresh(self.__label, time.time())
            if lazy_load:
                self.__payload = None
            else:
                args = []
                kwargs = {}
                if isinstance(parameters, dict):
                    kwargs = parameters
                elif isinstance(parameters, list):
                    args = parameters
                self.__payload = self.__reload(*args, **kwargs)
        return self
    #
    #
    def __reload(self, *args, **kwargs):
        try:
            if callable(self.__on_pre_load):
                self.__on_pre_load(self.__label, time.time())
            #
            result = self.__loader(*args, **kwargs, __content__=self.__payload)
            #
            if callable(self.__on_post_load):
                self.__on_post_load(self.__label, time.time())
            #
            return result
        except Exception as exception:
            if callable(self.__on_load_error):
                self.__on_load_error(self.__label, time.time(), exception)
            raise exception


def default_on_refresh(label, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] refresh the content', label)

def default_on_pre_load(label, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] invoke the loader to load the content', label)

def default_on_post_load(label, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] save the result of loader to the buffer', label)

def default_on_load_error(label, timestamp, error):
    if LOG.isEnabledFor(logging.ERROR):
        LOG.log(logging.ERROR, 'SettingCapsule[%s] error in loader function call', label)
