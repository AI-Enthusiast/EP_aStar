# AStar.py created for solving the 8-puzzle problem and TicTacToe
# DateCreated: 9/7/18
# Author: Cormac Dacker (cxd289)
from typing import List

from SlavesToTheMain import EightPuzzle as ep
from SlavesToTheMain import TicTacToe as ttt


def error(errorMessage):
    print("> ERROR: " + str(errorMessage))


class AStar:
    # Constructor
    # Params: puzzle(the puzzle being solved), heuristic(either 'h1' or 'h2', maxNodes(the maximum depth)
    def __init__(self, maxNodes,puzzle, heuristic = 'h2'):
        self.H = heuristic
        if self.H == 'h1':
            print("f(x) = h1(x) + inversions(x)")
        elif self.H == 'h2':
            print("f(x) = h2(x) + inversions(x)")
        elif self.H == 'h3':
            print("f(x) = inversions(x) + depth(x)")
        elif self.H == 'h4':
            print("f(x) = h1(x) + h2(x) + inversions(x) + depth(x)")
        else:
            raise ValueError("Please enter a valid heuristic for A*. Either 'h1','h2','h3', or 'h4'")
        self.aStar(puzzle, maxNodes)  # print aStar solution

    # The heuristic function
    def f(self, puzzle):
        if type(puzzle) is ttt.TicTacToe: # TTT heuristic function
            return puzzle.numLinesOpen
        elif self.H == 'h1':
            return puzzle.h1() + puzzle.inversions() + puzzle.Depth
        elif self.H == 'h2':
            return puzzle.h2() + puzzle.inversions() + puzzle.Depth
        elif self.H == 'h3':
            return puzzle.inversions() + puzzle.Depth
        elif self.H == 'h4':
            return puzzle.h1() + puzzle.h2() + puzzle.inversions() + puzzle.Depth

    # Chooses a branch based off a priority queue representing the heuristic function of the puzzles
    def chooseBranch(self, open, closed):
        funcHeap = []
        for branch in range(len(open)):  # build the queue
            if str(open[branch].State) not in closed:
                funcHeap.append((self.f(open[branch]), open[branch]))  # pushes info to the queue
        funcHeap.sort(reverse=True)
        theChosenOne = funcHeap.pop()[1]  # picks top branch
        return theChosenOne # returns the puzzle on top

    # The one and only A* it'self! Say hello A*! <3
    def aStar(self, puzzle, maxNodes):
        goal = False
        open, closed = [], {}  # nodes to visit, nodes to not visit
        if puzzle.isGoal():  # if the current puzzle is the goal state
            puzzle.generateSolutionPath()  # goal has been achieved
        else:  # work toward the goal
            open.append(puzzle)  # add the starting puzzle to open
            while open is not None:  # while there are still nodes to expand in open
                try:
                    branch = self.chooseBranch(open,
                                               closed)  # type: ep.EightPuzzle or ttt.TicTacToe #choose a branch from open
                except ValueError as e:  # if invalid heuristic given
                    error(e)
                    break
                closed[branch.State] = branch  # add the chosen branch to the closed table
                open.remove(branch)  # remove the branch from open
                newBranches = branch.move(
                    0)  # type: List[ep.EightPuzzle] or List[ttt.TicTacToe] # get childern of that branch
                for stem in range(len(newBranches)):  # for each expantion of the branch
                    try:
                        if newBranches[stem].isGoal():  # if it's the goal
                            newBranches[stem].generateSolutionPath([])  # generate solution
                            print("Number of moves:", newBranches[stem].Depth)
                            print("Total nodes explored:", len(open) + closed.__len__())
                            goal = True  # we are done
                            break  # goal has been achieved
                    except Exception: # draws
                        continue
                    # if not in closed & not exceeded depth
                    if newBranches[stem].State not in closed and newBranches[stem].Depth < 31:
                        open.append(newBranches[stem])  # add stem to open nodes
                if goal:
                    break
                elif len(open) + closed.__len__() > maxNodes:
                    error("Max nodes exceeded")
                    break


if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()
