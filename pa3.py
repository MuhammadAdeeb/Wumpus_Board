# TODO import the necessary classes and methods
import sys
# from logic import *
from logic import *
from utils import *

'''
-def to_cnf(s) # string
-class propKb()
-class Expr()
-def expr()
-def symbol()
'''

if __name__ == '__main__':

	'''
	wumpus_kb = PropKB()

	P11, P12, P21, P22, P31, B11, B21 = expr('P11, P12, P21, P22, P31, B11, B21')
	wumpus_kb.tell(~P11)
	wumpus_kb.tell(B11 | '<=>' | (P12 | P21))
	wumpus_kb.tell(B21 | '<=>' | (P11 | P22 | P31))
	wumpus_kb.tell(~B11)
	wumpus_kb.tell(B21)

	# print(wumpus_kb.clauses)
	# print(tt_entails(Expr('&', *wumpus_kb.clauses), P31))
	# print(wumpus_kb.ask_if_true(~B21))
	'''
	input_file = sys.argv[1]
	# input_file = "test.txt"
	read_file = open(input_file, 'r')
	read_file = read_file.readlines()

	# print(read_file)
	size = read_file[2]  # line with size of the board
	size = size[:len(size)-1]  # size of the board w/o '\n'
	row = int(size[0])  # row in the size string
	column = int(size[2])  # col in the size string
	# print("row: ", row, "   Column: ", column )
	# print(size)

	lst = [[], []]  # lst of lsts, where 1st lst has provided KB and 2nd lst has the queries
	i = 0  			# used to differentiate b/w 2 lists in lst
	for x in range(3, len(read_file)-1):  # to break apart KB and Queries and add it to lst
		# print(read_file[x])
		if 'Query' in read_file[x]:  # increment the lst counter
			i += 1
		if '#' not in read_file[x]:  # if it's not a comment append it w/o the '\n' at the end
			lst[i].append(read_file[x][:len(read_file[x])-1])
	lst[1].append(read_file[len(read_file)-1])

	# print("lst: ", lst)
	# print(size)
	# print(lst)

	kb = PropKB()

	mines_lst = []
	beep_list = []
	rules_list = []

	for x in lst[0]:
		kb.tell(x)
	# print(kb.clauses)

	for i in range(column):  # Column impacts x axis vals
		for j in range(row): # Row impacts y axis vals
			B = 'B' + str(i) + str(j)
			M = 'M' + str(i) + str(j)
			beep_list.append(B)
			mines_lst.append(M)

			if i == 0:  	# when x == 0
				if j == 0:  # x = 0, y = 0; corner piece
					kb.tell(to_cnf((expr(B) | '<=>' | (expr('M' + str(i + 1) + str(j)) | expr('M' + str(i) + str(j + 1))))))
				elif j == row - 1:  # x = 0, y = max_val; corner piece
					kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i) + str(j - 1)) | expr('M' + str(i + 1) + str(j)))))
				else:  # x = 0, y = (0, max_val)
					kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i) + str(j+1)) | expr('M' + str(i) + str(j-1)) | expr('M' + str(i+1) + str(j)))))
			elif i == column - 1:  # x = max_val
				if j == 0:  # x = max_val, y = 0; corner piece
					kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i - 1) + str(j)) | expr('M' + str(i) + str(j + 1)))))
				elif j == row - 1:  # x = max_val, y = max_val; corner piece
					kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i) + str(j - 1)) | expr('M' + str(i - 1) + str(j)))))
				else:  # x = max_val, y = (0, max_val)
					kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i) + str(j+1)) | expr('M' + str(i) + str(j-1)) |
											   expr('M' + str(i-1) + str(j)))))
			elif j == 0:  # y = 0, x = (0, max_val)
				kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i-1) + str(j)) | expr('M' + str(i+1) + str(j)) |
										   expr('M' + str(i) + str(j+1)))))

			elif j == row - 1:  # y = max_val, x = (0, max_val)
				kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i-1) + str(j)) | expr('M' + str(i+1) + str(j)) |
										   expr('M' + str(i) + str(j-1)))))
			else: # everything other than the side/corner squares
				kb.tell(to_cnf(expr(B) | '<=>' | (expr('M' + str(i-1) + str(j)) | expr('M' + str(i+1) + str(j)) | expr('M' + str(i) + str(j-1) | expr('M' + str(i) + str(j+1))))))

	# print("Mines_lst: ", mines_lst)
	# print("Beep_lst: ", beep_list)
	# print("kb_clauses: ", kb.clauses)
	# for every query, create an expression and pass it to tt_entails to see if kb entails query

	for q in lst[1]:
		# print(q)
		a = tt_entails(Expr('&', *kb.clauses), expr(q))  # Returns True/False and need to print Yes/No:
		# a = pl_resolution(kb, expr(q))
		if a:
			print('Yes')
		else:
			print('No')
