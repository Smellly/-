#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-18 20:07:30
# @Author  : Jay Smelly
# @Version : 1

import os
import shutil
import pynlpir
import chardet
# from test_para import para

def wordSegment(fileList):
    pynlpir.open() 
    for filename in fileList:
        # print 'src:', filename,
        name = str(fileList.index(filename))
        src_filename = os.path.join('all_v0', name + '.txt')
        des_filename = src_filename.replace('v0', 'v1')
        shutil.copyfile(filename, src_filename)
        # print '->', src_filename,
        # para(src_filename)
        with open(src_filename, 'r') as fin:
            raw = fin.read()
            coding = chardet.detect(raw)['encoding']
        # print '->', des_filename
        with open(des_filename, 'w') as fout:
            r = pynlpir.nlpir.ParagraphProcess(raw.decode(coding).encode('utf8'), False)
            fout.write(r)
    pynlpir.close()

def getFileList(path):
    fileList = os.listdir(path)
    return fileList

def getPaperList(path):
    paperPath = []
    for paperOrder in os.listdir(path):
        ppath = os.path.join(path, str(paperOrder))
        for year in os.listdir(ppath):
            ypath = os.path.join(ppath, str(year))
            for month in os.listdir(ypath):
                mpath = os.path.join(ypath, str(month))
                fileList = getFileList(mpath)
                for f in fileList:
                    tmpPath = os.path.join(mpath, f)
                    # print tmpPath
                    paperPath.append(tmpPath)        
    return sorted(paperPath)

def all2one(paperList):
    res = []
    for paper in paperList:
        print paper
        with open(os.path.join('all_v1', paper), 'r') as fin:
            article = fin.read().replace('\n', ' ')
        s = combineNegWord(article)
        # print s
        res.append(s)
        # break
    return res

# need all articles fuse into one article (1 paragraph 1 article)
def combineNegWord(sample):
    neg_words = ["不","不屑","不再","不配","不算","不至于","不必","不是","没有","没能","没法","无法","不要","不太","不会","并非","不可","不能","不够","绝不","不想","毫不","不及","没干","无论","无视","无所","无须","毫无","绝无","绝非","也不","也不会","也不能","纵然","纵使","诚然","尽管","虽然"]
    s = ''
    words = sample.split()
    i = 0
    while i < len(words) - 1:
        word = words[i]
        if word in neg_words:
            words[i] = word + words[i+1]
            words.pop(i+1)
            i += 1
        i += 1
    for word in words:
        s += word + ' '
    return  s

if __name__ == '__main__':
    if not os.path.exists('all_v0'):
        os.mkdir('all_v0')
    if not os.path.exists('all_v1'):
        os.mkdir('all_v1')
    # copy decode and word segment
    # paperList = getPaperList('Alltxt')
    # wordSegment(paperList)
    # with open('paperList.txt', 'w') as fout:
    #     for idx,line in enumerate(paperList):
    #         l = line + '\t' + str(idx) + '.txt' + '\n'
    #         fout.write(l)
    # negword + word[i+1]
    paperList = os.listdir('all_v1')
    paperList = sorted(paperList, key = lambda d:int(d[:-4]))
    articles = all2one(paperList)
    # print len(articles)
    with open('test.txt', 'w') as fout:
        for line in articles:
            fout.write(line + '\n')