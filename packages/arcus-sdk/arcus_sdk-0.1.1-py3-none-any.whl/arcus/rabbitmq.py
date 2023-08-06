#!/usr/bin/env python3
# encoding: utf-8
"""
@author: zhoutuo
@license: (C) Copyright © 2018 Yitu Network Technology Co., Ltd.
@contact: tuo.zhou@yitu-inc.com
@software: tester
@file: rabbitmq_helper.py
@time: 2020/11/27 下午5:35
@desc:
"""
import pika
import time
import uuid
import json
from threading import Lock

HOST = 'rabbitmq-service'
# HOST = '127.0.0.1'
USERNAME = 'arcus'
PASSWORD = 'arcus'
VHOST = 'arcus_vhost'

EXCHANGE_NAME = 'case.result.messages'
QUEUE_NAME = 'case.result.messages.collector-group'
ROUTING_KEY = EXCHANGE_NAME


class Rabbitmq(object):
    _instance_lock = Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Rabbitmq, '_instance'):
            with Rabbitmq._instance_lock:
                if not hasattr(Rabbitmq, '_instance'):
                    Rabbitmq._instance = object.__new__(cls)
                    Rabbitmq.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=HOST, virtual_host=VHOST, credentials=pika.credentials.PlainCredentials(USERNAME, PASSWORD)))
                    Rabbitmq.channel = Rabbitmq.connection.channel()
                    Rabbitmq.channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
                    Rabbitmq.channel.queue_declare(queue=QUEUE_NAME, durable=True)
                    Rabbitmq.channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
        return Rabbitmq._instance

    def send(self, obj):
        with self._instance_lock:
            self.channel.basic_publish(exchange=EXCHANGE_NAME,
                                       routing_key=ROUTING_KEY,
                                       properties=pika.BasicProperties(
                                           content_type='application/json',
                                           delivery_mode=2,
                                           priority=0,
                                           headers={},
                                           message_id=str(uuid.uuid1()),
                                           timestamp=int(time.time() * 1000)
                                       ),
                                       body=json.dumps(obj))

    def close(self):
        self.connection.close()
