import base64
import json
import re
import sys
import urllib
import urllib2

# stores the mapping between category and all queries
query_dict = {}

# stores the hierarchy of categories
category_dict = {'Root':['Computers', 'Health', 'Sports'], 'Computers':['Hardware', 'Programming'], \
	'Health':['Fitness', 'Diseases'], 'Sports':['Basketball', 'Soccer']}

# stores the mapping between query and [category, result_dict]
query_result = {}

# stores the mapping between db url and number of total documents
db_info = {}

def generate_query(query_word, site):
	valid_query = urllib.quote(query_word)
	query_part = '%27site%3a' + site + '%20' + valid_query + '%27'
	return query_part

def generate_url(query_part):
	url = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%s&$top=4&$format=JSON' % query_part
	return url

# get response of Bing API
def get_page(url):
	#Provide your account key here
	accountKey = 'nelZyDIjJV7cXKNFXeU7iUWgoLSwiUjTS4+H8aWrcgA'
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(url, headers = headers)
	response = urllib2.urlopen(req)
	content = response.read()
	return content

def get_queries():
	queries = []
	for line in open('queries.txt'):
		content = line.split()
		category = content[0]
		query = ' '.join(content[1:])
		if not category in query_dict:
			query_dict[category] = [query]
		else:
			query_dict[category].append(query)

def load_cache():
	for line in open('cache'):
		original_dict = json.loads(line)
		key = original_dict.keys()[0]
		value = original_dict[key]
		query_result[key] = value

def save_to_cache(query, content, category):
	res_dict = {}
	res_dict[query] = [category, content]
	res_string = json.dumps(res_dict)
	file_handler = open('cache', 'a')
	file_handler.write('%s\n' % res_string)
	file_handler.close()

def get_db_info(db_url):
	if db_url in db_info:
		return db_info[db_url]
	query_part = generate_query("", db_url)
	query_url = generate_url(query_part)
	page_content = get_page(query_url)
	returned_dict = json.loads(page_content)
	database_total_num = returned_dict["d"]["results"][0]["WebTotal"]
	db_info[db_url] = database_total_num
	file_handler = open('db_info', 'a')
	file_handler.write('%s###%s\n' % (db_url, database_total_num))
	file_handler.close()
	return database_total_num

def load_db_info():
	for line in open('db_info'):
		[key, value] = line.split('###')
		db_info[key] = int(value)

def classify(category, database_url, ec, es, ESpecificity):
	result_categories = []
	if not category in category_dict:
		return [category]
	sub_categories = category_dict[category]
	
	for each_category in sub_categories:
		total_num = 0
		for query in query_dict[each_category]:
			query_part = generate_query(query, database_url)
			if query_part in query_result:
				query_part_dict = json.loads(query_result[query_part][1])
				print int(query_part_dict["d"]["results"][0]["WebTotal"])
				total_num += int(query_part_dict["d"]["results"][0]["WebTotal"])
			else:
				request_url = generate_url(query_part)
				page_content = get_page(request_url)
				returned_dict = json.loads(page_content)
				res_num = returned_dict["d"]["results"][0]["WebTotal"]
				query_result[query_part] = [each_category, page_content]
				save_to_cache(query_part, page_content, each_category)
				print res_num
				total_num += res_num
		
		# database_total_num = db_info[database_url] if database_url in db_info else get_db_info(database_url)
		# print 'database total num for ' + database_url + ' is ' + str(database_total_num)
		database_total_num = ESpecificity * total_num / 
		coverage = total_num
		specificity = float(total_num) / float(database_total_num)
		print 'Specificity for category:%s is %s' % (each_category, specificity)
		print 'Coverage for category:%s is %s' % (each_category, coverage)
		if coverage >= ec and specificity >= es:
			result_categories += classify(each_category, database_url, ec, es)

	if not result_categories:
		return [category]
	return result_categories


def main():
	if len(sys.argv) != 4:
		print sys.argv
		print 'arguments wrong'
		sys.exit()
	load_cache()
	load_db_info()
	get_queries()
	es = float(sys.argv[1])
	ec = float(sys.argv[2])
	database_url = sys.argv[3]
	print 'Classifying...'
	classification_result = classify('Root', database_url, ec, es)
	print 'Classification:'
	print classification_result

if __name__ == '__main__':
	main()

