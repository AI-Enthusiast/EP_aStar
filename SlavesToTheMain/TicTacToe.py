# TicTacToe.py created for representing the classic puzzle of the same name
# DateCreated: 9/16/18
# Author: Cormac Dacker (cxd289)

import random
import sys

random.seed(23)
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))

class TicTacToe:
    def __init__(self, state = "random", parent = None):
        self.Parent = parent

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

    def validateState(self):
        print("TEMP")

    def randomizeState(self):
        print("TEMP")

    def __str__(self):
        print("TEMP")

    def placePiece(self):
        print("TEMP")

#TODO solve