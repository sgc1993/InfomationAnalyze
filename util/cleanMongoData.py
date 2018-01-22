import json
import os
import util.clean
sep = os.path.sep


#根据论文link,去除重复paper
def remove_duplicate_paper_in_file():
    file = open("..%sfile%smongoFile%s36.json"%(sep,sep,sep),encoding='UTF-8')
    file2 = open("..%sfile%smongoFile%s36new.json"%(sep,sep,sep),'w+',encoding='UTF-8')
    try:
        lines = file.readlines()
        paper_json_list = []
        for line in lines:
            paper_json = json.loads(line)
            num = 0
            for else_paper_json in paper_json_list:
                if else_paper_json["link"] == paper_json["link"]:
                    break
                num = num + 1
            if num == len(paper_json_list):
                paper_json_list.append(paper_json)
        for paper_json in paper_json_list:
            file2.write(json.dumps(paper_json,ensure_ascii=False)+'\n')
    finally:
        file.close()
        file2.close()

#remove_duplicate_paper_in_file()

#获得某个机构爬取论文集合中所有不重复机构名
def get_institution_name_set_from_file(file_path):
    file = open(file_path,"r",encoding='utf-8')
    file2 = open("..%sfile%smongoFile%snames.json"%(sep,sep,sep),"w+",encoding='utf-8')
    lines = file.readlines()
    institution_names = set()
    for line in lines:
        paper_json = json.loads(line)
        for key in paper_json["institutions"].keys():
            if "电" in key and "科" in key:
                if "15" in key or "十五" in key:
                    institution_names.add(key)
    for name in institution_names:
        file2.write(name+"\n")

def get_institution_name_paper_map():
    file = open("..%sfile%smongoFile%snames.json"%(sep,sep,sep),encoding='utf-8')
    file2 = open("..%sfile%smongoFile%s15new2.json" % (sep, sep, sep), encoding='utf-8')
    file3 = open("..%sfile%smongoFile%sname_paper_map.json"%(sep,sep,sep),'w+',encoding='utf-8')
    papers = file2.readlines()
    names = file.readlines()
    for name in names:
        name = name.strip()
        name_paper_map = {}
        name_paper_map["institution"] = name
        paper_set = set()
        for paper in papers:
            paper = json.loads(paper)
            if name in paper["institutions"].keys():
                paper_set.add(paper["link"])
        name_paper_map["papers"] = list(paper_set)
        file3.write(json.dumps(name_paper_map,ensure_ascii=False)+'\n')


def get_dataset():
    file = open("..%sfile%smongoFile%sname_paper_map.json"%(sep,sep,sep),'r',encoding='utf-8')
    file2 = open("..%sfile%smongoFile%s15new2.json" % (sep, sep, sep), encoding='utf-8')
    file3 = open("..%sfile%smongoFile%sdataset.json" % (sep, sep, sep), 'w+', encoding='utf-8')

    lines = file.readlines()
    paper_lines = file2.readlines()
    papers = []
    for line in paper_lines:
        paper = json.loads(line)
        papers.append(paper)

    for line in lines:
        name_paper_map = json.loads(line)
        institution = name_paper_map["institution"]
        workers = set()
        co_institutions = set()
        keywords = []
        for link in name_paper_map["papers"]:
            for paper in papers:
                if link == paper["link"]:#找到了对应的paper
                    for author in paper["authors"].keys():#将对应的机构作者加入到员工列表中
                        if institution == paper["authors"][author]["institution"]:
                            workers.add(author)
                        else:
                            co_institutions.add(paper["authors"][author]["institution"])
                    keywords += paper["keywords"]
                    break
        dataset = {}
        dataset["institution"] = institution
        dataset["workers"] = list(workers)
        dataset["co_institutions"] = list(co_institutions)
        dataset["keywords"] = keywords
        file3.write(json.dumps(dataset,ensure_ascii=False)+"\n")

get_dataset()

