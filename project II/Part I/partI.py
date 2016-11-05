import base64
import urllib2
import urllib

query_dict = {}
category_dict = {'Root':['Computers', 'Health', 'Sports'], 'Computers':['Hardware', 'Programming'], \
	'Health':['Fitness', 'Diseases'], 'Sports':['Basketball', 'Soccer']}

def generate_url(query_word, site):
	valid_query = urllib.quote(query_word)
	url = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%27site%3a'+site+ '%20' + valid_query + '%27&$top=1&$format=Atom'
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

def classify(database_url):
	pass

if __name__ == '__main__':
	# get_queries()
	# print len(query_dict)
	print get_page(generate_url('blood heart ', 'diabetes.org'))
