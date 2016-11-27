# -*- coding: utf-8 -*-
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant

host = "http://test-cn-qingdao.alicloudapi.com"
url = "/api/billing/test/123243?queryparam=query1"

cli = client.DefaultClient(app_key="appKey", app_secret="appSecret")

# GET
# req = request.Request(host=host,protocol=constant.HTTP, url=url, method="GET", time_out=30000)
# print cli.execute(req)


#post body stream

# import json
# req_post = request.Request(host=host, protocol=constant.HTTP, url=url, method="POST", time_out=30000)
# body = {}
# body["name"] = "testName1111111"
# body["address"] = "testAddress"
# body["email"] = "testemail@123.com"
# req_post.set_body(bytearray(source=json.dumps(body), encoding="utf8"))
# req_post.set_content_type(constant.CONTENT_TYPE_STREAM)
# print cli.execute(req_post)


#post form

# req_post = request.Request(host=host, protocol=constant.HTTP, url=url, method="POST", time_out=30000)
# bodyMap = {}
# bodyMap["bodyForm1"] = "fwefwef"
# bodyMap["bodyForm2"] = "ffwefwef"
# req_post.set_body(bodyMap)
# req_post.set_content_type(constant.CONTENT_TYPE_FORM)
# print cli.execute(req_post)


# import datetime
# import uuid
#
# host = "http://sms.aliyuncs.com"
#
# url = "/?Action=SingleSendSms" \
#     + '&ParamString={"verify":"1111"}' \
#     + "&RecNum=13636672480" \
#     + "&SignName=verify" \
#     + "&TemplateCode=SMS_29920056"\
#     + "&Version=2016-09-27"\
#     + "&Timestamp=%s" % datetime.datetime.utcnow().isoformat()\
#     + "&SignatureNonce=%s" % str(uuid.uuid1())\
#     + "&AccessKeyId=LTAIeYfXwFJaZqLv"\
#     + "&SignatureMethod=HMAC-SHA1"\
#     + "&SignatureVersion=1.0"\
#
# req = request.Request(host=host, url=url, method="GET", time_out=30000)
# cli = client.DefaultClient(app_key="LTAIeYfXwFJaZqLv", app_secret="bjYBcuTTplbhTbQJElkMZyPJHPxYoU")
# print cli.execute(req)




host = "http://sms.market.alicloudapi.com"

url = "/singleSendSms" \
    + '?ParamString={"verify":"1111"}' \
    + "&RecNum=13636672480" \
    + "&SignName=verify" \
    + "&TemplateCode=SMS_29980098"

req = request.Request(host=host, url=url, method="GET", time_out=30000)
cli = client.DefaultClient(app_key="23548833", app_secret="9c3ee6c6ce6e3296e89988e653d0bf93")
print cli.execute(req)