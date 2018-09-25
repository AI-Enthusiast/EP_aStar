# Beam.py created for solving the 8-puzzle problem and TicTacToe
# DateCreated: 9/21/18
# Author: Cormac Dacker (cxd289)
from SlavesToTheMain import TicTacToe as ttt
from SlavesToTheMain import EightPuzzle as ep
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))

#TODO finish Beam
class Beam:

    # Constructor
    # Params: puzzle(the puzzle being solved), k(number of states being kept track of)
    def __init__(self, puzzle, k=3, first=1):
        self.K = k
        self.First = first
        self.beam(puzzle)  # print aStar solution

    def chooseBranch(self, open):
        print("TEMP")

    def beam(self, puzzle):
        goal = False
        open, closed = [], {}  # nodes to visit, nodes to not visit

        if puzzle.isGoal():  # if the current puzzle is the goal state
            puzzle.generateSolutionPath()  # goal has been achieved
        else:  # work toward the goal
            open.append(puzzle)  # add the starting puzzle to open

            while open is not None:  # while there are still nodes to expand in open
                branch = self.chooseBranch(open) # choose best branch
                closed[branch.State] = branch  # add the chosen branch to the closed table
                open.remove(branch)  # remove the branch from open
                set = None  # the empty set

                for state in open:
                    successors = open[state].move()
                    for stem in range(len(successors)):
                        print("TEMP")

if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()