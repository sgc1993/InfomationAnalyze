import gensim

def trainWordVec(sentences,min_count = 2):
    model = gensim.models.Word2Vec(sentences, min_count=min_count)
    model.save('file\\word2vecModel')

def updateWordVec(more_sentences):
    model = gensim.models.Word2Vec.load('file\\word2vecModel')
    model.train(more_sentences)
    model.save('file\\word2vecModel')

def getWordVecFromModel(word):
    model = gensim.models.Word2Vec.load('file\\word2vecModel')
    return model[word]

def getTrainDataToSentences():
    return

if __name__=='__main__':
    print(getWordVecFromModel("文本"))