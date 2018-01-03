import json
import jieba
from gensim import corpora, models,similarities
from gensim.models import LdaModel

def getNameSegList(fromFile,toFile):
    file = open(fromFile,encoding='UTF-8')
    resultFile = open(toFile, 'w+', encoding='UTF-8')
    try:
        institutionStrs = file.readlines()
        for institutionStr in institutionStrs:
            institutionJosn = json.loads(institutionStr)
            resultFile.write(' '.join(institutionJosn["namewordlist"])+'\n')
    finally:
        file.close()
        resultFile.close()

def testLDA(file):
    file = open(file, encoding='UTF-8')
    train = []
    try:
        lines = file.readlines()
        for line in lines:
            line = line.split()
            train.append(line)
    finally:
        file.close()
        dict = corpora.Dictionary(train)#自建词典
        dict.save("file\\institutionNameLDA.dict")
        # 通过dict将用字符串表示的文档转换为用id表示的文档向量
        #print(dict.token2id)字典中id和单词映射
        corpus = [dict.doc2bow(text) for text in train]
        corpora.MmCorpus.serialize('file\\institutionNameLDAcorpus.mm', corpus)  # 存入硬盘，以备后需
        lda = LdaModel(corpus=corpus, id2word=dict, num_topics=30)
        lda.save('file\\institutionNameLDA.model')

def queryForLDA():
    file = open("file\\nameseglist.dat", encoding='UTF-8')
    try:
        lines = file.readlines()
    finally:
        file.close()
    lda = models.ldamodel.LdaModel.load('file\\institutionNameLDA.model')
    dictionary = corpora.Dictionary.load('file\\institutionNameLDA.dict')
    corpus = corpora.MmCorpus('file\\institutionNameLDAcorpus.mm')
    index = similarities.MatrixSimilarity(lda[corpus])  ## transform corpus to LDA space and index it
    test_doc = list("电子科技 集团 58 所".split())  # 新文档进行分词
    doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
    doc_lda = lda[doc_bow]  # 得到新文档的主题分布
    sims = index[doc_lda]
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for i in sort_sims:
        print(lines[i[0]])
        #print(''.join(train[i[0]]))

def loadLDA():
    lda = models.ldamodel.LdaModel.load('file\\institutionNameLDA.model')
    # resultFile = open("file\\institutionNameLDA.dat", 'w+', encoding='UTF-8')
    # for i in lda.print_topics(100):
    #     resultFile.write(i[1]+'\n')
    # 输出新文档的主题分布
    # for topic in doc_lda:
    #     print("%s\t%f\n" % (lda.print_topic(topic[0]), topic[1]))

def testLSI(file):
    file = open(file, encoding='UTF-8')
    train = []
    try:
        lines = file.readlines()
        for line in lines:
            line = line.split()
            train.append(line)
    finally:
        file.close()
        dict = corpora.Dictionary(train)  # 自建词典
        # 通过dict将用字符串表示的文档转换为用id表示的文档向量
        corpus = [dict.doc2bow(text) for text in train]#每个id对应的词在本文档中的次数表示的文档，list(list)
        # for doc in corpus[0:2]:
        #     print(doc)
        #     [(0, 1), (1, 1), (2, 1), (3, 1)]
        #     [(4, 1), (5, 1), (6, 1), (7, 1), (8, 1)]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]#每个id对应的词的TFIDF值表示的文档，list(list)
        # for doc in corpus_tfidf[0:2]:
        #     print(doc)
        #     [(0, 0.7432576787962963), (1, 0.568443392833714), (2, 0.28944547044090296), (3, 0.2016468489594658)]
        #     [(4, 0.4704465054268491), (5, 0.5104671481345072), (6, 0.4175420934561469), (7, 0.43042586271919103),
        #      (8, 0.39811499984525456)]
        #print(tfidf.dfs)每个id对应的dfs
        #print(tfidf.idfs)每个id对应的idfs
        lsi = models.LsiModel(corpus_tfidf, id2word=dict, num_topics=5)
        corpus_lsi = lsi[corpus_tfidf]
        # for doc in corpus_lsi:
        #     print(doc)[(0, 0.44797692152874452), (1, 0.022280361032730511), (2, -0.21099138409389981), (3, -0.15538849559731538), (4, 0.055983208068151762)]
        index = similarities.MatrixSimilarity(lsi[corpus])

        # query = "黑龙江省 科学院 高技术 研究院"
        # query_bow = dict.doc2bow(query.split())
        # query_lsi = lsi[query_bow]
        # sims = index[query_lsi]
        # for i in list(enumerate(sims)):
        #     print(i)
if __name__ == '__main__':
    #getNameSegList("file\\dict_data5.dat","file\\nameseglist.dat")
    #testLDA("file\\nameseglist.dat")
    #loadLDA()
    #testLSI("file\\nameseglist.dat")
    queryForLDA()