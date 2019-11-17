
import MySQLdb
import MySQLdb.cursors
from util.DateEncoder import DateEncoder
import json


class DBUtil:
    @staticmethod
    def getdb(self):
        return  MySQLdb.connect(host='www.wupicheng.com', user='root', \
                                passwd='824761abcD!', db='weserver2', use_unicode=1, \
                                charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
    @staticmethod
    def getQuery(sql):
        print('[dbutil][getQueryJson]')
        db=DBUtil.getdb()
        cur = db.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        # jj = {}
        # jj['data'] = rs
        # jj['success'] = 'true'
        # jj['message'] = 'true'
        # j = json.dumps(rs, ensure_ascii=False, cls=DateEncoder)
        cur.close()
        db.close()
        return rs