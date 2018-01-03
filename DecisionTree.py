 #coding=utf-8
import operator

from sklearn.datasets import load_iris
from math import log
from sklearn import tree
import time

def createDataSet():
    dataSet=[[1,1,1,'yes'],
              [1,1,1,'yes'],
              [1,0,0,'no'],
             [0,1,0,'no'],
             [0,1,1,'no'],
             [0,0,1, 'no'],
             [0,1,0, 'yes']]
    labels = ['test','flippers','no surfaceing']
    return dataSet, labels

 #计算香农熵
def calcShannonEnt(dataSet):
     numEntries = len(dataSet)
     labelCounts = {}
     for feaVec in dataSet:
         currentLabel = feaVec[-1]
         if currentLabel not in labelCounts:
             labelCounts[currentLabel] = 0
         labelCounts[currentLabel] += 1
     shannonEnt = 0.0
     for key in labelCounts:
         prob = float(labelCounts[key]) / numEntries
         shannonEnt -= prob * log(prob, 2)
     return shannonEnt

#构造在某个维度上进行决策之后的剩余数据
def splitDataSet(dataSet, axis, value):
     retDataSet = []
     for featVec in dataSet:
         if featVec[axis] == value:
             reducedFeatVec = featVec[:axis]
             reducedFeatVec.extend(featVec[axis+1:])#拼接数组
             retDataSet.append(reducedFeatVec)
     return retDataSet

def chooseBestFeatureToSplit(dataSet):
     numFeatures = len(dataSet[0]) - 1#因为数据集的最后一项是标签
     baseEntropy = calcShannonEnt(dataSet)
     bestInfoGain = 0.0
     bestFeature = -1
     for i in range(numFeatures):
         featList = [example[i] for example in dataSet]
         uniqueVals = set(featList)
         newEntropy = 0.0
         for value in uniqueVals:
             subDataSet = splitDataSet(dataSet, i, value)
             prob = len(subDataSet) / float(len(dataSet))
             newEntropy += prob * calcShannonEnt(subDataSet)
         infoGain = baseEntropy -newEntropy
         if infoGain > bestInfoGain:
             bestInfoGain = infoGain
             bestFeature = i
     return bestFeature

 #因为我们递归构建决策树是根据属性的消耗进行计算的，所以可能会存在最后属性用完了，但是分类
 #还是没有算完，这时候就会采用多数表决的方式计算节点分类
def majorityCnt(classList):
     classCount = {}
     for vote in classList:
         if vote not in classCount.keys():
             classCount[vote] = 0
         classCount[vote] += 1
     return max(classCount)

def createTree(dataSet, labels):
     classList = [example[-1] for example in dataSet]
     if classList.count(classList[0]) ==len(classList):#类别相同则停止划分
         return classList[0]
     if len(dataSet[0]) == 1:#所有特征已经用完
         return majorityCnt(classList)
     bestFeat = chooseBestFeatureToSplit(dataSet)
     bestFeatLabel = labels[bestFeat]
     myTree = {bestFeatLabel:{}}
     del(labels[bestFeat])
     featValues = [example[bestFeat] for example in dataSet]
     uniqueVals = set(featValues)
     for value in uniqueVals:
         subLabels = labels[:]#为了不改变原始列表的内容复制了一下
         myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,
                                         bestFeat, value),subLabels)
     return myTree

def main():
     data,label = createDataSet()
     t1 = time.clock()
     myTree = createTree(data,label)
     t2 = time.clock()
     print(myTree)
     #print('execute for '+(t2-t1))

def test():
    # X = [[0, 0], [1, 1],[2,2]]
    # Y = [0, 1, 3]
    #
    # clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(X, Y)
    #
    # print(clf.predict([[2., 2.]]))
    # print(clf.predict_proba([[2., 2.]]))

    iris = load_iris()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(iris.data, iris.target)
    print(iris.data[:1, :])
    print(clf.predict(iris.data[:1, :]))

if __name__=='__main__':
     #main()
     #test()
     a = [1,2,3,4,5,6,7,8,9]
     a = [[1,2,3],[4,5,6],[7,8,9]]
     print(a[:3])