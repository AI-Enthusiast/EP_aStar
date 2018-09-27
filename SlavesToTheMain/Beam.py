# Beam.py created for solving the 8-puzzle problem and TicTacToe
# DateCreated: 9/21/18
# Author: Cormac Dacker (cxd289)
from SlavesToTheMain import TicTacToe as ttt
from SlavesToTheMain import EightPuzzle as ep


def error(errorMessage):
    print("> ERROR: " + str(errorMessage))


# TODO finish Beam
class Beam:

    # Constructor
    # Params: puzzle(the puzzle being solved), k(number of states being kept track of)
    def __init__(self, puzzle, k=35):
        self.K = int(k)
        self.beam(puzzle)  # print aStar solution

    def f(self, puzzle):
        if type(puzzle) is ep.EightPuzzle:
            return puzzle.euclidianDist() + puzzle.inversions()
        elif type(puzzle) is ttt.TicTacToe:
            return puzzle.numLinesOpen() + puzzle.Depth

    def beam(self, puzzle):
        children = []  # nodes to visit, nodes to not visit
        open = [(self.f(puzzle),
                 puzzle)]  # type: List[tuple(int, ep.EightPuzzle)] or List[[tuple(int, ttt.TicTacToe)]] # childern of that branch
        openStates = {}
        while True:  # work toward the goal
            open.sort()
            for state in range(len(open)):
                openStates[open[state][1].State] = open[state][1]

            try:
                if open[0][1].isGoal():  # if the top puzzle is the goal state
                    open[0][1].generateSolutionPath()  # goal has been achieved
                    break
            except IndexError as e:
                error(str(e) + "K param too low, please increase.")
                break

            while len(open) > 0:  # while there are still nodes to expand in open
                i=len(open)
                newBranch = open[0][1].move(0) #adds the puzzle to newbranch
                for branch in range(len(newBranch)):
                    if newBranch[branch].State not in openStates: # if it's a new branch
                        children.append(newBranch[branch])  # append all it's potential moves to chldren

                open.remove(open[0])  # remove it from open
            temp = []
            for child in range(len(children)):
                temp.append((self.f(children[child]), children[child]))

            while len(temp) > self.K:  # remove children untill it's k size
                temp.sort(reverse=False)
                temp.pop()[1] # remove worst branches untill it's K size
            for puzzle in range(len(temp)):
                open.append(temp[puzzle]) # add to open
            children = [] #reset
            openStates={} #reset


if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()
