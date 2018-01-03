from entity.entity import Institution,Expert
from dataimpl.Database import MSSQL,Neo4j


class InstitutionImpl():

    def __init__(self):
        self.mssql = MSSQL()

    def impl_institution_entity(self,institution_id):
        name = self.get_name(institution_id)
        location = self.get_location(institution_id)
        keywords = self.get_keywords(institution_id)
        workers = self.workers(institution_id)
        cooperate_institutions = self.cooperate_institutions(institution_id)
        return Institution(name,location,keywords,workers,cooperate_institutions)

    def get_name(self,id):
        pass
    def get_location(self,id):
        pass
    def get_keywords(self,id):
        pass
    def get_workers(self,id):
        pass
    def get_cooperate_institutions(self,id):
        pass

class ExpertImpl():

    def __init__(self):
        self.mssql = MSSQL()

    def impl_expert_entity(self,expert_id):
        name = self.get_name(expert_id)
        keywords = self.get_keywords(expert_id)
        cooperate_experts = self.cooperate_experts(expert_id)
        return Expert(name,keywords,cooperate_experts)

    def get_name(self,id):
        pass
    def get_keywords(self,id):
        pass
    def get_cooperate_experts(self,id):
        pass