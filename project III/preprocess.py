# These lines store the mapping between restaurant name and their problems.
rest_dict = {}

for line in open('DOHMH_New_York_City_Restaurant_Inspection_Results.csv'):
	line_list = line.split(',')

	# Removes incomplete lines to increse confidence.
	if line_list[10] == '':
	 	continue
	if not line_list[0] in rest_dict:
		#rest_dict[line_list[0]] = set([line_list[2], line_list[7], line_list[10]])
		#rest_dict[line_list[0]] = set([line_list[7], line_list[10]])
		rest_dict[line_list[0]] = set([line_list[10]])
	else:
		#rest_dict[line_list[0]].add(line_list[2])
		#rest_dict[line_list[0]].add(line_list[7])
		rest_dict[line_list[0]].add(line_list[10])

target_file = open('New_York_City_Restaurant_Inspection_Results_Concern.csv', 'w')
for restaurant in rest_dict.keys():

	# We only concern restaurants who has no less than 10 problems to 
	# dig their assocation rules.
	if len(rest_dict[restaurant]) < 5:
		continue
	target_file.write('%s\n' % (','.join(list(rest_dict[restaurant]))))

target_file.close()