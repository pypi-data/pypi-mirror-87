#!/usr/bin/env python3

import json
from typing import Any, Callable, List, Tuple, Dict, Optional


def json_loads(data):
    if not isinstance(data, str):
        return data, None
    try:
        json_dict = json.loads(data)
        return json_dict, None
    except Exception as exception:
        return data, exception


def transform_json_data(message:Dict) -> Tuple[Dict, Any]:
    if not isinstance(message, dict):
        return message, ValueError('message must be a dict')
    #
    if 'data' not in message:
        return message, ValueError('data field not found')
    #
    if not isinstance(message['data'], bytes):
        return message, ValueError('message[data] must be bytes or string')
    #
    obj, err = json_loads(message['data'].decode('utf-8'))
    if obj:
        message['data'] = obj
    return message, err


def match_by_label(name):
    assert isinstance(name, bytes)
    def match_func(message, err, *args, **kwargs):
        if not isinstance(message, dict):
            return False
        #
        channel_name = message.get('channel')
        if not isinstance(channel_name, bytes):
            return False
        #
        return channel_name.endswith(name)
    return match_func
