# These lines store the mapping between restaurant name and their problems.
rest_dict = {}

for line in open('New_York_City_Restaurant_Inspection_Results.csv'):
	line_list = line.split(',')

	# Removes incomplete lines to increse confidence.
	if '' in line_list:
		continue
	if not line_list[1] in rest_dict:
		rest_dict[line_list[1]] = set([line_list[10]])
	else:
		rest_dict[line_list[1]].add(line_list[10])

target_file = open('New_York_City_Restaurant_Inspection_Results_Concern.csv', 'w')
for restaurant in rest_dict.keys():

	# We only concern restaurants who has no less than 10 problems to 
	# dig their assocation rules.
	if len(rest_dict[restaurant]) < 10:
		continue
	target_file.write('%s\n' % (','.join(list(rest_dict[restaurant]))))

target_file.close()