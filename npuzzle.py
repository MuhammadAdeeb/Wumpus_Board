from search import *  # TODO import the necessary classes and methods
import sys


class NPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal, n):
        self.n = n
        super().__init__(initial, goal)

    """ Define goal state and initialize a problem """

    # self.initial = initial
    # self.goal = goal
    # self.n = n

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % self.n == 0:
            possible_actions.remove('LEFT')
        if index_blank_square % self.n == self.n-1:
            possible_actions.remove('RIGHT')
        if index_blank_square < self.n:
            possible_actions.remove('UP')
        if index_blank_square > (self.n * self.n - self.n - 1):
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -1 * self.n, 'DOWN': self.n, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


if __name__ == '__main__':

    input_file = sys.argv[1]
    search_algo_str = sys.argv[2]
    # input_file = "C:\Users\muham\Desktop\Fall 2020\ Intro to AI, CS 480\Assignments\pa1\puzzle.txt"

    search_algs = {"DFTS": depth_first_tree_search, "DFGS": depth_first_graph_search, "BFTS": breadth_first_tree_search,
                   "BFGS": breadth_first_graph_search, "UCTS": uniform_cost_search,
                   "UCGS": uniform_cost_search, }  # UCTS

    search_algs_2 = {"GBFTS": best_first_graph_search,  # GBFTS
                     "GBFGS": best_first_graph_search, "ASTS": astar_search, "ASGS": astar_search}  # ASTS
    # For GBFGS specify f = h(n)

    local_test_file = open(input_file, "r")
    all_lines = local_test_file.readlines()

    np_line_list = []  # Lines from the text file
    # fill up np_line_list
    for x in range(len(all_lines)):
        if all_lines[x][0] != '#':
            if all_lines[x][len(all_lines[x]) - 1] == 'n':
                np_line_list.append(all_lines[x][:len(all_lines[x]) - 1])
            else:
                np_line_list.append(all_lines[x])

    n = len(np_line_list)
    state_tup = []  # Current state of npuzzle
    # fill up state_tup state
    for y in range(n):
        y = np_line_list[y].split(' ')
        for char in y:
            state_tup.append(int(char))
    state_tup = tuple(state_tup)
    # print(state_tup)

    goal_tup = []
    # fill up goal tup state
    for x in range(n * n):
        goal_tup.append(x)
    goal_tup = tuple(goal_tup)
    # print(goal_tup)
    puzz_prob = NPuzzle(state_tup, goal_tup, n)

    # puzz_prob = EightPuzzle((0,1,2,3,4,5,6,7,8))

    # search_algo_str = "GBFGS"
    # print(puzz_prob.check_solvability(state_tup))
    if search_algo_str in search_algs:
        goal_node = search_algs[search_algo_str](
            puzz_prob)  # TODO call the appropriate search function with appropriate parameters
    else:
        goal_node = search_algs_2[search_algo_str](puzz_prob, puzz_prob.h)

# TODO implement
    if goal_node is not None:
        print("Solution path", goal_node.solution())
        print("Solution cost", goal_node.path_cost)
    else:
        print("No solution was found.")
'''
goal_node = ... # TODO call the appropriate search function with appropriate parameters

# Do not change the code below.

'''