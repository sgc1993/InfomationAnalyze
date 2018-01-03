import jieba.analyse

def loadStopWord(fileName):
    """
    加载停用词
    :fileName: 停用词路径
    :return: 返回停用词的集合
    """
    stopwords = set()
    fstop = open(stopwordsPath, 'r', encoding='utf-8', errors='ignore')
    for eachWord in fstop:
        stopwords.add(eachWord.strip())
    fstop.close()
    return stopwords

def init():
    """
    初始化全局变量和停用词表
    :return: None
    """
    global stopwordsPath, dataPath, keywordsPath, stopwords  # 声明全局变量
    stopwordsPath = "file\\stopwords_cn.txt"
    dataPath = "file\\paper_clean.dat"
    keywordsPath = "file\\paper_keywords_textrank2.dat"
    stopwords = loadStopWord(stopwordsPath)
    print("停用词加载完成: 共%d个停用词. " % (len(stopwords)))
    print("初始化完成. ")

def cutText(text):
    """
    对文本进行分词
    :param text: 待分词的文本
    :return: 分词结果
    """
    wordList = list(jieba.cut(text))  # 用结巴分词，对每行内容进行分词
    reList = []
    for word in wordList:
        if word not in stopwords:  # 手动去停用词
            reList.append(word)
    return reList

def extractWords(text, num=20, withWeight=False):
    """
    提取关键词
    :param text: 待提取文本
    :param num: 提取关键词的数量
    :param withWeight: 是否返回权重
    :return: 关键词的列表
    """
    jieba.analyse.set_stop_words(stopwordsPath)  # 加载停用词
    # return jieba.analyse.extract_tags(text, topK = num, withWeight = withWeight)  tf-idf
    return jieba.analyse.textrank(text, topK=num, withWeight=withWeight)

def extractPhrases(text, keywordsNum=20, reKeywordsNum=5, minOccurNum=2):
    """
    获取关键[词语]和[短语]。
    获取 keywordsNum 个关键词中前 reKeywordsNum 个关键词。
    获取 keywordsNum 个关键词构造的可能出现的[短语]，要求这个短语在原文本中至少出现的次数为 minOccurNum 。
    :param text: 待提取文本
    :param keywordsNum: 待选关键[词语]数量
    :param reKeywordsNum: 返回关键[词语]数量
    :param minOccurNum: [短语]最少出现次数
    :return: 关键关键词语和短语的列表。
    """
    keywordsList = extractWords(text, num=keywordsNum)  # 提取关键词语
    # 将候选关键词中的前 reKeywordsNum 添加到返回列表中
    reKeyWords = [keywordsList[i] for i in
                  range((reKeywordsNum < len(keywordsList)) and reKeywordsNum or len(keywordsList))]
    keywordsSet = set(keywordsList)
    keyphrases = set()
    one = []
    # 获取关键短语
    for word in cutText(text):
        if word in keywordsSet:
            one.append(word)
        else:
            if len(one) > 1:
                keyphrases.add(''.join(one))
            if len(one) == 0:
                continue
            else:
                one = []
    # 最后一个
    if len(one) > 1:
        keyphrases.add(''.join(one))
    # 出现次数大于 minOccurNum 的加入关键词列表
    reKeyWords.extend([phrase for phrase in keyphrases
                       if text.count(phrase) >= minOccurNum])
    return reKeyWords

def main():
    init()
    text = "在分析Turbo码编译码中MAP类译码算法的基础上,重点研究了Max-Log-MAP译码算法的工程实现方法.为解决Turbo码译码嚣FPGA实现时的复杂性高、存储量大的问题,提出了一种基于FPGA的优化译码器结构和译码算法实现方案,有效减少了存储容量,提高了处理速度,并在Altera的EP2S90芯片上实现了10MHz速率的Turbo码译码器,通过时序仿真验证了译码结构的有效性."
    text2 = "提出了一种基于伪随机补偿技术的流水线模数转换器（ADC）子级电路．该子级电路能够对比较器失调和电容失配误差进行实时动态补偿．误差补偿采用伪随机序列控制比较器阵列中参考比较电压的方式实现．比较器的高低位被随机分配，以消除各比较器固有失调对量化精度的影响，同时子ADC输出的温度计码具有伪随机特性，可进一步消除MDAC电容失配误差对余量输出的影响．基于该子级电路设计了一种12位250 MS/s流水线ADC，电路采用0．18μm 1P5M 1．8 V CMOS工艺实现，面积为2．5 mm2．测试结果表明，该ADC在全速采样条件下对20 MHz输入信号的信噪比（SNR）为69．92 dB，无杂散动态范围（SFDR）为81．17 dB，积分非线性误差（INL）为-0．4～＋0．65 LSB，微分非线性误差（DNL）为-0．2～＋0．15 LSB，功耗为320 mW．"
    list = extractPhrases(text)
    list2 = extractPhrases(text2)
    for i in list+list2:
        print(i)
if __name__ == "__main__":

    main()