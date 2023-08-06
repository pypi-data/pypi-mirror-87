#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import hmac
import base64
from datetime import datetime,timedelta
from urllib.parse import urlunparse, urlparse
from tornado.escape import utf8, to_unicode
from tornado.httputil import HTTPHeaders


def generate_md5(password):
    '''
    生成MD5值
    :param password:传输的明文
    :return:
    '''
    md5Obj = hashlib.md5()
    md5Obj.update(utf8(password))
    return md5Obj.hexdigest()


def url_join(url, path='/', query=''):
    """
        url拼接
    """
    parser_ret = urlparse(url)
    components = (parser_ret.scheme, parser_ret.netloc, path,
                  '', query, '')
    return urlunparse(components)


def current_timestamp():
    """
        获取当前的时间戳,V4使用
    """
    return str(int(datetime.now().timestamp() * 1000))


def get_current_datetime(format_str='%Y%m%d', days=None):
    """
    获取当前的时间，显示格式化后的时间
    :param format_str:格式化符号拼接
    :param days:设置前天或后天
    :return:
    """
    current_time = datetime.now()
    if days:
        sum_time = current_time + timedelta(days=days)
        return sum_time.strftime(format_str)
    else:
        return current_time.strftime(format_str)


def make_header(spKey, body_content):
    """
    生成请求头部的信息
    :param spKey: 密钥
    :param body_content: 提交的短信的body
    :return: 返回字典类型
    """""
    headers = HTTPHeaders({'Content-Type': 'application/json;charset=utf-8'})
    timestamp = current_timestamp()
    msg = body_content + timestamp
    signature = hmac.new(utf8(spKey), utf8(msg), digestmod=hashlib.sha256).digest()
    signature_base64 = to_unicode(base64.standard_b64encode(signature))
    headers.add('Authorization', 'HMAC-SHA256 {timestamp},{signature}'.format(
        timestamp=timestamp,
        signature=signature_base64
    ))
    return headers


if __name__ == '__main__':
    url = 'https://book.qidian.com/info/1004608738?wd=123&page=20#Catalog'
    ret = url_join(url, '/', '')
    print(ret)
