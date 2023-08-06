#!/usr/bin/env python3

import logging

from configator.engine.connector import RedisClient
from configator.utils.function import assure_not_null, json_dumps
from typing import List, Tuple, Dict, Optional, Union

LOG = logging.getLogger(__name__)

class SettingPublisher(object):
    #
    def __init__(self, *args, connector=None, **kwargs):
        if isinstance(connector, RedisClient):
            self.__use_shared_connector = True
            self.__connector = connector
        else:
            self.__use_shared_connector = False
            self.__connector = RedisClient(**kwargs)
        #
        self.CHANNEL_PREFIX = self.__connector.CHANNEL_GROUP + ':'
        #
        super(SettingPublisher, self).__init__(**kwargs)
    #
    ##
    @property
    def connector(self):
        return self.__connector
    #
    ##
    def publish(self, message: Union[Dict, bytes, str, int, float],
            label: Optional[Union[bytes,str]] = None,
            with_datetime: Optional[bool] = False,
            raise_on_error: Optional[bool] = False) -> Optional[Exception]:
        try:
            self.__publish_or_error(message, label=label, with_datetime=with_datetime)
            return None
        except Exception as err:
            if raise_on_error:
                raise err
            return err
    #
    #
    def __publish_or_error(self, message, label=None, with_datetime=False):
        if label is None:
            channel_name = self.__connector.CHANNEL_GROUP
        else:
            if isinstance(label, bytes):
                label = label.decode('utf-8')
            else:
                label = str(label)
            channel_name = self.CHANNEL_PREFIX + label
        #
        if isinstance(message, (dict, list)):
            message, err = json_dumps(message, with_datetime=with_datetime)
            if err:
                if LOG.isEnabledFor(logging.ERROR):
                    LOG.log(logging.ERROR, err)
                raise err
        elif not self.__is_valid_type(message):
            errmsg = "Invalid type of input: '%s'. Only a dict, list, bytes, string, int or float accepted." % type(message)
            if LOG.isEnabledFor(logging.ERROR):
                LOG.log(logging.ERROR, errmsg)
            raise ValueError(errmsg)
        #
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "publish() a message [%s] to channel [%s]", str(message), channel_name)
        #
        assure_not_null(self.__connector.connect(pinging=False, retrying=False)).publish(channel_name, message)
    #
    #
    def close(self):
        if not self.__use_shared_connector:
            self.__connector.close()
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "SettingPublisher has closed")
    #
    #
    @staticmethod
    def __is_valid_type(data):
        return isinstance(data, (bytes, str, float)) or (isinstance(data, int) and (type(data) != type(True)))
