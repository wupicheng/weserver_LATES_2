#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import os
import mimetypes
import MySQLdb
from util.util import WeUtil
from util.controller import Controller

# mimetypes=MimeTypes()

def render_template(html, keys={}):
    for k, v in keys.items():
        html = html.replace("${" + k + "}", v)
    return html

dir_path = os.path.dirname(os.path.abspath(__file__))
static_root="/public"
type=''
print('当前目录绝对路径:',dir_path)
def binaryReturn(absolute_path):
    with open(absolute_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        html = s
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {'Content-Type': type},
        "body": html
    }
def checkLogin(session_key):
    sql=" select * from we_session where t_c_2='"+session_key+"'"
    print('checkLogin')
    db= WeUtil.getdb()
    cur = db.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    if(len(rs)>0):
        return True
    else:
        return False

def main_handler(event, context):
    global f
    relative_path=str(event["path"])#请求的路径/weserver/index.html
    relative_file=""
    print(relative_path)
    type=mimetypes.guess_type(relative_path)[0]#根据路径的扩展名确定 content-type
    if(relative_path.find("/controller")==0):
        print('controller')
        return  Controller.controllerHandler(relative_path,event,context)

    if(relative_path.index("/",0)==0):
        relative_file=relative_path
        if(relative_file=='' or relative_file=='/'):
            relative_file='/index.html'#/weserver 这种路径表示用户打开的是网站首页
    else:
        relative_file="/index.html"


    absolute_path=dir_path+static_root+relative_file
    #判断登录进行拦截
    if(type==None):
        type=''
    if(type.find("html")>-1):
        print('登录拦截')
        if(checkLogin(WeUtil.getSession_Token(context)) or relative_file.find("syspage")>-1):
            print('登录成功')
        else:
            print('跳转到登录页')
            absolute_path=dir_path+'/public/syspage/login.html'

    if not os.path.exists(absolute_path):
        absolute_path=dir_path+'/public/syspage/404.html'
    if(type!=None and type.find('image')>-1):
        with open(absolute_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            html=s
        return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {'Content-Type': type},
        "body":html
        }
    elif(relative_path.find('woff') > -1):
        type = 'application/x-font-woff'
        return binaryReturn(absolute_path)
    elif( relative_path.find('ttf') > -1):
        type = 'application/octet-stream'
        return binaryReturn(absolute_path)

    else:
        f = open(absolute_path, encoding='utf-8')
        html = f.read()
    # keys = {
    #     "master": "腾讯云云函数团队", # 您的名称
    #     "centralCouplet": "年年有余", # 横批
    #     "upCouplet": "千年迎新春", # 上联
    #     "downCouplet": "瑞雪兆丰年" # 下联
    # }
    # html = render_template(html, keys)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': type},
        "body":html+"<br>"+relative_path
    }#调试路径信息 "  relative_path"+relative_path+" dir_path="+dir_path+" absolute_pa"+absolute_path