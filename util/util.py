import MySQLdb
import MySQLdb.cursors

class WeUtil:
    @staticmethod
    def getSession_Token(context):
        environ= context['environ']
        ss=environ.split(";")
        session_token=''
        for s in ss:
            k=s.split("=")
            if(k[0]=='TENCENTCLOUD_SESSIONTOKEN'):
                session_token=k[1]
        return session_token

    @staticmethod
    def getdb():
        return  MySQLdb.connect(host='www.wupicheng.com', user='root',\
                             passwd='824761abcD!', db='weserver2', use_unicode=1,\
                             charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)