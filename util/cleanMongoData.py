import json
import os
import util.clean
sep = os.path.sep


#根据论文link,去除重复paper
def remove_duplicate_paper_in_file():
    file = open("..%sfile%smongoFile%s15.json"%(sep,sep,sep),encoding='UTF-8')
    file2 = open("..%sfile%smongoFile%s15new.json"%(sep,sep,sep),'w',encoding='UTF-8')
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

