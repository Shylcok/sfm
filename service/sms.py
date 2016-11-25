#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 ����11:48
# Desc: ����http�ӿڵ�python�������ʾ��
import httplib
import urllib

# �����ַ
# host = "sapi.253.com"
host = "222.73.117.158"

# �˿ں�
port = 80

# �汾��
version = "v1.1"

# ���˻���Ϣ��URI
balance_get_uri = "/msg/QueryBalance"

# ����ƥ��ģ����Žӿڵ�URI
sms_send_uri = "/msg/HttpBatchSendSM"

# �����˺�
account = "jkcs-zdA1"

# ��������
password = "DtwpQi23864"
import logging


def get_user_balance():
    """
    ȡ�˻����
    """
    conn = httplib.HTTPConnection(host, port=port)
    conn.request('GET', balance_get_uri + "?account=" + account + "&pswd=" + password)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_sms(text, mobile):
    """
    ���ýӿڷ�����
    """
    params = urllib.urlencode(
        {'account': account, 'pswd': password, 'msg': text, 'mobile': mobile, 'needstatus': 'false', 'extno': ''})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    logging.info(response_str)
    return response_str


import time


def send_sms_1(text, mobile):
    url = """
        https://sms.aliyuncs.com/?Action=SingleSendSms
        &SignName=阿里云短信服务
        &TemplateCode=SMS_1595010
        &RecNum=13636672480
        &ParamString={"no":"123456"}
        &<公共请求参数>
    """


    """"""
    id = "su6838354"
    pwd = "su139527"
    url = "http://service.winic.org:8009/sys_port/gateway/index.asp?id=%s&pwd=%s&to=%s&content=%s&time=%s" % (
    id, pwd, mobile, text, time.time())
    f = urllib.urlopen(url)
    s = f.read()
    print s


if __name__ == '__main__':
    send_sms_1("你好", "13636672480")

    # mobile = "18721645360"
    # text = "4001"
    #
    # #���˻����
    # print(get_user_balance())
    #
    # #��������ƥ��ģ��ӿڷ�����
    # print(send_sms(text, mobile))
