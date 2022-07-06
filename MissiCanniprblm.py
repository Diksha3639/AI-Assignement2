class MissiCanni:
    ### MC is missionaries and cannibals
    def __init__(self, state_vars, num_moves=0, parent=None):
        self.state_vars = state_vars
        self.num_moves = num_moves
        self.parent = parent


    @classmethod
    def root(cls):
        return cls((3, 3, 1))

    def get_possible_moves(self):
        
        ''' return all possible moves in the game as tuples possible moves:
            1 or 2 missionaries
            1 or 2 cannibals
            1 missionary , 1 cannible
        '''

        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        return moves

    def is_valid(self):
        missionaries = self.state_vars[0]
        cannibals = self.state_vars[1]


        if missionaries < 0 or missionaries > 3:
            return False
        elif cannibals < 0 or cannibals > 3:
            return False
        return True

    def is_solution(self):
        if self.state_vars == (0, 0, 0):
            return True
        return False

    def is_failure(self):
        missionaries = self.state_vars[0]
        cannibals = self.state_vars[1]
        boat = self.state_vars[2]

        if missionaries > 0 and missionaries < cannibals:
            return True


        missionaries_on_left = 3 - missionaries
        cannibals_on_left = 3 - cannibals

        if missionaries_on_left > 0 and missionaries_on_left < cannibals_on_left:
            return True



        return False

    def get_next_states(self):
        ## using possible move, get next states

        moves = self.get_possible_moves()
        all_states = list()
        mis_right, can_right, raft_right = self.state_vars
        ## if raft is on right, subtract move from these numbers
        ## if raft is on left, add these move numbers to these numbers
        for move in moves:
            change_mis, change_can = move
            if raft_right == 1:  ## mis_right = 3; can_right = 3, raft_right = 1
                new_state_vars = (mis_right - change_mis, can_right - change_can, 0)
            else:
                new_state_vars = (mis_right + change_mis, can_right + change_can, 1)


            new_state = MissiCanni(new_state_vars, self.num_moves + 1, self)
            if new_state.is_valid():
                all_states.append(new_state)

        return all_states

    def __str__(self):
        return "MCState[{}]".format(self.state_vars)

    def __repr__(self):
        return str(self)


def search(dfs=True):

    from collections import deque

    #creating the root state
    root = MissiCanni.root()

    ### we use the stack/queue for keeping track of where to search next
    to_search = deque()

    ### use a set to keep track fo where we've been
    seen_states = set()

    ### use a list to keep track of the solutions that have been seen
    solutions = list()

    ### start the search with the root
    to_search.append(root)

    ### safety variable for infinite loops!
    loop_count = 0
    max_loop = 10000

    ### while the stack/queue still has items
    while len(to_search) > 0:
        loop_count += 1
        if loop_count > max_loop:
            print(len(to_search))
            print("Escaping this super long loop!")
            break

        ### get the next item
        current_state = to_search.pop()


        next_states = current_state.get_next_states()


        for possible_next_state in next_states[::-1]:


            possible_state_vars = possible_next_state.state_vars


            if possible_state_vars not in seen_states:

                if possible_next_state.is_failure():

                    continue
                elif possible_next_state.is_solution():
                    solutions.append(possible_next_state)
                    continue

                if dfs:
                    to_search.append(possible_next_state)
                else:
                    to_search.appendleft(possible_next_state)

                seen_states.add(possible_state_vars)

    ## finally, we reach this line when the stack/queue is empty (len(to_searching==))

    print("Found {} solutions".format(len(solutions)))
    return solutions


sol_dfs = search(True)
sol_bfs = search(False)

current_state = sol_dfs[0]
while current_state:
    print(current_state)
    current_state = current_state.parent


print("--")
current_state = sol_dfs[1]
while current_state:
    print(current_state)
    current_state = current_state.parent

print("--")
current_state = sol_bfs[0]
while current_state:
    print(current_state)
    current_state = current_state.parent


print("--")
current_state = sol_bfs[1]
while current_state:
    print(current_state)
    current_state = current_state.parent