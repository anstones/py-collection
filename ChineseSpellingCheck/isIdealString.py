# stop_symbols 是文档中可能出现的符号

stop_symbols = [".", ",","。","#", "\n", "(", "、", "`", "，", \
"##","$","###","####", "-", "+","|","/", ":", "：","*","?","!","@", \
"#"," ","\'","\"","\\",";","%",")","(","<",">","？","！","；","「","」","（","）" \
"[","]","{","}","“","”","）","《","》","=","\t","】","__"]

# word 和 PreviousWord 是我们要检测的前后关系

def isIdealString(word, PreviousWord):
	if PreviousWord not in stop_symbols \
	and word not in stop_symbols \
	and not word[0].encode("UTF-8").isalpha() \
	and not PreviousWord[0].encode("UTF-8").isalpha() \
	and not word[0].isdigit() \
	and not PreviousWord[0].isdigit():
		return True
	else:
		return False