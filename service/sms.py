#!/usr/local/bin/python
#-*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 ����11:48
# Desc: ����http�ӿڵ�python�������ʾ��
import httplib
import urllib

#�����ַ
# host = "sapi.253.com"
host = "222.73.117.158"

#�˿ں�
port = 80

#�汾��
version = "v1.1"

#���˻���Ϣ��URI
balance_get_uri = "/msg/QueryBalance"

#����ƥ��ģ����Žӿڵ�URI
sms_send_uri = "/msg/HttpBatchSendSM"

#�����˺�
account = "jk_cs_J6"

#��������
password = "FRf789258"

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
    params = urllib.urlencode({'account': account, 'pswd' : password, 'msg': text, 'mobile':mobile, 'needstatus' : 'false', 'extno' : '' })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str 

if __name__ == '__main__':

    mobile = "18721645360"
    text = "4001"

    #���˻����
    print(get_user_balance())

    #��������ƥ��ģ��ӿڷ�����
    print(send_sms(text, mobile))