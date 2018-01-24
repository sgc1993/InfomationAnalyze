import DataBase
import ExtractKeywords
import json
import os

sep = os.path.sep

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
    paperText = ""
    #字段为空时，查询结果为None
    if resultList[0][0] != None:
        paperText += resultList[0][0]
    if resultList[0][1] != None:
        paperText = paperText + '。'+ resultList[0][1]
    return paperText

def getProjectTextByProjectId(id):
    resultList = mssql.ExecQuery("select main_content,abstract_str,object from Project WHERE id = '%s'" % id)
    if len(resultList) == 0:
        return ""
    projectText = ""
    # 字段为空时，查询结果为None
    if resultList[0][0] != None:
        projectText += resultList[0][0]
    if resultList[0][1] != None:
        projectText = projectText + '。'+ resultList[0][1]
    if resultList[0][2] != None:
        projectText = projectText + '。' + resultList[0][2]

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

def get_paper_keyword_list_by_paper_uid(paperUid):
    resultList = mssql.ExecQuery("select keywords from Paper WHERE UID = '%s'" % paperUid)
    paper_keyword_list = json.loads(resultList[0][0])
    return paper_keyword_list

#根据专家id获得专家对应所有论文的keyword,包括数据自带的keywords和论文文本抽取的keywordList
def getExpertPaperKeywordListByExpertId(id):
    expertName = getNameByExpertId(id)
    if expertName == "" or expertName == None:#如果未查到专家名即id无效，返回空数组
        return []
    paperUidList = getPaperUidListByExpertName(expertName)
    if len(paperUidList) == 0:#Author中没有对应专家，返回空数组
        return []
    expert_keywords = []
    for paperUid in paperUidList:
        paper_keyword_list = get_paper_keyword_list_by_paper_uid(paperUid)
        #可能有UID不存在的情况，返回空串
        expert_keywords = unionKeywordsList(expert_keywords, paper_keyword_list)
    return expert_keywords

def get_project_keyword_list_by_project_id(project_id):
    resultList = mssql.ExecQuery("select keywords from Project WHERE id = %s" % project_id)
    project_keyword_list = json.loads(resultList[0][0])
    return project_keyword_list

def getExpertProjectKeywordListByExpertId(id):
    expertName = getNameByExpertId(id)
    if expertName == "" or expertName == None:  # 如果未查到专家名即id无效，返回空数组
        return []
    projectIdList = getProjectIdListByExpertName(expertName)
    if len(projectIdList) == 0:#Project中没有对应专家，返回空数组
        return []
    projectKeywordsList = []
    for projectId in projectIdList:
        project_keyword_list = get_project_keyword_list_by_project_id(projectId)
        # 可能有UID不存在的情况，返回空串
        projectKeywordsList = unionKeywordsList(projectKeywordsList, project_keyword_list)
    return projectKeywordsList

def get_patent_id_list_by_expert_id(expert_id):
    resultList = mssql.ExecQuery("select patentid from Patent2Expert WHERE expertid = %d" % expert_id)
    patent_id_list = []
    for result in resultList:
        patent_id_list.append(result[0])
    return patent_id_list

def get_patent_text_by_patent_id(patent_id):
    resultList = mssql.ExecQuery("select name,abstract_cn from Patent WHERE id = '%s'" % patent_id)
    if len(resultList) == 0:
        return ""
    patent_text = ""
    # 字段为空时，查询结果为None
    if resultList[0][0] != None:
        patent_text += resultList[0][0]
    if resultList[0][1] != None:
        patent_text = patent_text + '。' + resultList[0][1]

    return patent_text

def get_patent_keyword_list_by_patent_id(patent_id):
    resultList = mssql.ExecQuery("select keywords from Patent WHERE id = %s" % patent_id)
    patent_keyword_list = json.loads(resultList[0][0])
    return patent_keyword_list

#获得专家的专利中的关键词list
def getExpertPatentKeywordListByExpertId(id):
    patent_id_list = get_patent_id_list_by_expert_id(id)
    patent_keywords_list = []
    for patent_id in patent_id_list:
        one_patent_keyword_list = get_patent_keyword_list_by_patent_id(patent_id)
        # 可能有UID不存在的情况，返回空串
        patent_keywords_list = unionKeywordsList(patent_keywords_list, one_patent_keyword_list)
    return patent_keywords_list

#根据专家id获得专家对应project和paper的keyword List
def getExpertKeywordListByExpertId(id):
    paperKeywordList = getExpertPaperKeywordListByExpertId(id)
    projectKeywordList = getExpertProjectKeywordListByExpertId(id)
    patentKeywordList = getExpertPatentKeywordListByExpertId(id)
    expertKeywords = unionKeywordsList(paperKeywordList,projectKeywordList)
    expertKeywords = unionKeywordsList(expertKeywords,patentKeywordList)
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
    #init()#初始化，连接数据库
    expertIdList = getExpertIdList()
    for expertId in expertIdList:
        updateExpertKeywordsByExpertId(expertId)


#获取论文id列表
def get_paper_id_list():
    id_list = []
    resultList = mssql.ExecQuery("select UID from Paper")
    for result in resultList:
        id_list.append(result[0])
    return id_list

def update_paper_keyword_by_paper_uid(uid):
    paperText = getPaperTextByPaperUid(uid)
    # 可能有UID不存在的情况，返回空串
    if paperText == "":
        keywordList1 = []
    else:
        keywordList1 = extractKeywordsFromText(paperText)  # 从paperText中抽取
    keywordList2 = getPaperKeywordListByPaperUid(uid)  # paper自带的keywords
    keywordList = unionKeywordsList(keywordList1, keywordList2)
    keywordSet = set(keywordList)
    keywordList = list(keywordSet)
    #keyword_dict = getKeywordDictByList(keywordList)
    keywordStr = json.dumps(keywordList, ensure_ascii=False)
    mssql.ExecNonQuery("update Paper set keywords = '%s' where UID = '%s'" % (keywordStr, uid))

def update_all_paper_keyword():
    paper_id_list = get_paper_id_list()
    for paper_id in paper_id_list:
        update_paper_keyword_by_paper_uid(paper_id)

def get_patent_id_list():
    id_list = []
    resultList = mssql.ExecQuery("select id from Patent")
    for result in resultList:
        id_list.append(result[0])
    return id_list

def update_patent_keyword_by_patent_id(id):
    patent_text = get_patent_text_by_patent_id(id)
    # 可能有UID不存在的情况，返回空串
    if patent_text == "":
        keywordList = []
    else:
        keywordList = extractKeywordsFromText(patent_text)  # 从paperText中抽取
    keywordSet = set(keywordList)
    keywordList = list(keywordSet)
    #keyword_dict = getKeywordDictByList(keywordList)
    keywordStr = json.dumps(keywordList, ensure_ascii=False)
    mssql.ExecNonQuery("update Patent set keywords = '%s' where id = %d" % (keywordStr, id))

def update_all_patent_keyword():
    patent_id_list = get_patent_id_list()
    for patent_id in patent_id_list:
        update_patent_keyword_by_patent_id(patent_id)

def get_project_id_list():
    id_list = []
    resultList = mssql.ExecQuery("select id from Project")
    for result in resultList:
        id_list.append(result[0])
    return id_list

def update_project_keyword_by_project_id(id):
    project_text = getProjectTextByProjectId(id)
    # 可能有UID不存在的情况，返回空串
    if project_text == "":
        keywordList = []
    else:
        keywordList = extractKeywordsFromText(project_text)  # 从paperText中抽取
    keywordSet = set(keywordList)
    keywordList = list(keywordSet)
    #keyword_dict = getKeywordDictByList(keywordList)
    keywordStr = json.dumps(keywordList, ensure_ascii=False)
    mssql.ExecNonQuery("update Project set keywords = '%s' where id = %d" % (keywordStr, id))

def update_all_project_keyword():
    project_id_list = get_project_id_list()
    for project_id in project_id_list:
        update_patent_keyword_by_patent_id(project_id)
#更新三个表的关键词列
def update_database_tables_keywords():
    update_all_paper_keyword()
    update_all_patent_keyword()
    update_all_project_keyword()

if __name__=='__main__':
    init()
    update_database_tables_keywords()
    getKeywordsToExpert()




