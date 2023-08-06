#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from tornado.escape import json_encode, utf8
from tornado.httpclient import HTTPRequest

from xsxx.base_channel import BaseChannel
from xsxx.util import generate_md5, url_join, make_header, get_current_datetime


class SmsV3HttpChannel(BaseChannel):

    def __init__(self, url, userId, password, request_timeout=0, connect_timeout=0):
        self.header = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.userId = userId
        self.md5password = generate_md5(password)
        self.url = url
        self.request_timeout = request_timeout
        self.connect_timeout = connect_timeout

    def content_arr_handler(self, content, mobile, msgId=None, extCode=None):
        """
            手机号与内容的包装
        :param content:短信内容
        :param mobile:短信号码（单个内容只能对应一个手机号）
        :param msgId:消息id,（Long）可不传，如果传的话结果中原样返回，如果不传，我们系统会生成一个.
        :param extCode:扩展码，手机上显示来源号码的后几位数字
        :return:
        """
        ret = {
            'content': content,
            'mobile': mobile
        }
        if msgId:
            ret['msgId'] = msgId
        if extCode:
            ret['extCode'] = extCode
        return ret

    def contents_phones(self, contentArr):
        """
            不同内容，不同号码
        :param contentArr:
        :return:字典类型
        """
        url = url_join(self.url, path='/batchwebsms/smsJsonService')

        post_body = [
            ('userId', self.userId),
            ('md5password', self.md5password),
            ('contentArr', json_encode(contentArr))
        ]
        return HTTPRequest(
            url=url,
            method='POST',
            body=utf8(urlencode(post_body)),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=self.header,
            user_agent='python-sdk',
        )

    def one_content_phones(self, content, mobile, msgId=None, extCode=None):
        '''
        单内容多号码批量发送,即群发
        :param content:短信内容
        :param mobile:手机号码
        :param msgId:消息ID
        :param extCode:扩展码
        :return:HTTPRequest对象
        '''
        url = url_join(self.url, path='/websms/smsJsonService', query='action=sendsms')
        post_body = [
            ('userId', self.userId),
            ('md5password', self.md5password),
            ('content', content),
            ('mobile', mobile),
        ]

        if msgId:
            post_body.append(('msgId', msgId))
        if extCode:
            post_body.append(('extCode', extCode))
        return HTTPRequest(
            url=url,
            method='POST',
            body=utf8(urlencode(post_body)),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=self.header,
            user_agent='python-sdk',
        )

    def get_user_balance(self):
        """
            获取余额
        :return:
        """
        url = url_join(self.url, path='/websms/smsJsonService')

        post_body = [
            ('action', 'getbalance'),
            ('userId', self.userId),
            ('md5password', self.md5password),
        ]
        return HTTPRequest(
            url=url + '?' + urlencode(post_body),
            method='GET',
            body=None,
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=self.header,
            user_agent='python-sdk',
        )

    def get_mo(self):
        """
            获取上行
        :return:
        """
        url = url_join(self.url, path='/websms/smsJsonService')

        post_body = [
            ('action', 'getdeliver'),
            ('userId', self.userId),
            ('md5password', self.md5password),
        ]
        return HTTPRequest(
            url=url + '?' + urlencode(post_body),
            method='GET',
            body=None,
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=self.header,
            user_agent='python-sdk',
        )

    def get_report(self):
        """
            获取状态报告
        :return:
        """
        url = url_join(self.url, path='/websms/smsJsonService')

        post_body = [
            ('action', 'getsendreport'),
            ('userId', self.userId),
            ('md5password', self.md5password),
        ]
        return HTTPRequest(
            url=url + '?' + urlencode(post_body),
            method='GET',
            body=None,
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=self.header,
            user_agent='python-sdk'
        )


class SmsV4HttpChannel(BaseChannel):

    def __init__(self, url, userId, password, request_timeout=0, connect_timeout=0):
        self.spId = userId
        self.spKey = password
        self.url = url
        self.request_timeout = request_timeout
        self.connect_timeout = connect_timeout

    def one_content_phones(self, content, mobile, sId=None, extCode=None):
        """
            多号码单内容发送
        :param content: 短信内容，例如： 【线上线下】您的验证码为123456，在10分钟内有效。
        :param mobile:短信号码，多个用“,”分割，号码数量<=1W
        :param sId:扩展码，必须可解析为数字
        :param extCode:批次号，可用于客户侧按照批次号对短信进行分组
        :return:
        """
        send_url = url_join(self.url, '/sms/send/{spId}'.format(spId=self.spId))

        post_body = {
            'content': content,
            'mobile': mobile
        }

        if sId:
            post_body['sId'] = sId

        elif extCode:
            post_body['extCode'] = extCode

        body_content = json_encode(post_body)

        return HTTPRequest(
            url=send_url,
            method='POST',
            body=utf8(body_content),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=make_header(self.spKey, body_content),
            user_agent='python-sdk',
        )

    def content_arr_handler(self, content, mobile, msgId=None, extCode=None, sId=None):
        """
            手机号与内容的包装
        :param content:短信内容
        :param mobile:短信号码（单个内容只能对应一个手机号）
        :param msgId:消息id,（Long）可不传，如果传的话结果中原样返回，如果不传，我们系统会生成一个.
        :param extCode:扩展码，手机上显示来源号码的后几位数字
        :param sId:自定义标识id,回调时一起推回该标识
        :return:
        """
        ret = {
            'content': content,
            'mobile': mobile
        }
        if msgId:
            ret['msgId'] = msgId
        if extCode:
            ret['extCode'] = extCode
        if sId:
            ret['sId'] = sId
        return ret

    def contents_phones(self, contentArr):
        """
            不同内容，不同号码
        :param contentArr:
        :return:字典类型
        """
        send_url = url_join(self.url, '/sms/sendBatch/{spId}'.format(spId=self.spId))

        post_body = json_encode(contentArr)

        return HTTPRequest(
            url=send_url,
            method='POST',
            body=utf8(post_body),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=make_header(self.spKey, post_body),
            user_agent='python-sdk',
        )

    def get_mo(self, maxSize=500):
        """
            上行主动获取
        :param maxSize:默认500，支持范围[10, 1000]，参数超出范围按照默认算
        :return:
        """
        send_url = url_join(self.url, '/sms/getUpstream/{spId}'.format(spId=self.spId))

        post_body = json_encode({'maxSize': maxSize})

        return HTTPRequest(
            url=send_url,
            method='POST',
            body=utf8(post_body),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=make_header(self.spKey, post_body),
            user_agent='python-sdk',
        )

    def get_report(self, maxSize=500):
        """
            获取状态报告
        :param maxSize:默认500，支持范围[10, 1000]，参数超出范围按照默认算
        :return:
        """
        send_url = url_join(self.url, '/sms/getReport/{spId}'.format(spId=self.spId))

        post_body = json_encode({'maxSize': maxSize})

        return HTTPRequest(
            url=send_url,
            method='POST',
            body=utf8(post_body),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=make_header(self.spKey, post_body),
            user_agent='python-sdk',
        )

    def get_daily_stats(self, date_str=get_current_datetime()):
        """
            获取发送账号日统计
        :param date_str: 日期格式化：yyyyMMdd ，默认获取当前的时间
        """
        send_url = url_join(self.url, '/sms/getDailyStats/{spId}'.format(spId=self.spId))

        post_body = json_encode({'date': date_str})

        return HTTPRequest(
            url=send_url,
            method='POST',
            body=utf8(post_body),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=make_header(self.spKey, post_body),
            user_agent='python-sdk',
        )

    def get_user_balance(self):
        """
            预付费账号余额查询
        """
        send_url = url_join(self.url, '/sms/getBalance/{spId}'.format(spId=self.spId))

        post_body = ''

        return HTTPRequest(
            url=send_url,
            method='POST',
            body=utf8(post_body),
            validate_cert=False,
            request_timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            headers=make_header(self.spKey, post_body),
            user_agent='python-sdk',
        )