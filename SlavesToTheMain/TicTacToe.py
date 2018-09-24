# TicTacToe.py created for representing the classic puzzle of the same name
# DateCreated: 9/16/18
# Author: Cormac Dacker (cxd289)
# TODO Finish
import random
from typing import List

random.seed(13)


def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


class TicTacToe:
    # Constructor
    # Params: state(the state of the board, default is all blank), player(either 'X' or 'O', default is 'O'),
    #   parent(the preceding node)
    def __init__(self, state="bbbbbbbbb", player="O", parent=None):
        self.Parent = parent
        self.Player = player.upper()
        if state.lower() == "random":  # default to random
            self.randomizeState()
        else:
            try:
                if self.Parent is None:
                    if self.validState(state):
                        self.State = list(state.replace(' ', ''))  # finally sets the state to State for one dimention
                else:  # we don't need to validate it if it has a parent. it must be originating from a valid state.
                    self.State = list(state.replace(' ', ''))  # finally sets the state to State for one dimention
            except ValueError and TypeError as e:  # if you gave a screwy state
                error(e)
                # TODO double check user inputed states are solvable
                print('Setting state to random instead')
                self.randomizeState()

    # prints a visual representation of the board
    def __str__(self):
        print("TEMP")

    # Checks if the goal has been met
    def isGoal(self):
        player = self.Player
        board = self.State

        # Compares there tile locations to see if it's a win
        def compare(x, y, z):
            return (board[x] == player and board[y] == player and board[z] == player)

        # Given a board and a player, this function returns True if that player has won.
        return (compare(0, 1, 2) or  # across the top
                compare(3, 4, 5) or  # across the middle
                compare(6, 7, 8) or  # across the bottom
                compare(0, 3, 6) or  # down the left side
                compare(1, 4, 7) or  # down the middle
                compare(2, 5, 8) or  # down the right side
                compare(0, 4, 8) or  # diagonal left down to right
                compare(2, 4, 6))  # diagonal right down to left

    def validState(self):
        if self.Player != "X" and self.Player != "O":
            raise ValueError("Player ID", self.Player, "is not a valid player ID, please select either 'X' or 'O'")

    def randomizeState(self):
        print("TEMP")

    def placePiece(self):
        print("TEMP")


# Collects all the potential moves
def move(puzzle: TicTacToe) -> List[TicTacToe]:
    moves = []
    state = puzzle.State
    for tile in range(len(state)):  # Potential_Moves = all blank "b" tiles
        if state[tile] == "b":
            state[tile] = puzzle.Player
            moves.append(state)
    return moves
