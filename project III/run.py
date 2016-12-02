import sys

class Solution(object):
	def __init__(self):
		self.min_sup = None
		self.min_conf = None
		self.file_name = None

		# item_list stores a list of set, each set represents a market basket
		self.item_list = None

	def set_params(self, file_name, min_sup, min_conf):
		self.file_name = file_name
		self.min_sup = float(min_sup)
		self.min_conf = float(min_conf)

	def load_data(self):
		self.item_list = []
		for line in open(self.file_name):
			if line == '\n':
				continue
			line = line.strip()
			if line[-1] == ',':
				self.item_list.append(set(line[:-1].split(',')))
			else:
				self.item_list.append(set(line.split(',')))

	# The main process function of this program. Calculate the large item set and the corresponding 
	# assocation rule, and write it to output.txt.
	def process(self):
		item_list = self.item_list
		total_line = len(item_list)
		counter_dict = {}
		sup_dict = {}
		one_item_set = []
		file_handler = open('output.txt', 'w')
		file_handler.write('==Frequent itemsets (min_sup=%s)\n' % self.min_sup)
		for i in range(len(item_list)):
			item_list[i] = set(item_list[i])
			for item in item_list[i]:
				if not [item] in one_item_set:
					one_item_set.append([item])
				if tuple([item]) in counter_dict:
					counter_dict[tuple([item])] += 1
				else:
					counter_dict[tuple([item])] = 1

		one_item_set_new = []
		for each_item in one_item_set:
			crr_sup = float(counter_dict[tuple(each_item)]) / float(total_line)
			if crr_sup >= self.min_sup:
				# file_handler.write('[%s],%s\n' % (','.join(each_item), crr_sup))
				one_item_set_new.append(each_item)
				sup_dict[tuple(each_item)] = crr_sup				

		res_item_set = one_item_set_new
		crr_item_set = one_item_set_new
		while crr_item_set:
			new_item_set = self.apriori_gen(crr_item_set)
			for each_basket in item_list:
				tmp_item_list = self.subset(new_item_set, each_basket)
				for each_tmp_item in tmp_item_list:
					if tuple(each_tmp_item) in counter_dict:
						counter_dict[tuple(each_tmp_item)] += 1
					else:
						counter_dict[tuple(each_tmp_item)] = 1
			for each_item in new_item_set:
				crr_sup = float(counter_dict[tuple(each_item)]) / float(total_line)
				if crr_sup >= self.min_sup:
					res_item_set.append(each_item)
					sup_dict[tuple(each_item)] = crr_sup				
			
			crr_item_set = new_item_set

		sup_dict = sorted(sup_dict.items(), key=lambda d:d[1], reverse = True)
		for item in sup_dict:
			file_handler.write('[%s],%s\n' % (','.join(list(item[0])), item[1]))


		file_handler.write('\n\n==High-confidence association rules (min_conf=%s)\n' % self.min_conf)
		association_rule_dict = {}
		for each_item_set in sup_dict:
			item_set = list(each_item_set[0])
			if len(item_set) == 1:
				continue
			for i in range(len(item_set)):
				target = item_set[i]
				left_part = item_set[:i] + item_set[i+1:]
				crr_conf = float(counter_dict[tuple(item_set)]) / float(counter_dict[tuple(left_part)])
				if crr_conf >= self.min_conf:
					print crr_conf, self.min_conf, tuple(left_part + [target])

					association_rule_dict[tuple(left_part + [target])] = crr_conf
		
		association_rule_dict = sorted(association_rule_dict.items(), key=lambda d:d[1], reverse = True)
		for item in association_rule_dict:
			item_set = list(item[0])
			fst_pt = item_set[:-1]
			snd_pt = item_set[-1]
			item_set = sorted(item_set)
			conf = item[1]
			supp = float(counter_dict[tuple(item_set)]) / float(total_line)
			file_handler.write('[%s] => [%s] (Conf: %s, Supp: %s)\n' % (','.join(fst_pt), snd_pt, conf, supp))

		file_handler.close()



	# Params: item_set, represents a item set, is a list of list
	#         basket, represents a market basket
	# Return: a list of list, represents all items in item_set which in 
	#         contained in current basket
	def subset(self, item_set, basket):
		result_list = []
		for each_item in item_set:
			if set(each_item) - basket == set([]):
				result_list.append(each_item)
		return result_list

	# Params: item_set, represents a item set, whose items have the same k length.
	# 		  Assume these items in each item_set are sorted in lexicographic order.
	# Return: a new item_set whose items have the same k+1 length.
	def apriori_gen(self, item_set):
		if len(item_set) <= 1:
			return []
		k = len(item_set[0])
		item_num = len(item_set)
		tmp_list = []
		res_list = []
		for i in range(item_num-1):
			for j in range(i+1, item_num):
				if item_set[i][:-1] == item_set[j][:-1] and item_set[i][-1] != item_set[j][-1]:
					new_item = item_set[i] + [item_set[j][-1]]
					if not new_item in tmp_list:
						tmp_list.append(new_item)
		for each_item_set in tmp_list:
			valid = True
			for i in range(len(each_item_set)):
				sub_item_set = each_item_set[:i] + each_item_set[i+1:]
				if not sub_item_set in item_set:
					valid = False
					break
			if valid:
				each_item_set.sort()
				res_list.append(each_item_set)
		return res_list


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print 'arg number wrong'
		sys.exit()

	sol = Solution()
	sol.set_params(sys.argv[1], sys.argv[2], sys.argv[3])
	sol.load_data()
	sol.process()










