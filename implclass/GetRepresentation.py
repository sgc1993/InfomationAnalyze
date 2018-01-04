from abc import ABCMeta, abstractmethod
import json
import jieba
from gensim import corpora, models,similarities
from gensim.models import LdaModel

class GetRepresentation():
    __metaclass__ = ABCMeta
    def __init__(self):
        return

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def get(self):
        pass


class GetLdaRepresentation(GetRepresentation):

    def __init__(self):
        return


    def train(self):
        trainData = self.getTrainData()
        dict = corpora.Dictionary(trainData)  # 自建词典
        dict.save("../file/institutionNameLDA.dict")
        # 通过dict将用字符串表示的文档转换为用id表示的文档向量
        # print(dict.token2id)字典中id和单词映射
        corpus = [dict.doc2bow(text) for text in trainData]
        corpora.MmCorpus.serialize('../file/institutionNameLDAcorpus.mm', corpus)  # 存入硬盘，以备后需
        lda = LdaModel(corpus=corpus, id2word=dict, num_topics=30, per_word_topics=True)
        lda.save('../file/institutionNameLDA.model')


    def get(self):
        pass

    def getTrainData(self):
        file = open("../file/institutionNameSegList.dat", encoding='UTF-8')
        trainData = []
        lines = file.readlines()
        for line in lines:
            trainData.append(line.strip().split())
        return  trainData


class GetLsiRepresentation(GetRepresentation):

    def __init__(self):
        return


    def train(self):
        pass


    def get(self):
        pass


class GetWord2VecRepresentation(GetRepresentation):

    def __init__(self):
        return


    def train(self):
        pass


    def get(self):
        pass


class GetKeywordRepresentation(GetRepresentation):

    def __init__(self):
        return


    def train(self):
        pass


    def get(self):
        pass

def getRepresentation(institution,algorithm,dim):
    return

def test():
    file = open("../file/institutionNameSegList.dat", encoding='UTF-8')
    trainData = []
    lines = file.readlines()
    for line in lines:
        trainData.append(line.strip().split())
    dict = corpora.Dictionary(trainData)  # 自建词典
    dict.save("../file/institutionNameLDA.dict")
    # 通过dict将用字符串表示的文档转换为用id表示的文档向量
    # print(dict.token2id)字典中id和单词映射
    corpus = [dict.doc2bow(text) for text in trainData]
    corpora.MmCorpus.serialize('../file/institutionNameLDAcorpus.mm', corpus)  # 存入硬盘，以备后需
    lda = LdaModel(corpus=corpus, id2word=dict, num_topics=30, per_word_topics=True)
    lda.save('../file/institutionNameLDA.model')
    lda = models.ldamodel.LdaModel.load('../file/institutionNameLDA.model')
    dictionary = corpora.Dictionary.load('../file/institutionNameLDA.dict')
    corpus = corpora.MmCorpus('../file/institutionNameLDAcorpus.mm')

    test_doc = list("电子科技 集团 58 所".split())  # 新文档进行分词
    doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
    doc_lda = lda[doc_bow]
    print(lda.print_topics(3))
    print(doc_lda)
    # print(doc_lda)
    # for a in doc_lda:
    #     print(a)


test()