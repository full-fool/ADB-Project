import Requests
import time
import subprocess

def load_cache():


def retrieve_top_4(cached_list):
	html_dict = {}
	for i in cached_list:
		url = cached_list[i].url
		time.sleep(5)
		req = urllib2.Request()
		handler = urllib2.urlopen(req)
		header = handler.headers.getheader('content-type')
		if 'text/html' in header:
			#html = handler.read().decode("utf-8")
			html_dict[url] = True
	return html_dict


def create_content_sample(html_dict):
	doc_sample = {}
	for key in html_dict.keys():
		output = subprocess.check_output(['java', 'getWordsLynx', key])
		for w in output:
			if w in doc_sample:
				doc_sample[w] += 1
			else:
				doc_sample[w] = 1


def sample_document():
	doc_sample = create_content_sample(retrieve_top_4())


