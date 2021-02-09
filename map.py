# import search
from search import *  # TODO import the necessary classes and methods
import sys


if __name__ == '__main__':
	
	input_file = sys.argv[1]
	search_algo_str = sys.argv[2]

	search_algs = {"DFTS": depth_first_tree_search, "DFGS": depth_first_graph_search, "BFTS": breadth_first_tree_search,
				"BFGS": breadth_first_graph_search, "UCTS": uniform_cost_search,
				"UCGS": uniform_cost_search, }  # UCTS

	search_algs_2 = {"GBFTS": best_first_graph_search,  # GBFTS
				"GBFGS": best_first_graph_search, "ASTS": astar_search, "ASGS": astar_search}  # ASTS
				# For GBFGS specify f = h(n)

	local_test_file = open(input_file, "r")
	all_lines = local_test_file.readlines()

	info_list = []
	sg_list = []
	h_list = []
	check = True

	# Dividing data from files into 3 lists: info_list, sg_list(start & Goal), h_list(heauristic)
	for x in range(len(all_lines)):
		if x != (len(all_lines)-1):
			all_lines[x] = all_lines[x][:len(all_lines[x])-1]
		if all_lines[x][0] != "#":
			if '>' in all_lines[x]:
				info_list.append(all_lines[x])
			elif check:
				sg_list.append(all_lines[x])
				check = False
			else:
				h_list.append(all_lines[x])

	# Creating a graph dict to organize data from info_list (All possible actions from a pt and their cost)
	graph = {}
	for i in range(len(info_list)):
		# if info_list[i] in graph:
		if '<>' in info_list[i]:
			if info_list[i][0] in graph:
				graph[info_list[i][0]][info_list[i][2]] = int(info_list[i][len(info_list[i])-1]) #.append([info_list[i][2], info_list[i][len(info_list[i])-1]])
			else:
				graph[info_list[i][0]] = {info_list[i][2]: int(info_list[i][len(info_list[i])-1])}

			if info_list[i][2] in graph:
				graph[info_list[i][2]][info_list[i][0]] = int(info_list[i][len(info_list[i])-1]) # .append([info_list[i][0], info_list[i][len(info_list[i])-1]])
			else:
				graph[info_list[i][2]] = {info_list[i][0]: int(info_list[i][len(info_list[i])-1])}
		else:
			if info_list[i][0] in graph:
				graph[info_list[i][0]][info_list[i][2]] = int(info_list[i][len(info_list[i])-1]) #   .append([info_list[i][2], info_list[i][len(info_list[i])-1]])
			else:
				graph[info_list[i][0]] = {info_list[i][2]: int(info_list[i][len(info_list[i])-1])}

	# Created h_dict(heuristic) w/ key being a location and its val being the H
	h_dict = {}
	for x in range(len(h_list)):
		h_dict[h_list[x][0]] = int(h_list[x][2])

	print("H_DICT: ", h_dict)
	# print()
	search_graph = Graph(graph)

	# create a problem object to pass to the search algorithms
	gp = GraphProblem(sg_list[0][0], sg_list[0][2], search_graph)

	def h_func(n):
		return h_dict[n.state]

	# TODO implement
	############################
	if search_algo_str in search_algs:
		goal_node = search_algs[search_algo_str](gp)  # TODO call the appropriate search function with appropriate parameters
	else:
		goal_node = search_algs_2[search_algo_str](gp, h_func)

	# Do not change the code below.
	if goal_node is not None:
		print("Solution path", goal_node.solution())
		print("Solution cost", goal_node.path_cost)
	else:
		print("No solution was found.")
