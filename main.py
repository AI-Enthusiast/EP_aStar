import argparse
import csv
import os
import timeit

from SlavesToTheMain import AStar
from SlavesToTheMain import Beam
from SlavesToTheMain import EightPuzzle as ep
from SlavesToTheMain import TicTacToe as ttt


# Reports an error
def error(errorMessage):
    print("> ERROR:\t" + str(errorMessage))


# Creates a "Command.csv" file
def createFile(file):
    f= open(file, 'w+', newline='\n', encoding='utf8')
    f.close()


# Reads commandCenter from "Command.csv"
def readFile(file):
    with open(file, "r", newline='', encoding='utf8') as csvfile:
        DataReader = csv.reader(csvfile, delimiter="\n", quotechar=" ")
        start, out = [], []  # you're beautiful (shhh it's a secret)
        for item in DataReader:
            start.append(item)
        csvfile.close()
        # print(start)
        # for index in range(len(start)):
        #     out.append(start[0][index])
        return start


def playAgain():
    userIn = input('>>').lower()  # splits the input at every space
    if userIn == 'n' or userIn ==  'no':
        quit()



def commandCenter(commands=None):
    newGame = True
    puzzle = None  # the puzzle being opporated on
    cmd = 0  # for the number of commands
    maxNodes = 5000

    # --- MAIN LOOP --- #
    # This is all one big loop for user commands
    while True:
        if puzzle is not None:
            try:
                if puzzle.isGoal():  # WIN! NEW GAME
                    puzzle = None
                    print("> You Win! Play again y/n?")
                    newGame = True
                    playAgain()
                    continue  # goto next iteration in the loop
            except Exception:  # DRAW
                print("> Draw! Play again y/n?")
                newGame = True
                playAgain()
                continue  # goto next iteration in the loop

        if len(commands)-1 >= cmd :  # if cmd is not greater than the number of commands
            userIn = str(  # replaces all the bad formatting
                ''.join(commands[cmd])).replace(']', '').replace('[', '').replace(',', '').replace("'", '').split(' ')
            print("\n>>", ' '.join(userIn).replace(']', '').replace('[', '').replace(',', '').replace("'", ''))
            if cmd == len(commands): # reset
                commands = []
                cmd = 0
        else:  # once the initiated commands are done, prompt the user for more commands
            if newGame:
                print("> Please enter a starting state value by typing setState <state> or random <number>, or"
                      " to start a game of TicTacToe(Extra Credit) ")
            userIn = input("\n>> ").split(' ')
        if userIn[0] == "quit" or userIn[0] == "q":
            quit()
        elif userIn[0] == "file" or userIn[0] == "test": # if commanded to read from file instead of directly
            if  userIn[0] == "test":
                commands= readFile("test.txt")
                continue
            if not os.path.isfile(userIn[1]):  # looks for the commands
                error(str(
                    userIn[1]) + "could not be found. Creating file now. Please insert your commands into this file")
                createFile(userIn[1])
            else:
                commands = readFile(userIn[1])  # read commands
                continue
        elif userIn[0] == 'ttt':  # set's puzzle to ttt
            puzzle = ttt.TicTacToe(player=userIn[1])
            newGame = False
        elif userIn[0] == 'state' or userIn[0] == 'setState':  # if the user commands a state
            uI = ' '.join(userIn[1:]).lower().replace(' ', '')
            try:
                if len(uI) > 0:  # if the user provided the state
                    puzzle = ep.EightPuzzle(state=str(uI))
                else:
                    error("Please provide a state")
                    continue
                newGame = False
            except ValueError:
                continue

        elif userIn[0] == "random" or userIn[0] == "randomizeState":
            if len(userIn) > 1:  # if there is a number provided
                puzzle = ep.EightPuzzle(random=userIn[1])
            else:
                puzzle = ep.EightPuzzle()
            newGame = False
        elif userIn[0] == "maxNodes":
            if len(userIn) > 1:  # if there is a number provided
                maxNodes = int(userIn[1])
            else:
                error("maxNodes not given a value")
                continue

        elif not newGame:  # There is an incomplete game in place (no way out but to win)


            if userIn[0] == "solve":  # user commands to solve
                start = timeit.default_timer()  # start timer

                # A* style
                if userIn[1] == "a-star" or userIn[1] == "aStar" or userIn[1] == "astar" or userIn[1] == "a_star":
                    if type(puzzle) is ttt.TicTacToe:
                        AStar.AStar(maxNodes, puzzle)
                    else:
                        AStar.AStar(maxNodes, puzzle, heuristic=userIn[2])  # takes puzzle, heuristic, and maxNodes
                elif userIn[1] == "beam":  # Beam stylepuzz
                    if len(userIn) < 3:
                        error("Please provide a k for beam")
                        continue
                    Beam.Beam(puzzle, userIn[2])  # takes puzzle and k value
                stop = timeit.default_timer()  # stop the timer
                print("Time to solve:", stop - start, "seconds")  # print time

            elif userIn[0] == "printState" or userIn[0] == 'print':  # user commands a print
                puzzle.__str__()

            elif userIn[0] == 'help':  # user needs help with commands
                print("> Valid commands include 'move <direction>', 'solve <algorithm>', 'print' or 'printState'")

            elif type(puzzle) is ep.EightPuzzle:
                if userIn[0] == 'move':  # user commands a move in a direction
                    uI = ' '.join(userIn[1:]).lower()  # unite all from 1 onward
                    try:
                        if uI == 'up':
                            ep.moveUp(puzzle)
                        elif uI == 'down':
                            ep.moveDown(puzzle)
                        elif uI == 'left':
                            ep.moveLeft(puzzle)
                        elif uI == 'right':
                            ep.moveRight(puzzle)
                        else:
                            print("> Please enter a valid move, eg: 'move left'")
                    except UnboundLocalError:
                        error("You can't go that way")
                        continue
                    puzzle.__str__()
            elif type(puzzle) is ttt.TicTacToe:
                if userIn[0] == 'move':  # user commands a move in a direction
                    try:
                        puzzle.placePiece(int(userIn[1]) - 1)
                    except IndexError:
                        error("Please enter a valid location")
                        continue
                    puzzle.__str__()
            else:
                error("Please enter a valid command or type 'help'")
        elif userIn[0] == 'help':  # user needs help with commands
            print("> Valid commands include 'state <state>' or 'setState <state>', the '<state>' is optional and if not"
            " inputted will create a random state. format the <state> = 'b12345678' or 'b12 345 678'")
        else:
            error("Please enter a valid command or type 'help'")
        if cmd <= len(commands):  # if cmd is not greater than the number of commands
            cmd += 1  # incrememnt command

# main's main ;)
if __name__ == "__main__":
    commands = []  # commands fed to loop

    print("> Welcome, type 'q' or 'quit' to quit")

    # Commandline interface
    parser = argparse.ArgumentParser(description="Initialize a game and play or watch algorithms solve it")
    parser.add_argument("-setState", help="e.g. 'b12 345 678' or 'b12345678' or 'random'", dest="state")
    parser.add_argument("-randomizeState", help="Sets number of random moves to create the random board", dest='random',
                        type=int)
    parser.add_argument("-maxNodes", help="The max depth A* can visit", dest="maxNodes", type=int)
    parser.add_argument("-aStar", help="Solves the puzzle A* style. Given a heuristic and a maxNodes", dest="a_star",
                        type=str)
    parser.add_argument("-beam", help="Solves the puzzle Beam style. Given k as a limit", dest="beam", type=int)
    parser.add_argument("-print", help="Prints the current state of the puzzle", dest="print", type=bool)
    parser.add_argument("-file", help="The file to  read commands from, is a csv", dest="file", type=str)
    args = parser.parse_args()



    # converts input into something readable by the Main Loop
    if args.file is not None:  # if commanded to read from file instead of directly
        if not os.path.isfile(args.file):  # looks for the commands
            error(str(
                args.file) + "could not be found. Creating file now. Please insert your commands into this file")
            createFile(args.file)
        commands = readFile(args.file)  # read commands
    else:  # if given a direct command through the command prompt
        print(args  )
        args = (args.__str__()[10:-1]).split(', ')  # splits the string at ',' and removes the unessisary parts
        for i in range(len(args)):  # this loop converts the commands into a readable format for the main loop
            args[i] = str(args[i]).split("=")  # split at '='
            print(args)
            if args[i][1] != 'None':  # while there are still None commands
                args[i] = str(args[i]).replace("'", "").replace("\"", "")  # remove single quotes
            if str(args[i][1:-1]).split(', ')[0] == "a_star" or str(args[i][1:-1]).split(', ')[0] == "beam":
                args[i] = str("0solve " + ' '.join(str(args[i][1:-1]).split(', ')[0:]) + '0')
            if args[i][1] != 'None':  # if not None
                commands.append(str(args[i][1:-1]).split(', '))  # append to commands the give command
        commands.reverse()
    commandCenter(commands)  # passes commands along to the interpreter
