import jieba
import numpy as np
from isIdealString import *
import sys
import CrawlTitle
import time
import ToHTML
import sys

if len(sys.argv) < 3:
    print("Wrong parameter")
    print("./copyfile.py Input_File_Name Output_File_Name(.html file)")
    sys.exit(1)

WordsToIndex = np.load("../WordsToIndex.npy").item()
BigramCounter = np.load("../BigramCounter.npy").item()

f = open(sys.argv[1])

file = f.read()

seg_list = jieba.cut(file,cut_all=False)

SuspiciousList = []


counter = False


# get the word in the test doc
for word in seg_list:
	if counter == False:
		PreviousWord = word
		counter = True
	else:
		if isIdealString(word,PreviousWord):
			if BigramCounter[WordsToIndex[PreviousWord],WordsToIndex[word]] == 0:
				SuspiciousList.append((PreviousWord,word))
		PreviousWord = word

print(SuspiciousList)
print(len(SuspiciousList))
print("\n")

time.sleep(1)


# get the worong word according to the result of search


WrongWordList = []

for pairs in SuspiciousList:
	question_word = ""
	question_word += pairs[0]
	question_word += pairs[1]
	res, NeedAutoCorrection = CrawlTitle.GetTitle(question_word)
	# print(res)
	if not CrawlTitle.CheckCorrectness(res, question_word) or NeedAutoCorrection:
		WrongWordList.append(pairs)
	time.sleep(0.5)

print(WrongWordList)
print(len(WrongWordList))

ToHTML.ToHTML(file,sys.argv[2], WrongWordList)
