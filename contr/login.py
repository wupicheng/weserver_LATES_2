
from util.sendMail import SendMail
from util.util import WeUtil
from util.dbutil import DBUtil

def sendMail(event,context):
    #检查用户名邮件地址是否存在
    querystr=event["queryString"]
    DBUtil.getQuery(" select * from ")
    email= querystr['email_address']
