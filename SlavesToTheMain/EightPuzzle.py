# EightPuzzle.py created for representing the classic puzzle of the same name
# DateCreated: 9/7/18
# Author: Cormac Dacker (cxd289)
import math
import random
from typing import List

random.seed(13)
goal = ['b', '1', '2', '3', '4', '5', '6', '7', '8']


def error(errorMessage):
    print("> ERROR:\t" + str(errorMessage))


class EightPuzzle:
    State = ...  # type: str

    # Constructor
    # Params: state(as a string of length 9), parent (type: EightPuzzle), b(location of the b tile)
    def __init__(self, state="random", random=42, parent=None, b=None, depth=0):
        self.Parent = parent
        self.B = b
        self.Depth = depth
        if str(state).lower() == "random":  # default to random
            self.randomizeState(int(random))
            self.__str__()
        else:
            try:
                if self.Parent is None:
                    if self.validState(state):
                        self.State = str(state).replace(' ', '')  # finally sets the state to State for one dimention
                        self.__str__()
                else:  # we don't need to validate it if it has a parent. it must be originating from a valid state.
                    self.State = str(state).replace(' ', '')  # finally sets the state to State for one dimention
            except ValueError  as e:  # if you gave a screwy state
                error(e)
                print('Setting state to random instead')
                self.randomizeState(int(random))
                self.__str__()

    # allows for EightPuzzle() < EightPuzzle() conparison
    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    # Checks if the goal has been met
    def isGoal(self):
        for i in range(len(self.State)):  # itterates through State and goal double checking they match
            if goal[i] != self.State[i]:  # if they dont match
                return False
        return True

    # Confirms the given state is valid
    def validState(self, state):
        # double checks it's of the right length(you can never trust the user)
        if len(state) != 9:
            raise ValueError(
                "Please format the desiered state correctly, e.g. 'b12 345 678'. Must be of length 9. "
                "You entered a string of length", len(state), state)
        # loops validates that entered state has all the right tiles
        for i in range(len(state)):
            for j in range(len(goal)):
                if goal[j] == state[i]:  # if the state has a correct tile
                    if state[i] == "b":  # ie if the blank tile has been found
                        self.B = i  # location of the blank tile
                    break  # break causes jump to the continue 4 lines down
                elif j == 8:  # a tile could not be found
                    raise ValueError("State", state[i],
                                     "not found. Please enter state correctly, 1->8 and a 'b'.")
            continue  # continue to next iteration
        if self.inversions() % 2 == 0:  # inversions determins state to be solvable
            return True
        else:
            raise ValueError("Please enter a solvable state. Your state:", state)

    # Creates a random starting state
    # Param: r(the range of random)
    def randomizeState(self, r):
        self.State = 'b12345678'  # sets 1d state
        self.B = 0  # location of the b tile
        # loop moves the blank piece 100 times in r directions
        for i in range(0, r):
            moves = self.move(0)  # type: List[EightPuzzle]
            ran = random.randint(0, len(moves) - 1)  # produce a r int between 1 and num of moves
            try:
                self.State = moves[ran].State  # sets state to chosen r move
                self.findB()  # updates the location of the b tile
            except UnboundLocalError:  # if it can't move that way
                i += 1  # don't let it miss a move
                pass

    # creates a string to visually represent the board
    def __str__(self):
        tile = self.State
        out = "\t{0}   |   {1}   |   {2}\n" \
              "\t-----------------\n" \
              "\t{3}   |   {4}   |   {5}\n" \
              "\t-----------------\n" \
              "\t{6}   |   {7}   |   {8}".format(
            tile[0], tile[1], tile[2],
            tile[3], tile[4], tile[5],
            tile[6], tile[7], tile[8])
        print(out)

    # Creates the path to the parent from the current node (this assumes that node is the goal)
    # Recursive
    def generateSolutionPath(self, path=[]):
        if self.Parent is None:  # your at the top
            path.reverse()  # reverse order as they are added in
            print(' --> '.join(path))
        else:  # there are still parent nodes
            path.append(self.Parent[0])
            return self.Parent[1].generateSolutionPath(path)  # recursively self call for path

    # Finds the location of the b tile
    def findB(self):
        for i in range(len(self.State)):
            if self.State[i] == 'b':
                self.B = i  # new B's location
                break

    # Swaps the location of the b tile with y
    # setting ( 0 = return states instead of setting them, 1 = set states at each move)
    def swap(self, b, y, direction=None, setting=1):
        state = list(self.State)
        # performs a switch
        temp = state[y]
        state[y] = state[b]
        state[b] = temp
        # update B's location
        if setting == 1:
            self.B = y
            self.State = str(''.join(state))
        else:
            return EightPuzzle(state=str(''.join(state)), parent=(direction, self), b=y, depth=self.Depth + 1)

    # Moves the tile up, down, left, right
    # setting ( 0 = return states instead of setting them, 1 = set states at each move)
    # the setting in this case is just to pass it along to lower level helpers
    def move(self, setting=1):
        puzzle = self
        moves = []
        try:
            moves.append(moveUp(puzzle, setting))  # move up
        except UnboundLocalError:  # cant go up
            pass
        try:
            moves.append(moveDown(puzzle, setting))  # move down
        except UnboundLocalError:  # cant go down
            pass
        try:
            moves.append(moveLeft(puzzle, setting))  # move left
        except UnboundLocalError:  # cant go left
            pass
        try:
            moves.append(moveRight(puzzle, setting))  # move right
        except UnboundLocalError:  # cant go right
            pass
        return moves

    # First Heuristic is based on the number of tiles out of place
    # the less the better
    def h1(self):
        puzzle = self
        numOutOfPlace = 0
        for i in range(len(goal)):
            if goal[i] != puzzle.State[i]:
                numOutOfPlace += 1
        return numOutOfPlace

    # Second heuristic is based on the distance of tiles to goal state (Manhattan Distance)
    # the less the better
    def h2(self):
        puzzle = self
        distTot = 0  # var for total distance
        for i in range(len(goal)):
            if puzzle.State[i] == goal[i]:  # if it's already on the right one
                continue
            else:
                tilePos = 0
                for j in range(len(puzzle.State)):
                    if puzzle.State[j] == goal[i]:  # if you find the current possion of the tile
                        tilePos = j
                        break  # break the loop cb tile found

                while tilePos != i:
                    if i < tilePos:  # if the tile needs to be moved up or left
                        if tilePos - 3 >= 0 and tilePos - 3 >= i:  # if it needs to be moved up
                            tilePos -= 3  # move the tile up
                            distTot += 1
                        elif tilePos - i < 3:  # if the tile needs to be moved left
                            dist = tilePos - i
                            tilePos -= dist
                            distTot += dist
                    elif i > tilePos:  # if the tile needs to be moved down or right
                        if tilePos + 3 <= 8 and tilePos + 3 <= i:  # if it needs to be moved down
                            tilePos += 3
                            distTot += 1
                        elif i - tilePos < 3:  # if the tile needs to be moved right
                            dist = i - tilePos
                            tilePos += dist
                            distTot += dist
        return distTot

    # Second heuristic is based on the distance of tiles to goal state (Manhattan Distance)
    # the less the better
    def euclidianDist(self):
        puzzle = self
        distTot = 0  # var for total distance
        for i in range(len(goal)):
            if puzzle.State[i] == goal[i]:  # if it's already on the right one
                continue
            else:
                tilePos = 0 # the position of the tile
                up = 0 # the num of moves up or down it must move
                over = 0 # the num of moves left or right it must move
                for j in range(len(puzzle.State)):
                    if puzzle.State[j] == goal[i]:  # if you find the current possion of the tile
                        tilePos = j
                        break  # break the loop cb tile found
                while tilePos != i:
                    if i < tilePos:  # if the tile needs to be moved up or left
                        if tilePos - 3 >= 0 and tilePos - 3 >= i:  # if it needs to be moved up
                            tilePos -= 3  # move the tile up
                            distTot += 1
                            up += 1
                        elif tilePos - i < 3:  # if the tile needs to be moved left
                            dist = tilePos - i
                            tilePos -= dist
                            distTot += dist
                            over += 1
                    elif i > tilePos:  # if the tile needs to be moved down or right
                        if tilePos + 3 <= 8 and tilePos + 3 <= i:  # if it needs to be moved down
                            tilePos += 3
                            distTot += 1
                            up += 1
                        elif i - tilePos < 3:  # if the tile needs to be moved right
                            dist = i - tilePos
                            tilePos += dist
                            distTot += dist
                            over += 1
                distTot += math.sqrt(up + over)
        return distTot

    # Counts the number of inversions with the given state, outputs odd or even number
    def inversions(self):
        state = str(self.State)
        inversion_count = 0
        for tile in range(len(state)):  # for each tile in the state
            if state[tile] != 'b' and tile != 0:  # if not blank tile or the fist tile
                for compare in range(tile - 1, -1, -1):  # work backwards counting tiles that shouldn't be there
                    if state[compare] != 'b':  # if not blank tile
                        if state[tile] < state[compare]:  # if a previouse tile is greater than current tile
                            inversion_count += 1
        return inversion_count


# Moves the blank tile up
# setting ( 0 = return states instead of setting them, 1 = set states at each move)
def moveUp(puzzle, setting=1):
    if (puzzle.B - 3) < 0:  # check to see if it's in bounds
        raise UnboundLocalError
    else:
        if setting == 1:  # set move to current state
            puzzle.swap(puzzle.B, puzzle.B - 3, setting)

        else:  # return the node made from moving
            return puzzle.swap(puzzle.B, puzzle.B - 3, "Up", setting)


# Moves the blank tile down
# setting ( 0 = return states instead of setting them, 1 = set states at each move)
def moveDown(puzzle, setting=1):
    if (puzzle.B + 3) > 8:  # check to see if it's in bounds
        raise UnboundLocalError
    else:
        if setting == 1:  # set move to current state
            puzzle.swap(puzzle.B, puzzle.B + 3, setting)
        else:  # return the node made from moving
            return puzzle.swap(puzzle.B, puzzle.B + 3, "Down", setting)


# Moves the blank tile left
# setting ( 0 = return states instead of setting them, 1 = set states at each move)
def moveLeft(puzzle, setting=1):
    if (puzzle.B % 3) == 0:  # check to see if it's in bounds
        raise UnboundLocalError
    else:
        if setting == 1:  # set move to current state
            puzzle.swap(puzzle.B, puzzle.B - 1, setting)
        else:  # return the node made from moving
            return puzzle.swap(puzzle.B, puzzle.B - 1, "Left", setting)


# Moves the blank tile right
# setting ( 0 = return states instead of setting them, 1 = set states at each move)
def moveRight(puzzle, setting=1):
    if (puzzle.B + 1) % 3 == 0:  # check to see if it's in bounds
        raise UnboundLocalError
    else:
        if setting == 1:  # set move to current state
            puzzle.swap(puzzle.B, puzzle.B + 1, setting)
        else:  # return the node made from moving
            return puzzle.swap(puzzle.B, puzzle.B + 1, "Right", setting)


if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()
