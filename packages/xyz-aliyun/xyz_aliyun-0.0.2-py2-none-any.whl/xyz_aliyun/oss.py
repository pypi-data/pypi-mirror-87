# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from .utils import get_setting
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2

# from .sts import Sts

A = lambda c: get_setting('OSS', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')
ROLE = A('ROLE')
AP = A('AP') or "cn-shenzhen"
BUCKET = A('BUCKET')
DOMAIN = A('DOMAIN') or '%s.oss-%s.aliyuncs.com' % (BUCKET, AP)


def gen_signature(allow_prefix=None, SecretId=SECRET_ID, SecretKey=SECRET_KEY, expire=300,
                  bucket=BUCKET, method='GET', session_name='nobody'):
    # endpoint = 'http://oss-%s.aliyuncs.com' % AP
    clt = client.AcsClient(SecretId, SecretKey, AP)

    policy_text = """{
            "Version": "1", 
            "Statement": [
              {"Action": ["oss:GetObject","oss:PutObject"], 
                "Effect": "Allow", 
                "Resource": ["acs:oss:*:*:%s/%s"]
              }
            ]
        }""" % (bucket, allow_prefix)
    # print(policy_text)

    req = AssumeRoleRequest.AssumeRoleRequest()
    req.set_accept_format('json')
    req.set_RoleArn(ROLE)
    req.set_RoleSessionName(session_name)
    req.set_Policy(policy_text)
    body = clt.do_action_with_exception(req)
    d = json.loads(oss2.to_unicode(body))

    # auth = oss2.StsAuth(token['Credentials']['AccessKeyId'],
    #                     token['Credentials']['AccessKeySecret'],
    #                     token['Credentials']['SecurityToken'])

    #
    # auth = oss2.Auth(SecretId, SecretKey)
    # the_bucket = oss2.Bucket(auth, endpoint, bucket)
    # surl = the_bucket.sign_url(method, allow_prefix, expire)
    d['region'] = 'oss-%s' % AP
    d['bucket'] = bucket
    return d
