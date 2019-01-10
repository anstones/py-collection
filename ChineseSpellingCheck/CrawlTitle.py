import sys
from bs4 import BeautifulSoup
from urllib import parse
from urllib import request

# question_word 是我们传入的需要检查是否为常用搭配的单词元组
def GetTitle(question_word):

	url = parse.quote('http://cn.bing.com/search?q='+question_word, safe='/:?=' )

    # 假装成一个浏览器进行访问
	req = request.Request(
    url,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    	}
	)

    # 得到了我们的页面
	htmlpage = request.urlopen(req).read().decode('utf8')

    # 对我们的HTML界面进行解析
	soup = BeautifulSoup(htmlpage,'html.parser')

    # 找到所有<strong>标签，res是一个列表
	res = soup.find_all('strong')


	NeedAutoCorrection = False

    # 如果搜索引擎有提示，那么这个搭配就肯定有问题
	if htmlpage.find('<div>是否只需要 <a') != -1:
		NeedAutoCorrection = True

	return res, NeedAutoCorrection

def CheckCorrectness(res, question_word):

	counter = 0

	for highlightWords in res:
		content = highlightWords.get_text()

		if content.find(question_word) != -1:
			counter += 1

	if counter > 3:
		return True
	else:
		return False
