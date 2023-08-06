#!/usr/bin/env python

import logging
import threading

from typing import Callable, Dict, Optional

LOG = logging.getLogger(__name__)

class SettingCapsule():
    __name = None
    __load = None
    __lock = threading.RLock()
    __payload = None
    #
    #
    def __init__(self, name: str, load: Callable):
        assert isinstance(name, str) and name, "[name] must be a string and not empty"
        self.__name = name
        assert callable(load), "[load] must be a function"
        self.__load = load
    #
    #
    @property
    def name(self):
        return self.__name
    #
    #
    @property
    def data(self):
        with self.__lock:
            if self.__payload is None:
                self.__payload = self.__load()
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.log(logging.DEBUG, 'Assign result of load() to the payload')
            return self.__payload
    #
    #
    def reset(self, message: Optional[Dict] = None, err: Optional[Exception] = None):
        with self.__lock:
            self.__payload = None
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, 'payload has been reset')
        return self
