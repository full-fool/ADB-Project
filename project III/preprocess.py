import csv
# These lines store the mapping between restaurant name and their problems.
rest_dict = {}

f = open('New_York_City_Restaurant_Inspection_Results.csv', 'rb') # opens the csv file
try:
    reader = csv.reader(f)  # creates the reader object
    for line_list in reader:   # iterates the rows of the file in orders

		if not line_list[1] in rest_dict:
			rest_dict[line_list[1]] = set([line_list[10]])
		else:
			rest_dict[line_list[1]].add(line_list[10])



finally:
    f.close()     


target_file = open('New_York_City_Restaurant_Inspection_Results_Concern.csv', 'w')
for restaurant in rest_dict.keys():

	# We only concern restaurants who has no less than 10 problems to 
	# dig their assocation rules.
	if len(rest_dict[restaurant]) < 10:
		continue
	target_file.write('%s\n' % (','.join(list(rest_dict[restaurant]))))

target_file.close()