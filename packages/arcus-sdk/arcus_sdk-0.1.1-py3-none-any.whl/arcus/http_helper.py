#!/usr/bin/env python3
# encoding: utf-8
"""
@author: zhoutuo
@license: (C) Copyright © 2018 Yitu Network Technology Co., Ltd.
@contact: tuo.zhou@yitu-inc.com
@software: tester
@file: http_helper.py
@time: 2020/11/27 下午5:37
@desc:
"""
import requests


def stop_task():
    r = requests.get('http://coordinator-service:9120/record/extra-stop')
    return r.text
