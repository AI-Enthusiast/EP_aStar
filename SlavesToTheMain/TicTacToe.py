# TicTacToe.py created for representing the classic puzzle of the same name
# DateCreated: 9/16/18
# Author: Cormac Dacker (cxd289)
# TODO Create heuristic function
# TODO flip btw turns
import random
from typing import List

random.seed(13)


def error(errorMessage):
    print("> ERROR:\t" + str(errorMessage))


class TicTacToe:
    # Constructor
    # Params: state(the state of the board, default is all blank), player(either 'X' or 'O', default is 'O'),
    #   parent(the preceding node)
    def __init__(self, state="123456789", player="O", parent=None, depth=0):
        self.Parent = parent
        self.Player = player.upper()
        self.Depth = depth
        try:
            if self.Parent is None:
                if self.validState(state):
                    self.State = list(state.replace(' ', ''))  # finally sets the state to State for one dimention
                    self.__str__()
            else:  # we don't need to validate it if it has a parent. it must be originating from a valid state.
                self.State = list(state.replace(' ', ''))  # finally sets the state to State for one dimention
        except ValueError and TypeError as e:  # if you gave a screwy state
            error(e)

    # prints a visual representation of the board
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

    # allows for TTT() < TTT() conparison
    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    # Checks if the goal has been met
    def isGoal(self):
        if self.move() is None:
            raise Exception
        # Given a board and a player, this function returns True if that player has won.
        return (compare(self, 0, 1, 2) or  # across the top
                compare(self, 3, 4, 5) or  # across the middle
                compare(self, 6, 7, 8) or  # across the bottom
                compare(self, 0, 3, 6) or  # down the left side
                compare(self, 1, 4, 7) or  # down the middle
                compare(self, 2, 5, 8) or  # down the right side
                compare(self, 0, 4, 8) or  # diagonal left down to right
                compare(self, 2, 4, 6))  # diagonal right down to left

    def validState(self, state):
        if self.Player != "X" and self.Player != "O":
            raise ValueError("Player ID", self.Player, "is not a valid player ID, please select either 'X' or 'O'")
        if len(state) != 9:
            raise ValueError(
                "Please format the desiered state correctly, e.g. 'b12 345 678'. Must be of length 9. "
                "You entered a string of length", len(state), state)
        return True

    # Places peice at location
    def placePiece(self, location):
        self.State[location] = self.Player


    # Get's the next player to play
    def nextPlayer(self):
        if self.Player == "X":
            return "O"
        else:
            return "X"

    # Collects all the potential moves
    def move(self):
        moves = []
        state = self.State
        for tile in range(len(state)):  # Potential_Moves = all blank "b" tiles
            if state[tile] != "X" and state[tile] != "O":  # the tile is blank
                state[tile] = self.Player
                moves.append(
                    TicTacToe(state=''.join(state), player=self.nextPlayer(), parent=self.__str__(),
                              depth=self.Depth + 1))  # appends instance of ttt
        return moves

    # Creates the path to the parent from the current node (this assumes that node is the goal)
    # Recursive
    def generateSolutionPath(self, path=[]):
        if self.Parent is None:  # your at the top
            path.reverse()  # reverse order as they are added in
            print(' --> '.join(path))
        else:  # there are still parent nodes
            path.append(self.Parent[0])
            return self.Parent[1].generateSolutionPath(path)  # recursively self call for path

    def h1(self):
        if self.move() is None:
            return 0
        if self.isGoal():
            return 1

# Compares there tile locations to see if it's a win
def compare(puzzle, x, y, z):
    board = puzzle.State
    player = puzzle.Player
    return board[x] == player and board[y] == player and board[z] == player


if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()
