#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
统计1.txt文档内出现频率最高的十个词和出现的次数
"""
f = open('/1.txt')
count = {}

for line in f:
    line = line.strip()
    words = line.split()
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

word_freq = []
for word, freq in count.items():
    word_freq.append((word, freq))

word_freq.sort(reverse = True)

for word, freq in word_freq[:10]:
    print(word, freq)


# 直接遍历count
count_sort = sorted(count.items(), key=lambda x: x[1], reverse=True)
for freq in count_sort[:10]:
    print(freq)


result = defaultdict(int)
with open(file_path) as f:
    for line in f:
        for word in filter(None,line.strip().split(' ')):
            result['word'] += 1
    print(sorted(result.items(), key=lambda(x,y):y, reverse=True))[:10]
    


