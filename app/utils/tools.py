#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
tools
'''

import time, hashlib, hmac, base64

async def gen_timestamp():
    '''
    生成X-Timestamp
    '''
    return str(int(time.time()))

async def gen_log_id():
    '''
    生成X-Log-Id
    '''
    total_ns = time.time_ns()
    sec = total_ns // 1_000_000_000
    nano = total_ns % 1_000_000_000
    time_str = f"{sec}{nano:09d}"
    log_id = f"log_{hashlib.md5(time_str.encode()).hexdigest()[:16]}"
    return log_id

async def gen_signature(app_key: str, app_secret, timestamp: str, log_id: str, extra_info: str = ''):
    '''
    生成X-Sign
    '''
    sign_string = f"app_key:{app_key}|ts:{timestamp}|logid:{log_id}|extra_info:{extra_info}"
    key = app_secret.encode("utf-8")
    msg = sign_string.encode("utf-8")
    signature_bin = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(signature_bin).decode("utf-8")


