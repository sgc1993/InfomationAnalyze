import json
import os
import util.clean
sep = os.path.sep


#根据论文link,去除重复paper
def remove_duplicate_paper_in_file(from_path, to_path):
    file = open(from_path,encoding='UTF-8')
    file2 = open(to_path,'w+',encoding='UTF-8')
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
        print(len(lines))
        print(len(paper_json_list))
        for paper_json in paper_json_list:
            file2.write(json.dumps(paper_json,ensure_ascii=False)+'\n')
    finally:

        file.close()
        file2.close()

#remove_duplicate_paper_in_file("..%sfile%smongoFile%s541.json"%(sep,sep,sep),"..%sfile%smongoFile%s541new.json"%(sep,sep,sep))

#获得某个机构爬取论文集合中所有不重复机构名
def get_institution_name_set_from_file(from_path,to_path,id):
    file = open(from_path,"r",encoding='utf-8')
    file2 = open(to_path,"w+",encoding='utf-8')
    lines = file.readlines()

    num_dict = {10:"十", 14:"十四", 15:"十五", 28:"二十八", 29:"二十九", 30:"三十", 36:"三十六", 38:"三十八", 54:"五十四"}
    name_dict = {10: "成都", 14: "南京电子技术", 15: "华北计算技术", 28: "南京电子工程", 29: "西南电子设备", 30: "西南通信", 36: "嘉兴", 38: "华东电子工程", 54: "通信测控"}
    institution_names = set()
    for line in lines:
        line = line.strip()
        paper_json = json.loads(line)
        for key in paper_json["institutions"].keys():
            # if "电" in key and "科" in key:
            #     if str(id) in key or num_dict[id] in key:
            #         institution_names.add(key)
            # else:
            #     if name_dict[id] in key:
            #         institution_names.add(key)
            if key == "":
                print(line)#"institutions": {"": null, "南京电子器件研究所": "南京"}
            institution_names.add(key)
    for name in institution_names:
        if name == "":
            print(id)
            continue
        file2.write(name+"\n")



def get_institution_name_paper_map(id):
    file = open("..%sfile%smongoFile%s%dnamesall.json"%(sep,sep,sep,id),encoding='utf-8')
    file2 = open("..%sfile%smongoFile%s%dnew2.json" % (sep, sep, sep,id), encoding='utf-8')
    file3 = open("..%sfile%smongoFile%s%dname_paper_map.json"%(sep,sep,sep,id),'w+',encoding='utf-8')
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


def get_dataset(id):
    file = open("..%sfile%smongoFile%s%dname_paper_map.json"%(sep,sep,sep,id),'r',encoding='utf-8')
    file2 = open("..%sfile%smongoFile%s%dnew2.json" % (sep, sep, sep,id), encoding='utf-8')
    file3 = open("..%sfile%smongoFile%s%ddataset.json" % (sep, sep, sep,id), 'w+', encoding='utf-8')

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

#get_dataset()

def get_all_name_set():
    files = [10, 14, 15, 28, 29, 30, 36, 38, 54]
    for id in files:
        get_institution_name_set_from_file("..%sfile%smongoFile%s%dnew2.json"%(sep,sep,sep,id),
                                           "..%sfile%smongoFile%s%dnamesall.json" % (sep, sep, sep, id),id)

def get_all_name_paper_map():
    files = [10, 14, 15, 28, 29, 30, 36, 38, 54]
    for id in files:
        get_institution_name_paper_map(id)



def get_all_dataset():
    files = [10, 14, 15, 28, 29, 30, 36, 38, 54]
    for id in files:
        get_dataset(id)

#去除没有classnum字段的数据
def remove_data_without_classnum():
    file = open("..%sfile%smongoFile%s54all.json"%(sep,sep,sep),encoding='utf-8')
    file2 = open("..%sfile%smongoFile%s54re.json" % (sep, sep, sep),'w+', encoding='utf-8')

    lines = file.readlines()
    for line in lines:
        paper = json.loads(line)
        if "classnum" in paper.keys():
            file2.write(json.dumps(paper,ensure_ascii=False)+'\n')

#将一个文件内容追加到另一个文件中
def append_file(file_path, append_path):
    file = open(file_path,'a', encoding='utf-8')
    append = open(append_path,encoding='utf-8')

    lines = append.readlines()
    for line in lines:
        file.write(line)

#append_file("..%sfile%smongoFile%s541.json" % (sep, sep, sep),"..%sfile%smongoFile%s54re.json" % (sep, sep, sep))