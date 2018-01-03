# -*- coding: utf-8 -*-
import json
import os
sep = os.path.sep


def __key_clean__(key, **kwargs):
	pass


def __institution_clean__(institution, **kwargs):
	'''
	Disambiguation
	Get uniqe institution name
	传入的是这样的字符串：中国电子科技集团公司第15研究所,北京,100083
	'''
	#If several institutions name in the same row,separator by ';' ,get the first one.(it was not supposed to appear,stupid wanFang...)
	institution = institution.decode('utf-8').split(';')[0]
	# print institution
	new_name = ''
	if_no_title_name = ''
	flag = False
	flag2 = False
	index = 0
	temp = ''
	no_title_name_flag = False
	#set separator
	separatorList = kwargs.get('separator')
	if separatorList == None:
		# separator = '所'
		separatorList = ["所", "学院", "系", "实验室"]
	ok = False
	for separator in separatorList:
		if ok == True:
			break
		if separator in institution:
			'''
            e.x.
            input:中国电子科技集团,第十四研究所,江苏,南京,210013
            output:电子科技集团14所
            '''
			ok = True
			institution = institution.strip().split(separator)[0].replace(',', '').replace('，', '').replace(' ', '').split(';')[0] + separator
			no_title_name_flag = True
	if ok == False:
		institution = institution.strip().split(" ")[0].split(",")[0].split('，')[0]
	# print institution
	return institution


def __date_clean__(date, **kwargs):
	if len(date) == 0:
		return None
	year = date.split(',')[0]
	period = date.split('(')[1].split(')')[0]
	return {'year': year, 'period': period}


def __location_clean__(institution,**kwargs):
	#传入的是这样的字符串：中国电子科技集团公司第15研究所,北京,100083
	city_list = read_city()
	institution = institution.decode('utf-8')
	institution = institution.split(';')[0]
	city = [x for x in city_list if x in institution]
	if len(city) == 0:return None
	max = 0
	locate = None
	for c in city:
		if institution.find(c) >= max:
			max = institution.find(c)
			locate = c
	#'北京大学.深圳研究生院' => return '深圳' not '北京'
	return locate


#将city.txt中河北省邢台市处理为邢台
def read_city():
    # Return all city's name in China
	file = open("..%sfile%scity.txt" % (sep, sep), encoding='UTF-8')
	name_list = file.readlines()
	file.close()
	names = set()
	for line in name_list:
		line = line.strip("\r\n").strip()
		line = line.split('省')
		# print(line)
		line = line[-1].split('市')[0]
		names.add(line)
	return names


#清洗一个字典
def clean(line):
	standard_names = ['中航工业','电子科技集团']
	try:
		temp = {}
		temp['institutions'] = {}
		temp['authors'] = {}
		temp['abstract'] = {}
		temp['title'] = line['title']
		temp['link'] = line['link']
		temp['keywords'] = line['keywords']
		temp['quote'] = line['quote']
		temp['spidertime'] = line['spidertime']
		temp['url'] = line['url']
		#set include
		if len(line['include'])==0:
			temp['include'] = None
		else:
			temp['include'] = line['include']
		#set journal
		temp['journal'] = line['journal']
		temp['date'] = __date_clean__(line['date'])
		temp['abstract']['Chinese'] = line['abstract']
		#Because of my stupid when crawl data,so have to do like this...
		#   not notice that if there just have one institution record,spider return a str type,not a list..
		if isinstance(line['institutions'],list):#有多个机构时，该字段是个列表
			for x in range(min(len(line['institutions']),len(line['authors']))):
				institution = __institution_clean__(line['institutions'][x].encode("utf-8"), standard_names=standard_names)
				# problem
				locate = __location_clean__(line['institutions'][x].encode("utf-8"))
				temp['authors'][line['authors'][x]] = {}
				temp['authors'][line['authors'][x]]['institution'] = institution
				temp['authors'][line['authors'][x]]['location'] = locate
				temp['institutions'][institution] = locate
		else:#只有一个机构时，该字段是个字符串
			temp['authors'][line['authors'][0]] = {}
			institution =  __institution_clean__(line['institutions'].encode("utf-8"), standard_names=standard_names)
			locate = __location_clean__(line['institutions'].encode("utf-8"))
			for x in line['authors']:
				temp['authors'][x] = {}
				temp['authors'][x]['institution'] = institution
				temp['authors'][x]['location'] = locate
			temp['institutions'][institution] = locate
		# temp['institutions'] = line['institutions']
		return temp
	except Exception as e:
		print('-----sssss------')
		print(e)
		print("-----eeeee-----")


#清洗文件
def clean_file(from_file, to_file):
	resultFile = open(from_file, 'w', encoding='UTF-8')
	with open(to_file, encoding='UTF-8') as f:
		result = f.readlines()
	#write file name
	for line in result:
		try:
			line = json.loads(line)
			#line['url'] = 'http://s.wanfangdata.com.cn/Paper.aspx?q= 题名:人工智能'
			temp = clean(line)
			temp.pop('url')#去掉url字段
			tempstr = json.dumps(temp, ensure_ascii=False)
			resultFile.write(tempstr+'\n')
		except Exception as e:
			print(e)







