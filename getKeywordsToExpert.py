import DataBase
import ExtractKeywords
import json

#初始化配置：连接数据库，加载停用词
def init():
    global mssql
    mssql = DataBase.MSSQL('10.168.103.8', 'STIMSTEST', 'sa', '1q2w3e4r5t!')
    ExtractKeywords.init()

#在数据库Expert表中，根据专家id获得专家名字,注意处理返回值为空情况
def getNameByExpertId(id):
    resultList = mssql.ExecQuery("select name from Expert WHERE id = %d"%id)
    if len(resultList) == 0:
        return ""
    if resultList[0][0] == None:
        return ""
    return resultList[0][0]

#在数据库Author表中，根据名字找到对应作者发表论文的UID数组
def getPaperUidListByExpertName(name):
    resultList = mssql.ExecQuery("select UID from Author WHERE display_name = '%s'" %name)
    UidList = []
    for result in resultList:
        UidList.append(result[0])
    return UidList

def getProjectIdListByExpertName(name):
    resultList = mssql.ExecQuery("select id from Project WHERE director = '%s'" % name)
    projectIdList = []
    for result in resultList:
        projectIdList.append(result[0])
    return projectIdList

#在数据库Paper表中，根据UID找到对应论文的文本信息，此处由中文标题和中文摘要拼接
def getPaperTextByPaperUid(uid):
    resultList = mssql.ExecQuery("select title_cn,abstract_text_cn from Paper WHERE UID = '%s'"%uid)
    if len(resultList) == 0:
        return ""
    #字段为空时，查询结果为None
    if resultList[0][0] == None:
        resultList[0][0] = ""
    if resultList[0][1] == None:
        resultList[0][1] = ""
    paperText = resultList[0][0] + '。' + resultList[0][1]
    return paperText

def getProjectTextByProjectId(id):
    resultList = mssql.ExecQuery("select main_content,abstract_str,object from Project WHERE id = '%s'" % id)
    if len(resultList) == 0:
        return ""
    # 字段为空时，查询结果为None
    if resultList[0][0] == None:
        resultList[0][0] = ""
    if resultList[0][1] == None:
        resultList[0][1] = ""
    if resultList[0][2] == None:
        resultList[0][2] = ""
    projectText = resultList[0][0] + '。' + resultList[0][1]+ '。'+resultList[0][2]
    return projectText

#在数据库Paper表中，根据UID找到对应论文的keywors字段，解析为keyword数组
def getPaperKeywordListByPaperUid(uid):
    resultList = mssql.ExecQuery("select keywords_cn from Paper WHERE UID = '%s'" % uid)
    if len(resultList) == 0:
        return []
    keywords = resultList[0][0]
    if keywords == None:
        return []
    keywordsList = keywords.split(',')
    return keywordsList

#根据文本信息，抽取关键词数组
def extractKeywordsFromText(text):
    return ExtractKeywords.extractPhrases(text)

#拼接两个关键词数组
def unionKeywordsList(keywordList1,keywordList2):
    return keywordList1 + keywordList2

#根据专家id获得专家对应所有论文的keyword,包括数据自带的keywords和论文文本抽取的keywordList
def getExpertPaperKeywordListByExpertId(id):
    expertName = getNameByExpertId(id)
    if expertName == "" or expertName == None:#如果未查到专家名即id无效，返回空数组
        return []
    paperUidList = getPaperUidListByExpertName(expertName)
    if len(paperUidList) == 0:#Author中没有对应专家，返回空数组
        return []
    keywords = []
    for paperUid in paperUidList:
        paperText = getPaperTextByPaperUid(paperUid)
        #可能有UID不存在的情况，返回空串
        if paperText == "":
            keywordList1 = []
        else:
            keywordList1 = extractKeywordsFromText(paperText)#从paperText中抽取
        keywordList2 =  getPaperKeywordListByPaperUid(paperUid)#paper自带的keywords
        keywordList = unionKeywordsList(keywordList1, keywordList2)
        keywords = unionKeywordsList(keywords, keywordList)
    return keywords

def getExpertProjectKeywordListByExpertId(id):
    expertName = getNameByExpertId(id)
    if expertName == "" or expertName == None:  # 如果未查到专家名即id无效，返回空数组
        return []
    projectIdList = getProjectIdListByExpertName(expertName)
    if len(projectIdList) == 0:#Project中没有对应专家，返回空数组
        return []
    projectKeywordsList = []
    for projectId in projectIdList:
        projectText = getProjectTextByProjectId(projectId)
        # 可能有UID不存在的情况，返回空串
        if projectText == "":
            keywordList = []
        else:
            keywordList = extractKeywordsFromText(projectText)
        projectKeywordsList = unionKeywordsList(projectKeywordsList, keywordList)
    return projectKeywordsList

#根据专家id获得专家对应project和paper的keyword List
def getExpertKeywordListByExpertId(id):
    paperKeywordList = getExpertPaperKeywordListByExpertId(id)
    projectKeywordList = getExpertProjectKeywordListByExpertId(id)
    expertKeywords = unionKeywordsList(paperKeywordList,projectKeywordList)
    return expertKeywords

#根据关键词数组统计关键词出现频率，转化为Dict
def getKeywordDictByList(keywordList):
    keywordDict = {}
    for keyword in keywordList:
        if keywordDict.__contains__(keyword):
            keywordDict[keyword] = keywordDict[keyword] + 1
        else:
            keywordDict[keyword] = 1
    return keywordDict

#用来测试，根据作者名找到对应论文的关键词数组
def getExpertKeywordListByAuthorName(name):
    paperUidList = getPaperUidListByExpertName(name)
    if len(paperUidList) == 0:
        return []
    keywords = []
    for paperUid in paperUidList:
        paperText = getPaperTextByPaperUid(paperUid)
        keywordList1 = extractKeywordsFromText(paperText)
        keywordList2 =  getPaperKeywordListByPaperUid(paperUid)
        keywordList = unionKeywordsList(keywordList1, keywordList2)
        keywords = unionKeywordsList(keywords, keywordList)
    return keywords

#根据传入的专家id，获得对应专家的keyword字符串
def getExpertKeywordsStrByExpertId(id):
    keywordList = getExpertKeywordListByExpertId(id)#获得专家的keyword数组
    keywordDict = getKeywordDictByList(keywordList)#统计keyword词频，转为dict类型
    keywordStr = json.dumps(keywordDict, ensure_ascii=False)#将dict转化为为字符串格式
    return keywordStr

#给对应id的专家插入keywords字段
def updateExpertKeywordsByExpertId(id):
    keywordStr = getExpertKeywordsStrByExpertId(id)
    if keywordStr == "{}":
        return
    mssql.ExecNonQuery("update Expert set keywords = '%s' where id = %d" % (keywordStr, id))

#获得所有专家id列表
def getExpertIdList():
    resultList = mssql.ExecQuery("select id from Expert")
    expertIdList = []
    for result in resultList:
        expertIdList.append(result[0])
    return expertIdList

#程序总入口，为每个Expert专家插入keywords字段
def getKeywordsToExpert():
    init()#初始化，连接数据库
    expertIdList = getExpertIdList()
    for expertId in expertIdList:
        updateExpertKeywordsByExpertId(expertId)

if __name__=='__main__':
    getKeywordsToExpert()



