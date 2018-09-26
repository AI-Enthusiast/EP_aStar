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
        self.K = int(k)
        self.First = first
        self.beam(puzzle)  # print aStar solution

    def f(self, puzzle):
        if type(puzzle) is ep.EightPuzzle:
            return puzzle.euclidianDist() + puzzle.Depth
        elif type(puzzle) is ttt.TicTacToe:
            return puzzle.h1() + puzzle.Depth

    def chooseBranch(self, open,closed):
        funcHeap=[]
        for branch in range(len(open)):  # build the queue
            if str(open[branch].State) not in closed:
                funcHeap.append((self.f(open[branch]), open[branch]))  # pushes info to the queue
        funcHeap.sort(reverse=True)
        return funcHeap

    def beam(self, puzzle):
        goal = False
        open, closed = [], {}  # nodes to visit, nodes to not visit
        children = []# type: List[ep.EightPuzzle] or List[ttt.TicTacToe] # get childern of that branch
        if puzzle.isGoal():  # if the current puzzle is the goal state
            puzzle.generateSolutionPath()  # goal has been achieved
        else:  # work toward the goal
            open.append(puzzle)  # add the starting puzzle to open
            while True:
                while open is not None:  # while there are still nodes to expand in open
                    stems = (self.chooseBranch(open,closed)) # type: List[ep.EightPuzzle] or List[ttt.TicTacToe] # get childern of that branch
                    for i in range(len(stems)):
                        children.append(stems[i])
                    closed[children[0].State] = children[0] # add the chosen branch to the closed table
                    open.remove(children[0])  # remove the branch from open
                    if branch[0].isGoal():
                        print("TEMP")
                open.append(children)
                while len(open) > self.K:
                    open.pop()


if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()