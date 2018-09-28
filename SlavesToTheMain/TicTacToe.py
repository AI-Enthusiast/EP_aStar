# TicTacToe.py created for representing the classic puzzle of the same name
# DateCreated: 9/16/18
# Author: Cormac Dacker (cxd289)
# TODO Create heuristic function
# TODO flip btw turns
import random

from SlavesToTheMain import AStar

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
                    self.Turn = random.randint(0, 1)
                # self.turn()
            else:  # we don't need to validate it if it has a parent. it must be originating from a valid state.
                self.State = list(state.replace(' ', ''))  # finally sets the state to State for one dimention
        except ValueError as e:  # if you gave a screwy state
            error(e)

    # prints a visual representation of the board
    def __str__(self, setting=1):
        tile = self.State
        out = "\t{0}   |   {1}   |   {2}\n" \
              "\t-----------------\n" \
              "\t{3}   |   {4}   |   {5}\n" \
              "\t-----------------\n" \
              "\t{6}   |   {7}   |   {8}".format(
            tile[0], tile[1], tile[2],
            tile[3], tile[4], tile[5],
            tile[6], tile[7], tile[8])
        if setting == 1:
            print(out)
        else:
            return out

    # allows for TTT() < TTT() conparison
    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def turn(self):
        while not self.isGoal():
            if self.Turn % 2:
                print("\t> It's your turn")
                move = int(input(">> move "))
                try:
                    self.placePiece(move)
                    self.Turn += 1
                except IndexError as e:
                    error("Please enter a valid location")
            else:
                print("\t> Computer's turn")
                open = self.move()
                puzzle = AStar.AStar(9, self)
                #   print(puzzle.chooseBranch(open,{}))
                print("Maybe oneday I'll finish this")
                quit()
        self.generateSolutionPath()



    # Checks if the goal has been met
    def isGoal(self):
        if len(self.move()) == 0:  # if there are now moves left DRAW
            raise Exception  # signals a draw
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
                "Please format the desiered state correctly, e.g. '123 456 789'. Must be of length 9. "
                "You entered a string of length", len(state), state)
        else:
            return True

    # Places peice at location
    def placePiece(self, location, player=None):
        if player == None:
            player = self.Player
        self.State[location] = player

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
                moves.append(
                    TicTacToe(state=''.join(state), player=self.nextPlayer(), parent=self.__str__(0),
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

    # counts the number of open lines
    @property
    def numLinesOpen(self):
        linesOpen = 0
        linesOpen += compare(self, 0, 1, 2, 1)  # across the top
        linesOpen += compare(self, 3, 4, 5, 1)  # across the middle
        linesOpen += compare(self, 6, 7, 8, 1)  # across the bottom
        linesOpen += compare(self, 0, 3, 6, 1)  # down the left side
        linesOpen += compare(self, 1, 4, 7, 1)  # down the middle
        linesOpen += compare(self, 2, 5, 8, 1)  # down the right side
        linesOpen += compare(self, 0, 4, 8, 1)  # diagonal left down to right
        linesOpen += compare(self, 2, 4, 6, 1)
        return linesOpen


# Compares there tile locations to see if it's a win
# x, y, z are tile locations
# setting 0 checks if it's a win, 1 checks if the line is open
def compare(puzzle, x, y, z, setting=0):
    board = puzzle.State
    player = puzzle.Player
    if setting == 0:
        return board[x] == player and board[y] == player and board[z] == player
    else:
        if board[x] != puzzle.nextPlayer() and board[y] != puzzle.nextPlayer() and board[z] != puzzle.nextPlayer():
            return -1  # if you or no one controlls the line
        else:
            return 1  # if the line is blocked


if __name__ == '__main__':
    error("Please run from 'main.py'")
    quit()
