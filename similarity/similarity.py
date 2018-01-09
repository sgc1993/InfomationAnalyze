from abc import ABCMeta, abstractmethod

class Similarity(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def compute_similarity(self,institution_A,institution_B):
        pass

#向量相似度
class vectorSimilarity(Similarity):

    def __init__(self):
        Similarity.__init__(self)
        pass
    #计算两个机构的相似度
    def compute_similarity(self,institution_A,institution_B):
        name_similarity = self.compute_name_similarity(institution_A,institution_B)
        research_areas_similarity = self.compute_research_areas_similarity(institution_A,institution_B)
        return name_similarity + research_areas_similarity
    #计算机构名称的相似度
    def compute_name_similarity(self,institution_A,institution_B):
        pass
    #计算机构研究领域的相似度
    def compute_research_areas_similarity(self,institution_A,institution_B):
        pass

#社交相似度
class socialSimilarity(Similarity):

    def __init__(self):
        Similarity.__init__(self)
    #计算两个机构的相似度
    def compute_similarity(self,institution_A,institution_B):
        return self.compute_social_similarity(institution_A, institution_B)
    #计算两个机构的社交关系相似度
    def compute_social_similarity(self,institution_A,institution_B):
        pass

