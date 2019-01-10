# -*- coding: utf-8 -*-
import collections
import jieba
import numpy as np
from isIdealString import * 



# calcualte the frequency of each word 
# WordFrequency = collections.Counter()

WordsToIndex = collections.defaultdict(int)

counter = 0
BigramCounter = collections.defaultdict(int)



for i in range(1,3):

	f = open("../Data/File%d.txt" % i)


	# 读取数据
	file = f.read()

	# 调用 Jieba 库进行中文分词
	seg_list = jieba.cut(file, cut_all=False)

    
	for word in seg_list:
		# 初始化 WordsToIndex
		if word not in WordsToIndex:
			WordsToIndex[word] = counter
			counter = counter + 1

		# 初始化 BigramCounter
		if counter == 1:
			PreviousWord = word
		else:
			if isIdealString(word,PreviousWord): 
				BigramCounter[WordsToIndex[PreviousWord],WordsToIndex[word]] += 1
			PreviousWord = word

np.save('WordsToIndex.npy', WordsToIndex)
np.save('BigramCounter.npy', BigramCounter)





















