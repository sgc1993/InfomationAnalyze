import json
import heapq
#编辑距离
class arithmetic():
    def __init__(self):
        pass

    ''''' 【编辑距离算法】 【levenshtein distance】 【字符串相似度算法】 '''

    def levenshtein(self, first, second):
        if len(first) > len(second):
            first, second = second, first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [[0 for i in range(second_length)] for x in range(first_length)]

        for i in range(1, first_length):
            distance_matrix[i][0] = i
        for i in range(1, second_length):
            distance_matrix[0][i] = i
        #print(distance_matrix)
        for i in range(1, first_length):
            for j in range(1, second_length):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion,deletion,substitution)

        return distance_matrix[first_length - 1][second_length - 1]

#K顶堆
class TopKHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)

    def topk(self):
        #return [x for x in [heapq.heappop(self.data) for x in range(len(self.data))]]
        return [x for x in reversed([heapq.heappop(self.data) for x in range(len(self.data))])]

def getNameList(FilePath):
    file = open(FilePath, encoding='UTF-8')
    try:
        lines = file.readlines()
        nameList = []
        for line in lines:
            institutionJson = json.loads(line)
            nameList.append(institutionJson["name"])
    finally:
        file.close()
        return nameList

if __name__ == "__main__":
    #arith = arithmetic()
    #print(arith.levenshtein('电子科技集团15所', '电子科技集团28所'))
    # list_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # th = TopKHeap(2)
    #
    # th.push((3,"中电科技大学啊啊啊啊啊"))
    # th.push((4,"中电科技大学"))
    # th.push((2,"中电科技北京"))
    # th.push((1,"中电科技65所"))
    # th.push((8,"中电科技大学"))
    #
    # print(th.topk())
    file = open("file\\nameEidtSim.dat", 'w+', encoding='UTF-8')
    arith = arithmetic()
    nameList = getNameList("file\\dict_data4.dat")

    for name1 in nameList[10:15]:
        th = TopKHeap(5)
        nameDict = {}
        for name2 in nameList:
            if(name1 == name2):
                continue
            th.push((-arith.levenshtein(name1,name2) / len(name2), name2))
        nameDict["name"] = name1
        nameDict["similar"] = th.topk()
        json_dict = json.dumps(nameDict, ensure_ascii=False)
        file.write(json_dict + "\n")

