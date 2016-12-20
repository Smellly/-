#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-20 18:50:06
# @Author  : Jay Smelly (j.c.xing@qq.com)
# @Link    : None
# @Version : $Id$

# from collections import defaultdict
import os

def getDict(path = 'Alltxt'):
    alltxt = dict()
    for paperOrder in os.listdir(path):
        ppath = os.path.join(path, str(paperOrder))
        alltxt[paperOrder] = dict()
        for year in os.listdir(ppath):
            ypath = os.path.join(ppath, str(year))
            alltxt[paperOrder][year] = dict()
            for month in os.listdir(ypath):
                alltxt[paperOrder][year][month] = 0
    # print alltxt    
    return alltxt

def statistic():
    alltxt = getDict()
    with open('predictions.txt', 'r') as fin:
        preds = fin.readlines()

    for line in preds:
        fullname, index, pred = line.split('\t')
        d, paper, year, month, name = fullname.split('/')
        alltxt[paper][year][month] += int(pred)

    # print alltxt
    s = []
    for i in sorted(alltxt): 
    # paper
        # print i,
        for j in sorted(alltxt[i]):
        # year
            # print j,
            for k in sorted(alltxt[i][j]):
            # month
                # print k
                content = str(i) + '/' + str(j) + '/' \
                    + str(k) + '\t' + str(alltxt[i][j][k])
                s.append(content)

    sorted(s)
    with open('statistic.txt', 'w') as fout:            
        for line in s:
            # print line
            fout.write(line + '\n')


if __name__ == '__main__':
    statistic()

