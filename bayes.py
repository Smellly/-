# -*- encoding:utf8 -*-
'''
Created on Oct 19, 2010
@author: Peter
'''
from numpy import *
import random
from tqdm import tqdm

# return
# postingList,classVec
def loadDataSet():
    with open('pos_v1.txt', 'r') as fin:
        pos_s = fin.readlines()
        print 'num of train pos:', len(pos_s)
    pos_l = [1] * len(pos_s)
    with open('neg_v1.txt', 'r') as fin:
        neg_s = fin.readlines()
        print 'num of train neg:', len(neg_s)
    neg_l = [0] * len(neg_s)
    pos = [(s,l) for s,l in zip(pos_s, pos_l)]
    neg = [(s,l) for s,l in zip(neg_s, neg_l)]
    sl = pos + neg
    random.shuffle(sl)
    samples = []
    labels = []
    for item in sl:
        samples.append(item[0])
        labels.append(item[1])
    return samples,labels
                 
def createVocabList():
    vocabSet = set([])  #create empty set
    with open('dic.txt', 'r') as fin:
        words = fin.readlines()
    for line in words:
        word = line.split(':')[0]
        word.replace('NEG', '')
        vocabSet.add(word)
    return list(vocabSet)

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones() 
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)          #change to log()
    p0Vect = log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else: 
        return 0

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        # else: print "the word: %s is not in my Vocabulary!" % word
    # print returnVec
    return returnVec

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    # print returnVec
    return returnVec

def loadTestDataSet():
    with open('test.txt', 'r') as fin:
        samples = fin.readlines()
        print 'num of test:', len(samples)
    return samples
   
# for train 
def spamTest():
    docList=[]; classList = []
    testdocList = []; testclassList = []
    docList,classList = loadDataSet()
    vocabList = createVocabList()#create vocabulary
    testdocList,testclassList = loadTestDataSet()
    trainingSet = range(len(docList))
    testSet     = range(len(testdocList))       #create test set
    # testSet = []
    # for i in range(int(0.2*len(docList))):
    #     randIndex = int(random.uniform(0,len(trainingSet)))
    #     testSet.append(trainingSet[randIndex])
    #     del(trainingSet[randIndex])  
    print 'train set:', len(trainingSet)
    print 'test set:', len(testSet)
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex].split()))
        trainClasses.append(classList[docIndex])
        # break
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = setOfWords2Vec(vocabList, testdocList[docIndex].split())
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != testclassList[docIndex]:
            errorCount += 1
            #print "classification error",docList[docIndex]
        # break
    print 'the error rate is: ', float(errorCount)/len(testSet)

# for final test
def uncertainTest():
    docList=[]; classList = []
    testdocList = []
    docList,classList = loadDataSet()
    vocabList = createVocabList()#create vocabulary
    testdocList = loadTestDataSet()
    trainingSet = range(len(docList))
    testSet     = range(len(testdocList))       #create test set
    print 'train set:', len(trainingSet)
    print 'test set:', len(testSet)
    trainMat=[]; trainClasses = []
    print 'training...'
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex].split()))
        trainClasses.append(classList[docIndex])
        # break
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    predList = []
    print 'predicting...'
    for docIndex in tqdm(testSet):        #classify the remaining items
        wordVector = setOfWords2Vec(vocabList, testdocList[docIndex].split())
        predList.append(classifyNB(array(wordVector),p0V,p1V,pSpam))
        # break
    # print len(predList)
    with open('predList.txt', 'w') as fout:
        for line in predList:
            fout.write(str(line) + '\n')
    with open('paperList.txt', 'r') as fin:
        paperList = fin.readlines()
    assert(len(predList) == len(paperList))
    for paper, pred in zip(paperList, predList):
        content = paper.strip('\n') + '\t' + str(pred) + '\n'
        fout.write(content)

if __name__ == '__main__':
    # uncertainTest()
    with open('predList.txt', 'r') as fin:
        predList = fin.readlines()
    with open('paperList.txt', 'r') as fin:
        paperList = fin.readlines()
    assert(len(predList) == len(paperList))
    with open('predictions.txt', 'w') as fout:
        for paper, pred in zip(paperList, predList):
            content = paper.strip('\n') + '\t' + str(pred).strip('\n') + '\n'
            fout.write(content)