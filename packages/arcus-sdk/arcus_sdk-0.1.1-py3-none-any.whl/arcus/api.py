#!/usr/bin/env python3
# encoding: utf-8
"""
@author: zhoutuo
@license: (C) Copyright © 2018 Yitu Network Technology Co., Ltd.
@contact: tuo.zhou@yitu-inc.com
@software: tester
@file: api.py
@time: 2020/11/27 下午4:47
@desc:
"""
import time
from arcus import http_helper
from arcus.rabbitmq import Rabbitmq


def add(params):
    results = {}
    for key, value in params.items():
        results[key] = {'latency': value[0], 'outputType': value[1]}
    Rabbitmq().send([{'sampleResults': results, 'transResults': {}, 'ts': time.time()}])


def close():
    Rabbitmq().close()


def stop():
    http_helper.stop_task()


def hello():
    print("hello arcus!")
