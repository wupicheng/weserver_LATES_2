import requests
import time
import json
from DateEncoder import DateEncoder

class clouddb:
    appid = "wxb8b1234b359673b0" # 小程序唯一appid
    secret = "c6c20d8bae3617cf1407b8271d621b5c" # 小程序
    DB_ENV_ID = "test-89946d"
    ACCESS_TOKEN = "" # 外部服务访问腾讯云的安全码有效期两个小时重复获取会被刷新

    GET_ACCESS_TOKEN_URL="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appid+"&secret="+secret+""
    ADD_CLOUD_COLLECTION_URL="https://api.weixin.qq.com/tcb/databasecollectionadd?access_token="
    DELETE_CLOUD_COLLECTION_URL="https://api.weixin.qq.com/tcb/databasecollectiondelete?access_token="
    CLOUD_COLLECTION_GET_INFO_URL="https://api.weixin.qq.com/tcb/databasecollectionget?access_token="#获取所有集合信息
    INSERT_CLOUD_ITEM_URL="https://api.weixin.qq.com/tcb/databaseadd?access_token=" #插入记录
    DELETE_CLOUD_ITEM_URL="https://api.weixin.qq.com/tcb/databasedelete?access_token=" #删除记录
    UPDATE_CLOUD_ITEM_URL="https://api.weixin.qq.com/tcb/databaseupdate?access_token=" #更新记录
    QUERY_CLOUD_ITEMS_URL="https://api.weixin.qq.com/tcb/databasequery?access_token="
    COUNT_CLOUD_ITEMS_URL="https://api.weixin.qq.com/tcb/databasecount?access_token="

    nowint=0
    # {"access_token":"ACCESS_TOKEN","expires_in":7200}
                # # 错误返回样式
                # # {"errcode":40013,"errmsg":"invalid appid"}
    def checkTockenEXpire(self):
            date = time.time()
            if(date<self.nowint):
                print('tocken还在有效期内')
            else:
                data = requests.get(self.GET_ACCESS_TOKEN_URL).json()
                # r=json.load(data)
                print(data['access_token'])
                print(data['expires_in'])

                self.ACCESS_TOKEN=data['access_token']
                self.nowint=(int(data['expires_in'])-300)+date
# self.checkTockenEXpire()
#发送数据格式{"env": "test2-4a89da","collection_name": "test_add_collection"}
#返回数据示例{ "errcode": 0,  "errmsg": "ok",}
    #添加集合
    def addCollection(self,collectionName):
        self.checkTockenEXpire()
        url=self.ADD_CLOUD_COLLECTION_URL+self.ACCESS_TOKEN+''
        data={'env':self.DB_ENV_ID,"collection_name":collectionName}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    #删除集合
    def deleteCollection(self,collectionName):
        self.checkTockenEXpire()
        url=self.DELETE_CLOUD_COLLECTION_URL+self.ACCESS_TOKEN+''
        data={'env':self.DB_ENV_ID,"collection_name":collectionName}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    #获取所有集合信息
    def getCollectionInfo(self):
        self.checkTockenEXpire()
        url=self.CLOUD_COLLECTION_GET_INFO_URL+self.ACCESS_TOKEN+''
        data={'env':self.DB_ENV_ID,"limit":10,"offset":0}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    def insertItem(self,collection_name,item):
        self.checkTockenEXpire()
        url=self.INSERT_CLOUD_ITEM_URL+self.ACCESS_TOKEN+''
        jj=json.dumps(item,ensure_ascii=False, cls=DateEncoder)
        jjj=str(jj)
        data={'env':self.DB_ENV_ID,"query": "db.collection(\""+collection_name+"\").add({data:"+jjj+" })"}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    def deleteItem(self,collection_name,where):
        self.checkTockenEXpire()
        url=self.DELETE_CLOUD_ITEM_URL+self.ACCESS_TOKEN+''
        jj=json.dumps(where,ensure_ascii=False, cls=DateEncoder)
        jjj=str(jj)
        data={'env':self.DB_ENV_ID, "query": "db.collection(\""+collection_name+"\").where("+jjj+").remove()"}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    def deleteItemById(self,collection_name,id):
        self.checkTockenEXpire()
        url=self.DELETE_CLOUD_ITEM_URL+self.ACCESS_TOKEN+''
        # jj=json.dumps(where,ensure_ascii=False, cls=DateEncoder)
        # jjj=str(jj)
        data={'env':self.DB_ENV_ID, "query": "db.collection(\""+collection_name+"\").doc(\""+id+"\").remove()"}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    def updateItemById(self,collection_name,where,update):
        self.checkTockenEXpire()
        url=self.UPDATE_CLOUD_ITEM_URL+self.ACCESS_TOKEN+''
        # jj=json.dumps(where,ensure_ascii=False, cls=DateEncoder)
        # jjj=str(jj)
        data={'env':self.DB_ENV_ID, "query": "db.collection(\""+collection_name+"\").where("+self.dumpx(where)+").update({data:"+self.dumpx(update)+"})"}
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    #count 最大只能是100条。如果记录很多需要多页分页获取
    #结果返回的数据结构如下
    #{'errcode': 0, 'errmsg': 'ok', 'pager': {'Offset': 0, 'Limit': 100, 'Total': 1}, 'data': ['{"_id":"04a0e69d-e98c-4c71-9059-cdbd021b464d","a":"我爱你","b":"b1"}']}
    def queryItems(self,collection_name,where,count):
        self.checkTockenEXpire()
        url=self.QUERY_CLOUD_ITEMS_URL+self.ACCESS_TOKEN+''
        # jj=json.dumps(where,ensure_ascii=False, cls=DateEncoder)
        # jjj=str(jj)
        data={'env':self.DB_ENV_ID, "query": "db.collection(\""+collection_name+"\").where("+self.dumpx(where)+").limit("+count+").get()"}
        print(data)
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    #统计集合的记录数
    #测试用例如下
    # 统计记录数
    # w = {}
    # d.countItems('xxx1', w)
    #返回结果的数据结构如下{'errcode': 0, 'errmsg': 'ok', 'count': 1}
    def countItems(self,collection_name,where):
        self.checkTockenEXpire()
        url=self.COUNT_CLOUD_ITEMS_URL+self.ACCESS_TOKEN+''
        # jj=json.dumps(where,ensure_ascii=False, cls=DateEncoder)
        # jjj=str(jj)
        data={'env':self.DB_ENV_ID, "query": "db.collection(\""+collection_name+"\").where("+self.dumpx(where)+").count()"}
        print(data)
        j= requests.post(url,json.dumps(data)).json()
        print(j)
        return j
    def dumpx(self,dict):
        jj = json.dumps(dict, ensure_ascii=False, cls=DateEncoder)
        jjj = str(jj)
        return jjj
# d=clouddb()
# d.deleteCollection("xxx")
# d.addCollection("xxx1")
# t={"a":"a1","b":"b1"}
# t2={"a":"a2","b":"b2"}
# list=[]
# list.append(t)
# list.append(t2)
# # d.getCollectionInfo()
# d.insertItem("xxx1",list)

#
# t={'_id':'a08353d25dc42eef001b7b6d03094772'}
# d.deleteItem("xxx1",t)
# d.deleteItemById("xxx1",'a08353d25dc42eef001b7b6d03094772')

#更新测试
# w={'_id':'04a0e69d-e98c-4c71-9059-cdbd021b464d'}
# u={'a':'我爱你'}
# d.updateItemById("xxx1",w,u)

#查询记录
# w={}
# d.queryItems('xxx1',w,'100')

#统计记录数
# w={}
# d.countItems('xxx1',w)