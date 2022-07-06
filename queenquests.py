#!/usr/bin/python

import random, sys, copy
from optparse import OptionParser

try:
    import psyco

    psyco.full()
except ImportError:
    pass


class chess:
    def __init__(self, list=None):
        if list == None:
            self.chess = [[0 for i in range(0, 8)] for j in range(0, 8)]
            # initialize queenquests at random places
            for i in range(0, 8):
                while 1:
                    row = random.randint(0, 7)
                    col = random.randint(0, 7)
                    if self.chess[row][col] == 0:
                        self.chess[row][col] = "Q"
                        break
        # TODO raise errors if board is not right format or dimension

# define how to print the board
    def __repr__(self):
        mstr = ""
        for i in range(0, 8):
            for j in range(0, 8):
                mstr = mstr + str(self.chess[i][j]) + " "
            mstr = mstr + "n"
        return (mstr)


class queenquest:
    def __init__(self, numruns, verbocity, passedboard=None):
        # TODO check options
        self.truns = 1000
        self.tsucc = 0
        self.totalnumsteps = 0
        self.verbocity = verbocity
        for i in range(0, 1000):
            if self.verbocity == True:
                print("Number of moves on the board", i)
            self.mboard = chess(passedboard)
            self.cost = self.calc_cost(self.mboard)
            self.hill_climbing_solution()

    def hill_climbing_solution(self):
        while 1:
            currViolations = self.cost
            self.getlowercostboard()
            if currViolations == self.cost:
                break

            self.totalnumsteps += 1
            if self.verbocity == True:
                print("Board Violations", self.calc_cost(self.mboard))
                print(self.mboard)
        if self.cost != 0:
            if self.verbocity == True:
                print("SOLUTION NOT FOUND")
        else:
            if self.verbocity == True:
                print("SOLUTION FOUND")
            self.tsucc += 1

        return self.cost

    def output(self):
        print("The total number of runs: ", self.truns)
        print("The total success rate : ", self.tsucc)
        print("The total success percentage: ", 100 - float(self.tsucc) * 100 / float(self.truns))
        print("The total failure percentage: ", float(self.tsucc) * 100 / float(self.truns))
        print("The average number of steps: ", float(self.totalnumsteps) / float(self.truns))

    def calc_cost(self, tboard):
        # these are separate for easier debugging
        totalhcost = 0
        totaldcost = 0
        for i in range(0, 8):
            for j in range(0, 8):
                # if this node is a queenquest, calculate all violations
                if tboard.chess[i][j] == "Q":
                    # subtract 2 so don't count self sideways and vertical
                    totalhcost -= 2
                    for k in range(0, 8):
                        if tboard.chess[i][k] == "Q":
                            totalhcost += 1
                        if tboard.chess[k][j] == "Q":
                            totalhcost += 1
                    # calculate diagonal violations
                    k, l = i + 1, j + 1
                    while k < 8 and l < 8:
                        if tboard.chess[k][l] == "Q":
                            totaldcost += 1
                        k += 1
                        l += 1
                    k, l = i + 1, j - 1
                    while k < 8 and l >= 0:
                        if tboard.chess[k][l] == "Q":
                            totaldcost += 1
                        k += 1
                        l -= 1
                    k, l = i - 1, j + 1
                    while k >= 0 and l < 8:
                        if tboard.chess[k][l] == "Q":
                            totaldcost += 1
                        k -= 1
                        l += 1
                    k, l = i - 1, j - 1
                    while k >= 0 and l >= 0:
                        if tboard.chess[k][l] == "Q":
                            totaldcost += 1
                        k -= 1
                        l -= 1
        return ((totaldcost + totalhcost) / 2)

    # this function tries moving every queenquest to every spot, with only one move and returns the move
    # that has the leas number of violations

    def getlowercostboard(self):
        lowcost = self.calc_cost(self.mboard)
        lowestavailable = self.mboard
        # move one queenquest at a time, the optimal single move by brute force
        for q_row in range(0, 8):
            for q_col in range(0, 8):
                if self.mboard.chess[q_row][q_col] == "Q":
                    # get the lowest cost by moving this queenquest
                    for m_row in range(0, 8):
                        for m_col in range(0, 8):
                            if self.mboard.chess[m_row][m_col] != "Q":
                                # try placing the queenquest here and see if it's any better
                                tryboard = copy.deepcopy(self.mboard)
                                tryboard.chess[q_row][q_col] = 0
                                tryboard.chess[m_row][m_col] = "Q"
                                thiscost = self.calc_cost(tryboard)
                                if thiscost < lowcost:
                                    lowcost = thiscost
                                    lowestavailable = tryboard
        self.mboard = lowestavailable
        self.cost = lowcost


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-q", "--quiet", dest="verbose",
                      action="store_false", default=False,
                      help="Don't print all the moves... wise option if using large numbers")

    parser.add_option("--numrun", dest="numrun", help="Number of random Boards", default=1000,
                      type="int")

    (options, args) = parser.parse_args()

    mboard = queenquest(verbocity=options.verbose, numruns=options.numrun)
    mboard.output()