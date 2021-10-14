#-*-coding:utf-8-*-
import os
import datetime
import time
import ddddocr
import requests
from flask import Flask

"""
eshop商城seller后台获取图形验证码并解析返回
"""
app = Flask(__name__)


def request(url,method,headers,body,format_json='json'):
#发送请求
    try:
        if method.upper() == "GET":
            return requests.get(url, verify=False, params=body.encode("utf-8"), headers=headers)
        elif method.upper() == "POST":
            return requests.post(url, verify=False, data=body.encode("utf-8"), headers=headers)
    except:
        log("请求不为GET/POST,请求失败",1)

def get_verify_code():
#获取验证码
    url = 'https://api.shuidihealth.com/api/eshop/base-api/captchas/eba22dc0-28c7-11ec-8908-1dd87f96495d/LOGIN?rmd='+ str(time_now("timestamp")*1000)
    method = "get"
    resp = request(url,method,headers="",body="").content
    return resp

def log(msg, err=None):
#打印日志
    if err:
        return ("{}""{}""{}""{}""{}".format("【", str(time_now("date_time"))[:19], "】", " ERROR ", msg))
    else:
        return ("{}""{}""{}""{}""{}".format("【", str(time_now("date_time"))[:19], "】", " INFO ", msg))

def time_now(param):
#时间和时间戳
    timestamp = int(time.time())
    date_time = datetime.datetime.fromtimestamp(timestamp)
    if param == "timestamp":
        return timestamp
    elif param == "date_time":
        return date_time

def write_code():
#写读文件并识别验证码
    with open(os.getcwd()+"/abc.jpg","wb") as file_write:
        file_write.write(get_verify_code())
    with open(os.getcwd()+"/abc.jpg","rb") as file_rede:
        img = file_rede.read()
        return img

@app.route("/",methods=["GET"])
def verify_decode():
#识别验证码
    return ddddocr.DdddOcr().classification(write_code())

print(verify_decode())

app.config['JSON_AS_ASCII'] = False
app.run(host='0.0.0.0',port=8091)
