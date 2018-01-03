import DataBase
import json
mssql = DataBase.MSSQL('localhost','STIMSTEST','sa','1q2w3e4r5t!')
#rows = mssql.ExecNonQuery("insert into Company (企业名称,ID) values('中国北邮电科',10000)")
#mssql.ExecNonQuery("DELETE FROM Company WHERE 企业名称='中国北邮电科'")
#mssql.ExecNonQuery("insert into institution  values('%s','%s','%d','%d')"%('明天','北京',2,1000))
file = open("file//dict_data4.dat",encoding='UTF-8')
#将文本数据导入数据库中
try:
    institutionList = file.readlines()
    id = 0
    num = 0
    for line in institutionList:
        institution = json.loads(line)
        id = id + 1
        print(id)
        try:
            mssql.ExecNonQuery("insert into institution values('%s','%s','%d','%d')"%(institution['name'],institution['location'],institution['num'],id))
        except Exception as e:
            num = num + 1
finally:
    print(num)
    file.close()