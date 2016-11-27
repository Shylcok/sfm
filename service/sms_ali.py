#!/usr/local/bin/python
# -*- coding:utf-8 -*-


import urllib
import httplib
import uuid
import datetime
import logging
import hmac
import base64
import hashlib
import json
import string

port = 80
host = 'http://sms.aliyuncs.com/'



def generator_sign(params, key_secret):
    keys = params.keys()
    keys.sort()
    params_str = ''
    for key in keys:
        key_str = params[key]
        # if type(key_str) is dict or type(key_str) is tuple:
        #     key_str = json.dumps(key_str)
        params_str = params_str + urllib.quote(str(key), safe='') + '=' + urllib.quote(str(key_str), safe='') + '&'

    params_str = params_str[0: -1]
    string_to_sign = "POST" + '&' + urllib.quote('/', safe='') + '&' + urllib.quote(params_str, safe='')

    # StringToSign = urllib.urlencode(params)
    # hash = hmac.new(key_secret)
    # hash.update(StringToSign)
    # HMAC = hash.hexdigest()
    # signature = base64.encodestring(HMAC)
    signature = hmac.new(key_secret, string_to_sign, hashlib.sha1).digest().encode('base64').rstrip()
    signature = urllib.quote(signature, safe='')
    print signature
    return signature


params = {
    "AccessKeyId": "testid",
    "Action": "SingleSendSms",
    "Format": "XML",
    "ParamString":"{\"name\":\"d\",\"name1\":\"d\"}",
    "RecNum": "13098765432",
    "RegionId": "cn-hangzhou",
    "SignName":"标签测试",
    "SignatureMethod": "HMAC-SHA1",
    "SignatureNonce": "9e030f6b-03a2-40f0-a6ba-157d44532fd0",
    "SignatureVersion": "1.0",
    "TemplateCode": "SMS_1650053",
    "Timestamp": "2016-10-20T05:37:52Z",
    "Version": "2016-09-27"
}

# generator_sign(params, 'testsecret&')

from time import strftime

def send_sms_verify(text, mobile):
    params_dict = {'AccessKeyId': 'LTAIeYfXwFJaZqLv',
                   'Action': 'SingleSendSms',
                   'Format': 'json',
                   'ParamString': "{\"verify\": \"%s\"}" % text,
                   'RecNum': mobile,
                   'RegionId': 'cn-hangzhou',
                   'SignName': 'verify',
                   'SignatureMethod': 'HMAC-SHA1',
                   'SignatureNonce': str(uuid.uuid1()),
                   'SignatureVersion': '1.0',
                   'TemplateCode': 'SMS_29920056',
                   'Timestamp': datetime.datetime.utcnow().isoformat(''),
                   'Version': '2016-09-27'
                   }
    signature = generator_sign(params_dict, 'bjYBcuTTplbhTbQJElkMZyPJHPxYoU&')
    # params_dict.update({'Signature': signature})
    # params = urllib.urlencode(
    #     params_dict
    # )
    keys = params_dict.keys()
    keys.sort()
    params_str = "Signature=%s&" % signature
    for key in keys:
        key_str = params_dict[key]
        params_str = params_str + key + "=" + key_str + "&"
    params_str = params_str[0: -1]

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection('sms.aliyuncs.com', port=port, timeout=30)
    conn.request("POST", host, params_str, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    logging.info(response_str)
    print response_str
    return response_str


if __name__ == '__main__':
    send_sms_verify(u"11", "13636672480")

    # mobile = "18721645360"
    # text = "4001"
    #
    # #���˻����
    # print(get_user_balance())
    #
    # #��������ƥ��ģ��ӿڷ�����
    # print(send_sms(text, mobile))
