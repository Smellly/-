# -*- coding: utf-8 -*-
'''
// Author: Jay Smelly.
// Last modify: 2016-12-12 09:28:40.
// File name: 002_word2dic.py
//
// Description:
    將分詞後的結果形成詞表，統計詞頻並按詞頻大小排列
'''
import re

neg_words = ["不","不屑","不再","不配","不算","不至于","不必","不是","没有","没能","没法","无法","不要","不太","不会","并非","不可","不能","不够","绝不","不想","毫不","不及","没干","无论","无视","无所","无须","毫无","绝无","绝非","也不","也不会","也不能","纵然","纵使","诚然","尽管","虽然"]


def combineNegWord(path):
    res = []
    # r = re.compile()
    with open(path, 'r' ) as fin:
        samples = fin.readlines()
    for sample in samples:
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
        res.append(s+'\n')
    return  res

if __name__ == '__main__':
    path = '/home/cc/Workspaces/uncertain/test/'
    pos_path = path + 'pos_set.txt'
    neg_path = path + 'neg_set.txt'
    pos = combineNegWord(pos_path)
    neg = combineNegWord(neg_path)
    print 'saving to', path
    with open(path + 'pos_v1.txt', 'w') as fout:
        for line in pos:
            # print line
            fout.write(line)
    with open(path + 'neg_v1.txt', 'w') as fout:
        for line in neg:
            fout.write(line)
            
