import os
from abc import ABCMeta, abstractmethod
import jieba
import gensim
from gensim import corpora, models,similarities
from gensim.models import LdaModel
import pickle as pkl
sep = os.path.sep
jieba.load_userdict("..%sfile%sjiebadict.txt"%(sep,sep))


class Representation(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def get_vector(self,institution_name):
        pass

    @abstractmethod
    def get_train_data(self):
        pass


class LdaRepresentation(Representation):

    dim = 20

    def __init__(self):
        Representation.__init__(self)
        #类初始化的时候就加载模型，不然每次查询的时候都要加载一次
        if os.path.exists('..%sfile%sinstitutionNameLDA.model' % (sep, sep)):#防止第一次部署时还没训练过的情况
            try:
                lda_file = open('..%sfile%sinstitutionNameLDA.model' % (sep, sep), 'rb')
                self.lda = pkl.load(lda_file)
            except EOFError:  # 捕获异常EOFError 后返回None
                print("test")
        else:
            self.train() # 第一次的话就训练一下
            return
        #存储着词和id的映射关系
        if os.path.exists('..%sfile%sinstitutionNameLDA.dict' % (sep, sep)):
            self.dictionary = corpora.Dictionary.load('..%sfile%sinstitutionNameLDA.dict' % (sep, sep))
        #将词语语料转化为id表示的语料
        if os.path.exists('..%sfile%sinstitutionNameLDAcorpus.mm' % (sep, sep)):
            self.corpus = corpora.MmCorpus('..%sfile%sinstitutionNameLDAcorpus.mm' % (sep, sep))

    def train(self):
        train_data = self.get_train_data() # 获取训练数据
        self.dictionary = corpora.Dictionary(train_data)  # 自建词典
        self.dictionary.save("..%sfile%sinstitutionNameLDA.dict"%(sep,sep))
        # 通过dict将用字符串表示的文档转换为用id表示的文档向量
        # print(dict.token2id)字典中id和单词映射
        self.corpus = [self.dictionary.doc2bow(text) for text in train_data]
        corpora.MmCorpus.serialize('..%sfile%sinstitutionNameLDAcorpus.mm'%(sep,sep), self.corpus)  # 存入硬盘，以备后需
        self.lda = LdaModel(corpus=self.corpus, id2word=self.dictionary,
                            num_topics=LdaRepresentation.dim, minimum_probability=1e-8)
        #第三方包序列化模型
        lda_file = open('..%sfile%sinstitutionNameLDA.model' % (sep, sep), 'wb')
        pkl._dump(self.lda, lda_file)
        lda_file.close()

    def get_vector(self, institution_name):
        institution_name_seg = list(jieba.cut(institution_name,cut_all=False)) # 新文档进行分词
        doc_bow = self.dictionary.doc2bow(institution_name_seg)  # 文档转换成bow
        doc_lda = self.lda[doc_bow]
        vector = []
        for dim in doc_lda:
            vector.append(dim[1])
        return vector

    def get_train_data(self):
        file = open("..%sfile%sinstitutionNameSegList.dat"%(sep,sep), encoding='UTF-8')
        train_data = []
        lines = file.readlines()
        for line in lines:
            train_data.append(line.strip().split())
        return  train_data


class LsiRepresentation(Representation):

    dim = 20

    def __init__(self):
        Representation.__init__(self)
        if os.path.exists('..%sfile%sinstitutionNameLSI.model' % (sep, sep)):#防止第一次部署时还没训练过的情况
            try:
                lsi_file = open('..%sfile%sinstitutionNameLDA.model' % (sep, sep), 'rb')
                self.lsi = pkl.load(lsi_file)
            except EOFError:  # 捕获异常EOFError 后返回None
                print("test")
        else:
            self.train()
            return

        if os.path.exists('..%sfile%sinstitutionNameLSI.dict' % (sep, sep)):
            self.dictionary = corpora.Dictionary.load('..%sfile%sinstitutionNameLSI.dict' % (sep, sep))

        if os.path.exists('..%sfile%sinstitutionNameLSIcorpus.mm' % (sep, sep)):
            self.corpus = corpora.MmCorpus('..%sfile%sinstitutionNameLSIcorpus.mm' % (sep, sep))

    def train(self):
        train_data = self.get_train_data()
        self.dictionary = corpora.Dictionary(train_data)
        self.dictionary.save("..%sfile%sinstitutionNameLSI.dict" % (sep, sep))
        self.corpus = [self.dictionary.doc2bow(text) for text in train_data]
        corpora.MmCorpus.serialize('..%sfile%sinstitutionNameLSIcorpus.mm' % (sep, sep), self.corpus)
        self.lsi = models.LsiModel(corpus=self.corpus, id2word=self.dictionary, num_topics=LsiRepresentation.dim)
        #用第三方包序列化模型
        lsi_file = open('..%sfile%sinstitutionNameLSI.model' % (sep, sep),'wb')
        pkl._dump(self.lsi,lsi_file)
        lsi_file.close()

    def get_vector(self, institution_name):
        institution_name_seg = list(jieba.cut(institution_name, cut_all=False))  # 新文档进行分词
        doc_bow = self.dictionary.doc2bow(institution_name_seg)  # 文档转换成bow
        doc_lsi = self.lsi[doc_bow]
        vector = []
        for dim in doc_lsi:
            vector.append(dim[1])
        return vector

    def get_train_data(self):
        file = open("..%sfile%sinstitutionNameSegList.dat"%(sep,sep), encoding='UTF-8')
        train_data = []
        lines = file.readlines()
        for line in lines:
            train_data.append(line.strip().split())
        return  train_data


class Word2VecRepresentation(Representation):

    dim = 200

    def __init__(self):
        Representation.__init__(self)

    def train(self):
        train_data = self.get_train_data()
        model = gensim.models.Word2Vec(train_data, size=Word2VecRepresentation.dim, window=5, min_count=2)
        model.save('..%sfile%sword2vecModel'%(sep,sep))

    def get_vector(self, institution_name):
        institution_name_seg = list(jieba.cut(institution_name, cut_all=False))
        model = gensim.models.Word2Vec.load('..%sfile%sword2vecModel'%(sep,sep))
        for word in institution_name_seg:
            word_vector = list(model[word])
        vector = list(model[institution_name_seg[0]])
        return vector

    def get_train_data(self):
        file = open("..%sfile%sinstitutionNameSegList.dat" % (sep, sep), encoding='UTF-8')
        train_data = []
        lines = file.readlines()
        for line in lines:
            train_data.append(line.strip().split())
        return train_data


class KeywordRepresentation(Representation):

    def __init__(self, dim):
        Representation.__init__(self)
        self.dim = dim

    def train(self):
        pass

    def get_vector(self,institution_name):
        pass

    def get_train_data(self):
        pass


class GetRepresentation(object):

    def __init__(self, algorithm, dim):
        representations = dict(Lda=LdaRepresentation, Lsi=LsiRepresentation,
                               Word2Vec=Word2VecRepresentation, Keyword=KeywordRepresentation)
        self.representation = representations[algorithm]()
        if dim != representations[algorithm].dim:
            representations[algorithm].dim = dim
            self.train()

    def train(self):
        self.representation.train()

    def get_vector_by_name(self, institution_name):
        return self.representation.get_vector(institution_name)


def test_lda():
    file = open("..%sfile%sinstitutionNameSegList.dat"%(sep,sep), encoding='UTF-8')
    trainData = []
    lines = file.readlines()
    for line in lines:
        trainData.append(line.strip().split())
    dict = corpora.Dictionary(trainData)  # 自建词典
    dict.save("..%sfile%sinstitutionNameLDA.dict"%(sep,sep))
    # 通过dict将用字符串表示的文档转换为用id表示的文档向量
    # print(dict.token2id)字典中id和单词映射
    corpus = [dict.doc2bow(text) for text in trainData]
    corpora.MmCorpus.serialize('..%sfile%sinstitutionNameLDAcorpus.mm'%(sep,sep), corpus)  # 存入硬盘，以备后需
    lda = LdaModel(corpus=corpus, id2word=dict, num_topics=30, minimum_probability=1e-9)
    lda.save('..%sfile%sinstitutionNameLDA.model'%(sep,sep))
    lda = models.ldamodel.LdaModel.load('..%sfile%sinstitutionNameLDA.model'%(sep,sep))
    dictionary = corpora.Dictionary.load('..%sfile%sinstitutionNameLDA.dict'%(sep,sep))
    corpus = corpora.MmCorpus('..%sfile%sinstitutionNameLDAcorpus.mm'%(sep,sep))

    test_doc = list("电子科技 集团 58 所".split())  # 新文档进行分词
    doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
    doc_lda = lda[doc_bow]
    print(lda.print_topics(3))
    print(doc_lda)
    # print(doc_lda)
    # for a in doc_lda:
    #     print(a)
    lda = GetLdaRepresentation()
    vec = lda.get_vector("电子科技集团11所")
    for v in vec:
        print(v)


def update_train_data():
    pass


a = GetRepresentation("Lsi",20)
v = a.get_vector_by_name("杭州电子科技大学")
for i in v:
    print(i)
