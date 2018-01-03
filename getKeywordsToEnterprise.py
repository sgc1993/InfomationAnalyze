import getKeywordsToExpert
import DataBase
import json

def init():
    global mssql
    mssql = DataBase.MSSQL('10.168.103.8', 'STIMSTEST', 'sa', '1q2w3e4r5t!')

#获取所有的机构id 列表
def getEnterpriseIdList():
    resultList = mssql.ExecQuery("select id from EnterpriseInfo")
    idList = []
    for result in resultList:
        idList.append(result[0])
    return idList

#获取对应id机构下的专家id列表
def getEnterpriseExpertIdListByEnterpriseId(id):
    resultList = mssql.ExecQuery("select expertid from Expert2Enterprise where enterpriseid = %d"%id)
    if len(resultList) == 0:
        return []
    expertIdList = []
    for result in resultList:
        expertIdList.append(result[0])
    return expertIdList

#根据专家id,获得对应专家的关键词转化的词典dict
def getExpertKeywordsDictByExpertId(id):
    resultList = mssql.ExecQuery("select keywords from Expert where id = %d"% id)
    if len(resultList) == 0:
        return {}
    if resultList[0][0] == None:
        return {}
    keywordDict = json.loads(resultList[0][0])
    return keywordDict

#合并关键词词典
def unionDict(dict1,dict2):
    d1keys = dict1.keys()
    for key in d1keys:
        if key in dict2:
            dict2[key] = dict2[key] + dict1[key]
        else:
            dict2[key] = dict1[key]
    return dict2

#根据企业Id获得企业的关键词字符串
def getEnterpriseKeywordsByEnterpriserId(id):
    expertIdList = getEnterpriseExpertIdListByEnterpriseId(id)
    enterpriseKeywordDict = {}
    for expertId in expertIdList:
        expertKeywordDict = getExpertKeywordsDictByExpertId(expertId)
        enterpriseKeywordDict = unionDict(enterpriseKeywordDict,expertKeywordDict)
    enterpriseKeywordStr = json.dumps(enterpriseKeywordDict,ensure_ascii=False)
    return enterpriseKeywordStr

#获得企业关键词，插入到数据库字段中
def updateEnterpriseKeywordsByEnterpriserId(id):
    enterpriseKeywordStr = getEnterpriseKeywordsByEnterpriserId(id)
    if enterpriseKeywordStr == "{}":
        return
    mssql.ExecNonQuery("update EnterpriseInfo set keywords = '%s' where id = %d" % (enterpriseKeywordStr, id))

#总的程序入口
def getKeywordsToEnterprise():
    init()
    enterpriseIdList = getEnterpriseIdList()
    for enterpriseId in enterpriseIdList:
        updateEnterpriseKeywordsByEnterpriserId(enterpriseId)

if __name__ == '__main__':
    getKeywordsToEnterprise()