#!/usr/bin/env python3

import datetime
import json
from typing import Any, Callable, List, Tuple, Dict, Optional, Union


def json_dumps(obj, indent=None, with_datetime=False):
    if isinstance(obj, str):
        return obj
    try:
        if with_datetime:
            return json.dumps(obj, ensure_ascii=False, indent=indent, default=datetime_to_string), None
        return json.dumps(obj, ensure_ascii=False, indent=indent), None
    except Exception as exception:
        return obj, exception


def json_loads(data):
    if not isinstance(data, str):
        return data, None
    try:
        json_dict = json.loads(data)
        return json_dict, None
    except Exception as exception:
        return data, exception


def datetime_to_string(o):
    if o and isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    return o


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


def match_by_label(name: Union[bytes, str]) -> Callable[[Dict, Any], bool]:
    if isinstance(name, str):
        name = bytes(name, 'utf-8')
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


def assure_not_null(conn):
    if conn is None:
        raise ValueError("The connecting is broken")
    return conn


def build_url(connection_args, hide_secret=False):
    scheme = 'redis'
    if connection_args.get('scheme'):
        scheme = connection_args.get('scheme')
    #
    credential = ''
    if connection_args.get('password'):
        if hide_secret:
            credential = '*' * len(connection_args.get('password'))
        else:
            credential = connection_args.get('password')
    if connection_args.get('username') and credential:
        credential = connection_args.get('username') + ':' + credential
    if credential:
        credential = credential + '@'
    #
    return "{_scheme_}://{credential}{host}:{port}/{db}".format(**connection_args,
            _scheme_=scheme, credential=credential)


def extract_parameters(message, err):
    if not err and isinstance(message, dict):
        params = message.get('data')
        if isinstance(params, (dict, list)):
            return params
    return None
