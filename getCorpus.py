import DataBase
import json
import jieba
jieba.load_userdict("file\\jiebadict.txt")#加载用户自定义词典


#从数据库中取出机构名字分词处理
def getNameSegListFromDatabase():
    mssql = DataBase.MSSQL('localhost', 'STIMSTEST', 'sa', '1q2w3e4r5t!')

    file = open("file\\institutionNameSegList.dat", "w+", encoding='UTF-8')

    try:
        results = mssql.ExecQuery("select name from EnterpriseInfo")
        nameList = []
        for result in results:
            sentence = list(jieba.cut(result[0], cut_all=False))
            str = ' '.join(sentence)
            file.write(str + '\n')
    finally:
        file.close()
#从一期文件中追加更多机构名分词信息
def appendNameSegListFromFile():
    file = open("file\\institutionNameSegList.dat", "a", encoding='UTF-8')
    file2 = open("file\\institutionInfo.dat", encoding='UTF-8')
    try:
        lines = file2.readlines()
        for line in lines:
            institutionInfo = json.loads(line)
            str = ' '.join(institutionInfo["namewordlist"])
            file.write(str + '\n')
    finally:
        file.close()
        file2.close()

