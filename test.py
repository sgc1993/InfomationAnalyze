import DataBase
import jieba.analyse
import json
import re
import gensim
from gensim import corpora, models
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import numpy as np
#从paper_clean中抽取摘要，简单处理
def getAbstract(fromFilePath,toFilePath):
    file = open(fromFilePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    lines = file.readlines()
    try:
        for line in lines:
            paperJson = json.loads(line)
            if ('Chinese' in paperJson["abstract"].keys()) and (paperJson["abstract"]["Chinese"] != ""):
                paperJson["abstract"]["Chinese"] = re.sub(r'\n',"",paperJson["abstract"]["Chinese"])#去除里边包含的换行符
                paperJson["abstract"]["Chinese"] = paperJson["abstract"]["Chinese"].strip()#去掉首尾多余空格
                paperJson["abstract"]["Chinese"] = paperJson["abstract"]["Chinese"].replace(" ","")#去掉文本中间空格
                resultFile.write(paperJson["abstract"]["Chinese"]+"\n")
    finally:
        file.close()
        resultFile.close()

#将摘要文件分词
def getVocaOfAbstract(filePath,toFilePath):
    file = open(filePath, encoding='UTF-8')
    resultFile = open(toFilePath, 'w+', encoding='UTF-8')
    #sentences = []
    try:
        lines = file.readlines()
        for line in lines:
            #line = re.sub("[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，,.．;:。？、~@#￥%……&*（）]+","",line)
            sentence = list(jieba.cut(line,cut_all=False))
            str = ' '.join(sentence)
            resultFile.write(str)
    finally:
        file.close()

#用分词后的摘要文件做词典训练word2vec模型，并将模型保存
def word2VecFromVocaFile(filePath):
    file =  open(filePath,encoding='UTF-8')
    sentences = []
    try:
        lines = file.readlines()
        for line in lines:
            alist = line.split()
            sentences.append(alist)
    finally:
        file.close()
        model = gensim.models.Word2Vec(sentences, size=300, window=5, min_count=5, workers=4)
        print(model.similarity("分析", "本文"))
        model.save('file\\word2vecModel')

#加载之前训练的word2vec模型
def testModel():
    new_model = gensim.models.Word2Vec.load('file\\word2vecModel')
    print(np.shape(new_model["文本"]))#300维
    print(new_model.similarity("分析", "本文"))

#用abstract去停用词建立词典，训练LDA，并保存
def testLDA(file):
    file = open(file, encoding='UTF-8')
    train = []
    try:
        lines = file.readlines()
        stopwords = open("file\\stopwords_cn.txt", encoding='UTF-8').readlines()
        stopwords = [w.strip() for w in stopwords]
        for line in lines:
            line = line.split()
            train.append([w for w in line if w not in stopwords])
    finally:
        file.close()
        dict = corpora.Dictionary(train)#自建词典
        # 通过dict将用字符串表示的文档转换为用id表示的文档向量
        corpus = [dict.doc2bow(text) for text in train]
        lda = LdaModel(corpus=corpus, id2word=dict, num_topics=20)
        lda.print_topic(2)
        lda.save('file\\lda.model')
#加载LDA模型，并将topics存入文件,测试一个新的文本的topic分布
def loadLDA():
    lda = models.ldamodel.LdaModel.load('file\\lda.model')
    resultFile = open("file\\abstractLDA.dat", 'w+', encoding='UTF-8')
    for i in lda.print_topics(20):
        resultFile.write(i[1]+'\n')
    #0.013 * "应力" + 0.010 * "材料" + 0.010 * "载荷" + 0.010 * "断裂"
    test_doc = list("对 基于 时间 反转 镜单 水听器 被动 定位 算法 进行 了 深入研究 , 并 通过 数值 仿真 分析 了 其 被动 定位 性能 . 通过 分析 得知 基于 单 声压 水听器 的 时间 反转 镜 定位 方法 即可 准确 估计 目标 的 距离 与 深度 , 相比 传统 组阵 定位 算法 有着 明显 的 优势 . 同时 给出 了 信号 的 脉 宽 、 频宽 、 相关 处理 对 定位 结果 的 影响 . ".split()) # 新文档进行分词
    doc_bow = lda.id2word.doc2bow(test_doc)  # 文档转换成bow
    doc_lda = lda[doc_bow]  # 得到新文档的主题分布
    # 输出新文档的主题分布
    for topic in doc_lda:
        print("%s\t%f\n" % (lda.print_topic(topic[0]), topic[1]))



if __name__ == '__main__':
    # mssql = DataBase.MSSQL('localhost','STIMSTEST','sa','1q2w3e4r5t!')
    # rows = mssql.ExecQuery("select id,country from Address")
    # for row in rows:
    #     print(row.id)

    #getAbstract("file\\paper_clean.dat","file\\abstract.dat")
    #test()
    #getVocaOfAbstract("file\\abstract.dat","file\\abstractseg.dat")
    #word2VecFromVocaFile("file\\abstractseg.dat")
    #testModel()
    #testLDA("file\\abstractseg.dat")

    testModel()

    #loadLDA()
