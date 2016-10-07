import urllib2
import base64
import re
import sys
import nltk
from nltk.util import ngrams

def word_grams(words, min=1, max=4):
    s = []
    for n in range(min, max):
        for ngram in ngrams(words, n):
            s.append(' '.join(str(i) for i in ngram))
    return s

def get_stop_word_list(file_name):
	content = open(file_name).read()
	stop_word_list = content.split('\n')
	return stop_word_list
		

def generate_query_word(res_list, number_list):
	query_word = ''
	'''
		some processing
	'''
	return query_word

def generate_url(res_list, number_list):
	query_word = ''
	if not res_list:
		query_word = "%27musk%27"
	else:
		query_word = generate_query_word(res_list, number_list)
	url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%s&$top=10&$format=Atom' % query_word
	return url

def get_page(url):
	#Provide your account key here
	accountKey = 'nelZyDIjJV7cXKNFXeU7iUWgoLSwiUjTS4+H8aWrcgA'
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(url, headers = headers)
	response = urllib2.urlopen(req)
	content = response.read()
	return content

def get_res_list(content):
	title_pattern = re.compile(r"<d:Title.+?>(.+?)</d:Title>")
	url_pattern = re.compile(r"<d:Url.+?>(.+?)</d:Url>")
	desp_pattern = re.compile(r"<d:Description.+?>(.+?)</d:Description>")
	title_list = title_pattern.findall(content)
	url_list = url_pattern.findall(content)
	desp_list = desp_pattern.findall(content)
	res_list = zip(title_list, url_list, desp_list)
	return res_list

def validate_input(content, max_num):
	content = content.replace(' ', '')
	content = content.strip()
	content = content.strip(',')
	if not content:
		return True, []
	for letter in content:
		if not letter in '01234567890,':
			return False, []
	number_list = map(int, content.split(','))
	if max(number_list) > max_num:
		return False, []
	return True, number_list

if __name__ == '__main__':
	res_list = []
	number_list = []
	stop_word_list_file = 'stop_words.txt'
	stop_word_list = get_stop_word_list(stop_word_list_file)
	while 1:
		url = generate_url(res_list, number_list)
		content = get_page(url)
		res_list = get_res_list(content)
		for i in range(len(res_list)):
			print i+1
			print 'Title:', res_list[i][0]
			print 'Url:', res_list[i][1]
			print 'Description:', res_list[i][2]
		print 'please input the number of relavant pages, seperated by \',\''
		legal = False
		while not legal:
			line = sys.stdin.readline() 
			res, number_list = validate_input(line, len(res_list))
			if not res:
				print 'invalid input, try again'
			else:
				break
		print number_list
		break
	sys.exit()

