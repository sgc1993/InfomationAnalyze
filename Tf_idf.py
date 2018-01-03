import jieba
import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
import json
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
"""
tfidf 模型，输入语料格式为一堆文本的list,其中文本为分词后的词串空格间隔
得到的是所有不重复的词语列表，并用每个词语在该文本中的tfidf值作为向量维度值表示一个文本的特征向量
"""
#获取机构名称的分词的 列表，作为Tfidf模型的训练语料
def getCorpusFromFile():
    corpus = []
    file = open("file\\dict_data5.dat",encoding='UTF-8')
    lines = file.readlines()
    for line in lines:
        line = json.loads(line)
        nameseg = ' '.join(line["namewordlist"])
        corpus.append(nameseg)
    return corpus

#获得每个文本对应的Tfidf特征向量表达
def getTfidfForName():
    corpus = getCorpusFromFile()
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值

    tfidf = transformer.fit_transform(
    vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    # print(len(word))3403
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    resultFile = open("file\\tfidfVecForEveryName.dat", 'w+', encoding='UTF-8')
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            resultFile.write(str(weight[i][j]) + ' ')
        resultFile.write('\n')

#根据名字文本获得其对应的特征向量表达
def getTfidfByName(name):
    file = open("file\\dict_data5.dat", encoding='UTF-8')
    lines = file.readlines()
    number = 0
    have = False#标志查询名字是否在表中存在
    for line in lines:
        line = json.loads(line)
        if line["name"] == name:
            have = True
            break
        number = number + 1
    if have == False:
        return []
    file = open("file\\tfidfVecForEveryName.dat", encoding='UTF-8')
    lines = file.readlines()
    line = lines[number]
    list = line.split("\n")[0].strip().split(" ")
    return list

if __name__ == "__main__":
    corpus = getCorpusFromFile()
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值

    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    # print(len(word))3403
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    print('Start Kmeans:')
    from sklearn.cluster import KMeans

    clf = KMeans(n_clusters=1000)
    s = clf.fit(weight)

    # 20个中心点
    print(clf.cluster_centers_)

    # 每个样本所属的簇
    print(clf.labels_)
    i = 1
    labeliddict = {}
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        if labeliddict.__contains__(clf.labels_[i - 1]):
            labeliddict[clf.labels_[i - 1]].add(i)
        else:
            labeliddict[clf.labels_[i - 1]] = set()
            labeliddict[clf.labels_[i - 1]].add(i)
        i = i + 1

    resultFile = open("file\\kmeansLabel.dat", 'w+', encoding='UTF-8')
    file = open("file\\dict_data5.dat", encoding='UTF-8')
    lines = file.readlines()
    for key in labeliddict.keys():
        resultFile.write(str(key)+'\n')
        nameList = []
        for id in labeliddict[key]:
            namejson = json.loads(lines[id-1])
            name = namejson["name"]
            nameList.append(name)
        nameListStr = json.dumps(nameList,ensure_ascii=False)
        resultFile.write(nameListStr+'\n')

        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print(clf.inertia_)


