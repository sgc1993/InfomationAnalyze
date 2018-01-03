# -*- coding: UTF-8 -*-# -*- coding: UTF-8 -*-
import json
import jieba
#获取最初的机构信息{"name": "电子科技集团58所", "location": "无锡"}
def getInitInstitutionInformations(fromFilePath,toFilePath):
    file = open(fromFilePath,encoding='UTF-8')
    resultFile = open(toFilePath,'w+',encoding='UTF-8')
    try:
        text = file.readlines()
        for line in text:  # 因为text是个List
            jsonText = json.loads(line)  # 将文件中的数据解析出来成为dict数据类型，存储为Unicode形式
            temp_dict = jsonText['institutions']  # 获得institutions对应的dict
            # { "电子科技集团54所" : "石家庄", "西安电子科技大学电子工程学院" : "西安" }
            for key, value in temp_dict.items():
                write_dict = dict()
                if (value == None):
                    write_dict["name"] = key
                    write_dict["location"] = "NoneCity"
                    write_dict["num"] = 1
                    json_dict = json.dumps(write_dict,ensure_ascii=False)#使用ensure这个属性就得每一个都encode
                    resultFile.write(json_dict+"\n")
                    continue
                write_dict["name"] = key
                write_dict["location"] = value
                write_dict["num"] = 1
                json_dict = json.dumps(write_dict,ensure_ascii=False)  # 使用ensure这个属性就得每一个都encode
                resultFile.write(json_dict+"\n")
    finally:
        file.close()
        resultFile.close()

# 对institutions信息进行排序,即按name和location两个字段排
def fileSort(fromFilePath, toFilePath):
    file = open(fromFilePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    try:
        institutionList = file.readlines()
        institutionList.sort()
        for line in institutionList:
            resultFile.write(line)
    finally:
        file.close()

#对机构信息按机构名排序
def sortByInstitutionNameAndNum(filePath,toFilePath):
    file = open(filePath,encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    try:
        instituionsStrList = file.readlines()
        institutionsDictList = list()
        for instituionsStr in instituionsStrList:#将字符串数组导成dict数组
            instituionsDict = json.loads(instituionsStr)
            institutionsDictList.append(instituionsDict)
        institutionsDictList.sort(key=lambda x:(x["name"],x["num"]), reverse=True)#对dict数组按照指定dict排序方式排序
        for institutionDict in institutionsDictList:
            json_dict = json.dumps(institutionDict, ensure_ascii=False)#把dict数组每个dict转化为字符串存入文件
            resultFile.write(json_dict + "\n")
    finally:
        file.close()
        resultFile.close()

#按机构名字和location做主键进行统计
def nameFrequencyStatistics(fromFilePath, toFilePath):
    file = open(fromFilePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    try:
        # ①先把数据读出来，放进一个list[dict]之中
        institutionStrList = file.readlines()
        institutionDictList = list()
        for institutionStr in institutionStrList:
            institutionDict = json.loads(institutionStr)
            institutionDictList.append(institutionDict)
        # ②创建一个新的list[dict]用存放统计后的dict
        newinstitutionDictList = list()
        # ③一个preDict用于记录上一个读出的dict,num用于记录出现次数
        preDict = institutionDictList[0]
        num = 1
        for institutionDict in institutionDictList[1:]:
            if (institutionDict == institutionDictList[-1]):  # list中最后一个字典情况单独处理，因为如果最后一个Dict跟preDict一样的话num+1不记录会漏掉
                if (institutionDict["name"] == preDict["name"] and institutionDict["location"] == preDict["location"]):
                    num = num + 1
                    preDict["num"] = num
                    newinstitutionDictList.append(preDict)
                if (institutionDict["name"] != preDict["name"] or institutionDict["location"] != preDict["location"]):
                    preDict["num"] = num
                    newinstitutionDictList.append(preDict)
                    newinstitutionDictList.append(institutionDict)
            if (institutionDict["name"] != preDict["name"] or institutionDict["location"] != preDict["location"]):
                preDict["num"] = num
                newinstitutionDictList.append(preDict)
                preDict = institutionDict
                num = 1
                continue
            if (institutionDict["name"] == preDict["name"] and institutionDict["location"] == preDict["location"]):
                num = num + 1
                continue
        # newinstitutionDictList统计好了频率
        # return newinstitutionDictList

        # 把新的list[dict]编码后写进文件
        for institutionDict in newinstitutionDictList:
            json_dict = json.dumps(institutionDict, ensure_ascii=False)
            resultFile.write(json_dict + "\n")
    finally:
        file.close()
        resultFile.close()

#用同名已知location的机构填充NoneCity将location按照词条数最多的同名机构的location填充 ，相当于去融合了同name不同location的实体
def paddingLocation(fromFilePath, toFilePath):
    file = open(fromFilePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    try:
        institutionStrList = file.readlines()
        institutionDictList = list()
        for institutionStr in institutionStrList:
            institutionDict = json.loads(institutionStr)
            institutionDictList.append(institutionDict)
        institutionDictList.sort(key=lambda x:(x["name"],x["num"]), reverse=True)#将字典按照name和num两个字段排序
        # 进行缺失值填充，同名机构按照最大的数目的location进行更改
        preDict = institutionDictList[0]
        for institutionDict in institutionDictList[1:]:
            if (institutionDict["name"] != preDict["name"]):
                preDict = institutionDict
            elif (institutionDict["name"] == preDict["name"]):
                if (institutionDict["num"] <= preDict["num"]):
                    if (preDict["location"] == "NoneCity"):
                        preDict["location"] = institutionDict["location"]
                    institutionDict["location"] = preDict["location"]
                elif (institutionDict["num"] > preDict["num"]):
                    preDict["location"] = institutionDict["location"]
        # 把新的list[dict]编码后写进文件
        for institutionDict in institutionDictList:
            json_dict = json.dumps(institutionDict , ensure_ascii=False)
            resultFile.write(json_dict + "\n")
    finally:
        file.close()
        resultFile.close()

def mergeTheSameNameInstitution(fromFilePath, toFilePath):
    file = open(fromFilePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    try:
        # ①先把数据读出来，放进一个list[dict]之中
        institutionStrList = file.readlines()
        institutionDictList = list()
        for institutionStr in institutionStrList:
            institutionDict = json.loads(institutionStr)
            institutionDictList.append(institutionDict)
        # ②创建一个新的list[dict]用存放统计后的dict
        newinstitutionDictList = list()
        # ③一个preDict用于记录上一个读出的dict,num用于记录出现次数
        preDict = institutionDictList[0]
        num = 1
        for institutionDict in institutionDictList[1:]:
            if (institutionDict == institutionDictList[
                -1]):  # list中最后一个字典情况单独处理，因为如果最后一个Dict跟preDict一样的话num+1不记录会漏掉
                if (institutionDict["name"] == preDict["name"] and institutionDict["location"] == preDict[
                    "location"]):
                    num = institutionDict["num"] + preDict["num"]
                    preDict["num"] = num
                    newinstitutionDictList.append(preDict)
                if (institutionDict["name"] != preDict["name"] or institutionDict["location"] != preDict[
                    "location"]):
                    preDict["num"] = num
                    newinstitutionDictList.append(preDict)
                    newinstitutionDictList.append(institutionDict)
            if (institutionDict["name"] != preDict["name"] or institutionDict["location"] != preDict["location"]):
                preDict["num"] = num
                newinstitutionDictList.append(preDict)
                preDict = institutionDict
                num = 1
                continue
            if (institutionDict["name"] == preDict["name"] and institutionDict["location"] == preDict["location"]):
                num = institutionDict["num"] + preDict["num"]
                continue
        # newinstitutionDictList统计好了频率
        # return newinstitutionDictList

        # 把新的list[dict]编码后写进文件
        for institutionDict in newinstitutionDictList:
            json_dict = json.dumps(institutionDict, ensure_ascii=False)
            resultFile.write(json_dict + "\n")
    finally:
        file.close()
        resultFile.close()

#分词
def nameDivision(fromFilePath, toFilePath):
    file = open(fromFilePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    try:
        institutionList = file.readlines()
        for line in institutionList:
            jsonText = json.loads(line)
            """
                word_list_unicode = list(jieba.cut(jsonText["name"], cut_all = False)) unicode 刚刚解析出的数据一般都是Unicode，需要进行编码
                ' '.join(word_list_unicode).encode('utf8')字符串才可以编码，所以把他转成字符串
                .split(' ')
            """
            g = ' '.join(list(jieba.cut(jsonText["name"],cut_all=False))).split(' ')
            jsonText["namewordlist"] = g
            #write_dict = dict()
            # for key, value in jsonText.items():
            #     if(key == "name"):
            #         write_dict["name".encode('utf-8')] = value.encode('utf-8')
            #     if(key == "location"):
            #         write_dict["location".encode('utf-8')] = value.encode('utf-8')
            #write_dict["namewordlist".encode('utf-8')] = g
               # write_dict["word".encode('utf-8')] = g

            json_dict = json.dumps(jsonText, ensure_ascii=False)
            resultFile.write(json_dict + "\n")
    finally:
        file.close()
        resultFile.close()


#对机构名进行过滤处理,把整个文件读到内存中，一个josn数组，过滤后再把每个josn写入文件
def processData():
    #处理规则：70○〇Ο1 4川 9江 9洲 name完全是数字的 存在非法字符的 （）括号中的提示是否可以去掉
    return 0
if __name__ == '__main__':
    #getInitInstitutionInformations("file\\paper_clean.dat","file\\dict_data.dat")
    #fileSort("file\\dict_data.dat","file\\dict_data1.dat")
    #nameFrequencyStatistics("file\\dict_data1.dat","file\\dict_data2.dat")
    #paddingLocation("file\\dict_data2.dat","file\\dict_data3.dat")
    #mergeTheSameNameInstitution("file\\dict_data3.dat","file\\dict_data4.dat")
    nameDivision("file\\dict_data4.dat","file\\dict_data5.dat")