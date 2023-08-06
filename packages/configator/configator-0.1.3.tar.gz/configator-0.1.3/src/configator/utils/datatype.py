#!/usr/bin/env python3

def str_to_int(value):
    try:
        return int(value), None
    except ValueError as err:
        return value, err
