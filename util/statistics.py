import json
import os

sep = os.path.sep

def get_institution_names(file_path, to_file_path):
    file = open(file_path, encoding='UTF-8')
    to_file = open(to_file_path, 'w', encoding='UTF-8')

    institution_name_list = []
    for line in file.readlines():
        paper_json = json.loads(line)
        for institution_name in paper_json["institutions"].keys():
            institution_name_list.append(institution_name)

    for institution_name in institution_name_list:
        to_file.write(institution_name+'\n')




#get_institution_names("..%sfile%smongoFile%s15new2.json" % (sep,sep,sep), "..%sfile%smongoFile%s15names.json" % (sep,sep,sep))