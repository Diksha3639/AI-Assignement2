#!/usr/bin/python
 
import random,sys,copy
from optparse import OptionParser
try:
  import psyco
  
  psyco.full()
except ImportError:
  pass
 
"""
cowboy code, but seems to work
USAGE: python prog <numberruns=1> <verbocity=False>
"""
 
class puzzle:
  def __init__(self, list=None):
    if list == None:
      self.puzzle = [[0 for i in range(0,8)] for j in range(0,8)]
      #initialize queenprblm at random places
      for i in range(0,8):
        while 1:
          rand_row = random.randint(0,7)
          rand_col = random.randint(0,7)
          if self.puzzle[rand_row][rand_col] == 0:
            self.puzzle[rand_row][rand_col] = "Q"
            break
    #TODO raise errors if puzzle is not right format or dimension
  #define how to print the puzzle
  def __repr__(self):
    mstr = ""
    for i in range(0,8):
      for j in range(0,8):
        mstr = mstr + str(self.puzzle[i][j]) + " "

      mstr = mstr + "n"
    return (mstr)
 
class queenprblm:
  def __init__(self, numruns, verbocity, passedpuzzle=None):
    #TODO check options
    self.totalruns = numruns
    self.totalsucc = 0
    self.totalnumsteps = 0
    self.verbocity = verbocity
    for i in range(0,numruns):
      if self.verbocity == True:
        print ("====================")
        print ("puzzle",i)
        print ("====================")
      self.mpuzzle = puzzle(passedpuzzle)
      self.cost = self.calc_cost(self.mpuzzle)
      self.hill_solution()
 
  def hill_solution(self):
    while 1:
      currViolations = self.cost
      self.getlowercostpuzzle()
      if currViolations == self.cost:
        break
      self.totalnumsteps += 1
      if self.verbocity == True:
        print ("puzzle Violations", self.calc_cost(self.mpuzzle))

        print (self.mpuzzle)
    if self.cost != 0:
      if self.verbocity == True:
        print ("SOLUTION NOT FOUND!")
    else:
      if self.verbocity == True:
        print ("SOLUTION FOUND!")

      self.totalsucc += 1
    return self.cost
 
  def printstats(self):
    print ("Total Runs: ", self.totalruns)
    print ("Total Success: ", self.totalsucc)
    print ("Success %: ", float(self.totalsucc)/float(self.totalruns))
    print ("Average no. Of steps: ", float(self.totalnumsteps)/float(self.totalruns))
 
  def calc_cost(self, tpuzzle):
    #these are separate for easier debugging
    totalhcost = 0
    totaldcost = 0
    for i in range(0,8):
      for j in range(0,8):
        #if this node is a queenprblm, calculate all violations
        if tpuzzle.puzzle[i][j] == "Q":
          #subtract 2 so don't count self
          #sideways and vertical
          totalhcost -= 2
          for k in range(0,8):
            if tpuzzle.puzzle[i][k] == "Q":
              totalhcost += 1
            if tpuzzle.puzzle[k][j] == "Q":
              totalhcost += 1
          #calculate diagonal violations
          k, l = i+1, j+1
          while k < 8 and l < 8:
            if tpuzzle.puzzle[k][l] == "Q":
              totaldcost += 1
            k +=1
            l +=1
          k, l = i+1, j-1

          while k < 8 and l >= 0:
            if tpuzzle.puzzle[k][l] == "Q":
              totaldcost += 1
            k +=1
            l -=1
          k, l = i-1, j+1
          while k >= 0 and l < 8:
            if tpuzzle.puzzle[k][l] == "Q":
              totaldcost += 1
            k -=1
            l +=1
          k, l = i-1, j-1

          while k >= 0 and l >= 0:
            if tpuzzle.puzzle[k][l] == "Q":
              totaldcost += 1
            k -=1
            l -=1
    return ((totaldcost + totalhcost)/2)
 
  #this function tries moving every queenprblm to every spot, with only one move
  #and returns the move that has the leas number of violations
  def getlowercostpuzzle(self):
    lowcost = self.calc_cost(self.mpuzzle)
    lowestavailable = self.mpuzzle

    #move one queenprblm at a time, brute force move the optimal single 
    for q_row in range(0,8):
      for q_col in range(0,8):
        if self.mpuzzle.puzzle[q_row][q_col] == "Q":
          #get the lowest cost by moving this queenprblm
          for m_row in range(0,8):
            for m_col in range(0,8):
              if self.mpuzzle.puzzle[m_row][m_col] != "Q":
                
                #try placing the queenprblm here and see if it's any better
                trypuzzle = copy.deepcopy(self.mpuzzle)
                trypuzzle.puzzle[q_row][q_col] = 0
                trypuzzle.puzzle[m_row][m_col] = "Q"
                thiscost = self.calc_cost(trypuzzle)
                if thiscost < lowcost:
                  lowcost = thiscost
                  lowestavailable = trypuzzle
    self.mpuzzle = lowestavailable
    self.cost = lowcost
 
if __name__ == "__main__":
 
  parser = OptionParser()
  parser.add_option("-q", "--quiet", dest="verbose",
                   action="store_false", default=True,
                   help="Don't print all the moves... wise option if using large numbers")
 
  parser.add_option("--numrun", dest="numrun", help="Number of random puzzles", default=1,
                   type="int")
 
  (options, args) = parser.parse_args()
 
  mpuzzle = queenprblm(verbocity=options.verbose, numruns=options.numrun)
  mpuzzle.printstats()