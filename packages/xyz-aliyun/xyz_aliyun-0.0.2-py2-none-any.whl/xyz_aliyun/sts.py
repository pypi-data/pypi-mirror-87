# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2

def sts_auth(SecretId, SecretKey, ap, role, session_name):
    pass