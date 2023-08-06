#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import functools
from tornado.gen import multi_future
from tornado.ioloop import IOLoop
from tornado.escape import json_decode, to_unicode
from tornado.httpclient import AsyncHTTPClient, HTTPClient


class BaseChannel(object):
    # 最大的并发数，默认：500
    max_clients = 500

    def send_sync_request(self, request, callback_func=None, callback_exception_func=None):
        """
            同步发送请求
            :param request: 请求的对象
            :param callback_func: 正常的回调函数
            :param callback_exception_func: 异常的回调函数
        :return:
        """
        http_client = HTTPClient()
        try:
            response = http_client.fetch(request)
            callback_func(json_decode(to_unicode(response.body)))
        except Exception as err:
            if callback_exception_func:
                callback_exception_func(err, request.headers, request.body)
            else:
                logging.error(err)

    async def send_async_request(self, request, callback_func=None, callback_exception_func=None):
        """
             异步发送请求
        :param request: 请求的对象
        :param max_clients : 并发数
        :param callback_func: 正常的回调函数
        :param callback_exception_func: 异常的回调函数
        :return:
        """
        http_client = AsyncHTTPClient(max_clients=BaseChannel.max_clients)
        try:
            response = await http_client.fetch(request)
            if callback_func:
                callback_func(json_decode(to_unicode(response.body)))
        except Exception as err:
            if callback_exception_func:
                callback_exception_func(err, request.headers, request.body)
            else:
                logging.error(err)

    async def runner(self, request_list, loop, callback_func=None, callback_exception_func=None):
        """
            包装为Future对象，并开始执行函数
        :param request_list:请求对象的列表
        :param loop: 事件循环
        :param callback_func: 回调函数
        :param callback_exception_func:异常回调函数
        :return:
        """
        future_list = []
        for request_obj in request_list:
            future_list.append(
                self.send_async_request(request_obj,
                                        callback_func=callback_func,
                                        callback_exception_func=callback_exception_func)
            )
        await multi_future(future_list)
        loop.clear_current()

    @staticmethod
    def send_request(channel_instance, request_list, callback_func=None, callback_exception_func=None):
        """
        :param channel_instance:SmsV3HttpChannel的实例对象
        :param request_list: 请求对象的列表
        :param callback_func: 回调函数
        :param callback_exception_func: 异常回调函数
        :return:
        """
        loop = IOLoop()
        runner_loop = functools.partial(channel_instance.runner, request_list, loop, callback_func,
                                        callback_exception_func)
        loop.run_sync(runner_loop)
        loop.close()

    def one_content_phones(self, content, mobile, msgId=None, extCode=None):
        raise NotImplementedError()

    def contents_phones(self, contentArr):
        raise NotImplementedError()

    def get_report(self):
        raise NotImplementedError()

    def get_mo(self):
        raise NotImplementedError()

    def get_user_balance(self):
        raise NotImplementedError()
