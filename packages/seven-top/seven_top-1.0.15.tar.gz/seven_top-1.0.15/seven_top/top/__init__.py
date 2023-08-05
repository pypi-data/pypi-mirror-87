# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-07-08 10:14:46
@LastEditTime: 2020-08-11 11:49:04
@LastEditors: HuangJingCan
@Description: 
"""
from seven_top.top.api.base import sign


class appinfo(object):
    def __init__(self, appkey, secret):
        self.appkey = appkey
        self.secret = secret


def getDefaultAppInfo():
    pass


def setDefaultAppInfo(appkey, secret):
    default = appinfo(appkey, secret)
    global getDefaultAppInfo
    getDefaultAppInfo = lambda: default
