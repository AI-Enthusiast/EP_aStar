import argparse
import csv
import os
import timeit

from SlavesToTheMain import AStar
from SlavesToTheMain import Beam
from SlavesToTheMain import EightPuzzle as ep

# Reports an error
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


# Creates a "Command.csv" file
def createFile():
    with open("Command.csv", 'w', newline='\n', encoding='utf8') as csvfile:
        csvfile.close()


# Reads commandCenter from "Command.csv"
def readFile():
    with open("Command.csv", "r", newline='', encoding='utf8') as csvfile:
        DataReader = csv.reader(csvfile, delimiter=",", quotechar=" ")
        start,out = [],[]  # you're beautiful (shhh it's a secret)
        for item in DataReader:
            start.append(item)
        csvfile.close()
        for index in range(len(start[0])):
            out.append([start[0][index]])
        return out


def commandCenter(commands):
    newGame = True
    puzzle = None  # the puzzle being opporated on
    cmd = 0  # for the main loop
    maxNodes = 31

    # --- MAIN LOOP --- #
    # This is all one big loop for user commands
    while True:
        if cmd <= len(commands) - 1:  # if cmd is not greater than the number of commands
            userIn = str(  # replaces all the bad formatting
                ' '.join(commands[cmd]).replace(']', '').replace('[', '').replace(',', '').replace("'", '')).split(' ')
            print("\n>>", ' '.join(userIn).replace(']', '').replace('[', '').replace(',', '').replace("'", ''))
        else:  # once the initiated commands are done, prompt the user for more commands
            userIn = input("\n>> ").split(' ')

        if userIn[0] == "quit" or userIn[0] == "q":
            quit()

        elif userIn[0] == 'state' or userIn[0] == 'setState':  # if the user commands a state

                uI = ' '.join(userIn[1:]).lower().replace(' ', '')
                try:
                    if len(uI) > 0:  # if the user provided the state
                        puzzle = ep.EightPuzzle(state=uI)
                    else:
                        error("Please provide a state")
                        continue
                    newGame = False
                except ValueError:
                    continue

        elif userIn[0] == "random" or userIn[0] == "randomizeState":
            if len(userIn) > 1: # if there is a number provided
                puzzle = ep.EightPuzzle(random=userIn[1])
            else:
                puzzle = ep.EightPuzzle()
            newGame = False
        elif userIn[0] == "maxNodes":
            if len(userIn) > 1: # if there is a number provided
                maxNodes = userIn[1]
            else:
                error("maxNodes not given a value")
                continue
        elif not newGame:  # There is an incomplete game in place (no way out but to win)

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
                puzzle.__str__()

                if puzzle.isGoal():  # WIN! NEW GAME
                    print("> You Win! Play again y/n?")
                    userIn = input('>>').lower()  # splits the input at every space

                    if userIn == 'n' or 'no':
                        quit()
                    else:
                        newGame = True
                        print("> Please enter a starting state 'state <state>' or type 'state' for a random state")
                        continue  # goto next iteration in the loop

            elif userIn[0] == "solve":  # user commands to solve
                start = timeit.default_timer()  # start timer
                # A* style
                if userIn[1] == "a-star" or userIn[1] == "aStar" or userIn[1] == "astar" or userIn[1] == "a_star":
                    AStar.AStar(puzzle, userIn[2], maxNodes)  # takes puzzle, heuristic, and maxNodes
                elif userIn[1] == "beam":  # Beam style
                    Beam.Beam(puzzle, userIn[2])  # takes puzzle and k value
                else:
                    error("Please enter a valid command or type 'help'")
                stop = timeit.default_timer()  # stop the timer
                print("Time to solve:", stop - start, "seconds")  # print time

            elif userIn[0] == "printState" or userIn[0] == 'print':  # user commands a print
                puzzle.__str__()

            elif userIn[0] == 'help':  # user needs help with commands
                print("> Valid commands include 'move <direction>', 'solve <algorithm>', 'print' or 'printState'")
            else:
                error("Please enter a valid command or type 'help'")

        elif userIn[0] == 'help':  # user needs help with commands
            print(
                "> Valid commands include 'state <state>' or 'setState <state>', the '<state>' is optional and if not"
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
            createFile()
        commands = readFile()  # read commands
        print(commands)
    else:  # if given a direct command through the command prompt
        args = (args.__str__()[10:-1]).split(', ')  # splits the string at ',' and removes the unessisary parts
        for i in range(len(args)):  # this loop converts the commands into a readable format for the main loop
            args[i] = str(args[i]).split("=")  # split at '='
            if args[i][1] != 'None':  # while there are still None commands
                args[i] = str(args[i]).replace("'", "").replace("\"", "")  # remove single quotes
        for i in range(len(args)):  # this loop converts the commands into a readable format for the main loop
            if str(args[i][1:-1]).split(', ')[0] == "a_star" or str(args[i][1:-1]).split(', ')[0] == "beam":
                args[i] = str("0solve " + ' '.join(str(args[i][1:-1]).split(', ')[0:]) + '0')
            if args[i][1] != 'None':  # if not None
                commands.append(str(args[i][1:-1]).split(', '))  # append to commands the give command
        print(commands)
        commands.reverse()
    commandCenter(commands) # passes commands along to the interpreter
