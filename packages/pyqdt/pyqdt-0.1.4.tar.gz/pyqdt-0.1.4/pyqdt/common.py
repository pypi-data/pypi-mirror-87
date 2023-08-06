# -*- coding: utf-8 -*-

import datetime
import time
import re

def formatter_st(v, default=None) -> time.struct_time:
    if v is None:
        v = default
    if type(v) == time.struct_time:
        return v
    elif type(v) == str and re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', v):
        return time.strptime(v, '%Y-%m-%d %H:%M:%S')
    if type(v) == str and re.match(r'\d{14}', v):
        return time.strptime(v, '%Y%m%d%H%M%S')
    elif type(v) == str and re.match(r'\d{4}-\d{2}-\d{2}', v):
        return time.strptime(v, '%Y-%m-%d')
    elif type(v) == str and re.match(r'\d{8}', v):
        return time.strptime(v, '%Y%m%d')
    elif type(v) == str and re.match(r'\d{2}:\d{2}:\d{2}', v):
        return time.strptime(v, '%H:%M:%S')
    elif type(v) == str and re.match(r'\d{6}', v):
        return time.strptime(v, '%H%M%S')
    elif type(v) == datetime.time:
        return time.strptime(v.strftime('%H:%M:%S'), '%H:%M:%S')
    elif type(v) == datetime.datetime or type(v) == datetime.date:
        return v.timetuple()
    else:
        raise ValueError('the value must be str, struct_time or datetime.')


def formatter_list(v, default=None) -> list:
    if v is None:
        v = default
    if type(v) is list:
        return v
    elif type(v) is str:
        return [v]
    elif v is None:
        return []
    else:
        raise ValueError('the value must be str or list')


def read_kvfile(kvfile) -> dict:
    result = dict()
    with open(kvfile, 'r') as f:
        lines = f.readlines()
        for s in lines:
            s = s.strip()
            if not s:
                continue
            p = s.find('=')
            if p <= 0:
                continue
            k = s[0:p].strip()
            v = s[p + 1:].strip()
            if not k or not v:
                continue
            result[k] = v
    return result