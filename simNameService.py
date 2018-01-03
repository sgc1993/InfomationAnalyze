import DataBase
import distanceTest
from flask import Flask,request
from flask import jsonify
import json
import re
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name')
    nameList = getSimNameList(name)#直接和enterpriseInfo中的机构名称进行对比
    #return jsonify(nameList)
    responseStr = ""
    for name in nameList:
        responseStr = responseStr + name + '</br>'
    return responseStr

#不用分块，直接全部计算匹配
def getSimNameList(name):
    """
    :param name: 请求查询相似机构的机构名
    :return: 返回一个字典字符串
    """
    nameList = getNameListFromDB()
    arith = distanceTest.arithmetic()
    th = distanceTest.TopKHeap(5)
    nameDict = {}
    for name2 in nameList:
        if (name == name2):
            continue
        th.push((-arith.levenshtein(name, name2) / len(name2), name2))
    resultList = []
    for line in th.topk():
        resultList.append(line[1])
    return resultList

def getNameListFromDB():
    """
    :return: 从数据库中获取所有科研机构名称到内存
    """
    mssql = DataBase.MSSQL('localhost', 'STIMSTEST', 'sa', '1q2w3e4r5t!')
    list = mssql.ExecQuery("select name from EnterpriseInfo")
    namelist = []
    for i in list:
        namelist.append(i[0])
    return namelist

def getNameLocationListFromDB():
    """
    :return: 从数据库中获取机构名称和所在地元组列表[(,),(,)]
    """
    mssql = DataBase.MSSQL('localhost', 'STIMSTEST', 'sa', '1q2w3e4r5t!')
    list = mssql.ExecQuery("select name,location from institution")
    namelocationlist = []
    for i in list:
        namelocationlist.append(i)
    return namelocationlist#('龙迅半导体科技有限公司', '合肥')

def getLocationByName(name):
    """
    :param name: 从请求传来的机构名称
    :return: 根据机构名称从数据库中获取机构名称和对应地址，list[('黑龙江科技学院', '哈尔滨')]
    """
    mssql = DataBase.MSSQL('localhost', 'STIMSTEST', 'sa', '1q2w3e4r5t!')
    list = mssql.ExecQuery("select name,location from institution where name = '%s'"%name)
    return list[0]

#按所在地进行分块匹配
def getSimNameByCity(nameLocation):
    """
    :param nameLocation: 请求传来的需要查找相似名称机构的机构名称和对应地址
    :return: 返回相似名称的机构名称数组，5个：TopKHeap(5)['黑龙江省科学院高技术研究院', '东北林业大学', '黑龙江大学电子工程学院', '黑龙江省石油化学研究院', '黑龙江大学']
    """
    arith = distanceTest.arithmetic()
    th = distanceTest.TopKHeap(5)
    nameLocationList = getNameLocationListFromDB()
    for nameLocation2 in nameLocationList:
        if (nameLocation[0] == nameLocation2[0]):
            continue
        if (nameLocation[1] != nameLocation2[1]):
            continue
        l1 = re.findall(r"\d+\.?\d*", nameLocation[0])
        l2 = re.findall(r"\d+\.?\d*", nameLocation2[0])
        if (len(l1) > 0 and len(l2) > 0):
            if (l1[-1] != l2[-1]):
                continue
        th.push((-arith.levenshtein(nameLocation[0], nameLocation2[0]), nameLocation2[0]))
    nameList = []
    for line in th.topk():
        nameList.append(line[1])
    return nameList
if __name__ == '__main__':
    app.run()


