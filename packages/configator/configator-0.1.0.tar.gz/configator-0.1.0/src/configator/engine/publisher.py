#!/usr/bin/env python3

import logging
import json

from configator.engine import RedisClient
from typing import List, Tuple, Dict, Optional, Union

LOG = logging.getLogger(__name__)

class SettingPublisher(RedisClient):
    #
    def __init__(self, *args, **kwargs):
        super(SettingPublisher, self).__init__(**kwargs)
        self.CHANNEL_PREFIX = self.CHANNEL_GROUP + ':'
    #
    #
    def publish(self, message: Union[Dict, bytes, str, int, float], label:Optional[str]=None):
        try:
            self.publish_or_error(message, label=label)
            return None
        except Exception as err:
            return err
    #
    #
    def publish_or_error(self, message: Union[Dict, bytes, str, int, float], label:Optional[str]=None):
        if label is None:
            channel_name = self.CHANNEL_GROUP
        else:
            channel_name = self.CHANNEL_PREFIX + label
        #
        if isinstance(message, dict):
            message = json.dumps(message)
        elif not self.__is_valid_type(message):
            errmsg = "Invalid type of input: '%s'. Only a dict, bytes, string, int or float accepted." % type(message)
            if LOG.isEnabledFor(logging.ERROR):
                LOG.log(logging.ERROR, errmsg)
            raise ValueError(errmsg)
        #
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "publish() a message [%s] to channel [%s]", str(message), channel_name)
        #
        self.connect().publish(channel_name, message)
    #
    #
    @staticmethod
    def __is_valid_type(data):
        return isinstance(data, (bytes, str, float)) or (isinstance(data, int) and (type(data) != type(True)))
