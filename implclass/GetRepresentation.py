from abc import ABCMeta, abstractmethod

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
        pass


    def get(self):
        pass

    def getCorpus(self):

        pass


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