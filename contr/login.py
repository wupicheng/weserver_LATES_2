
from util.sendMail import SendMail
from util.util import WeUtil
from util.dbutil import DBUtil
from util.DateEncoder import DateEncoder
import re
import random
import json

def sendMail(event,context):
    #检查用户名邮件地址是否存在
    querystr=event["queryString"]
    error_msg=''
    email= querystr['email_address']
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        rs=  DBUtil.getQuery(" select * from we_user where t_c_1='"+email+"'")
        if(len(rs)>0):
            error_msg='账号已存在'
        else:
            checkcode=getCheckCode()
            mail_result=  SendMail.sendMail(email,checkcode)
            if(mail_result=='邮件发送成功'):
                DBUtil.insertData(" insert into check_code(t_c_1,t_c_2) values('"+email+"','"+checkcode+"')")
                error_msg='邮件发送成功'

    else:
        error_msg='邮箱格式不正确'
    j={}
    j['error_msg']=error_msg
    jj=json.dumps(j, ensure_ascii=False,cls=DateEncoder)
    print(str(jj))
    return result(jj)
def result(j):
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body":j
    }
def getCheckCode():
    check_code = ''

    for i in range(4):
        current = random.randrange(0, 4)
        if current == i:
            tmp = chr(random.randint(65, 90))
        else:
            tmp = random.randint(0, 9)
        check_code += str(tmp)
    print(check_code)
    return check_code