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
    print("> ERROR: " + str(errorMessage))


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
    print("> Play again y/n?")
    userIn = input('>>').lower()  # splits the input at every space
    if userIn == 'n' or userIn ==  'no':
        quit()



def commandCenter(commands=[]):
    test = False
    if len(commands) > 0:
        test = True
    newGame = True
    puzzle = None  # type: ep.EightPuzzle or ttt.TicTacToe
    cmd = 0  # for the number of commands
    maxNodes = 5000
    # --- MAIN LOOP --- #
    # This is all one big loop for user commands
    while True:
        if puzzle is not None:
            try:
                if puzzle.isGoal():  # WIN! NEW GAME
                    puzzle = None
                    print("> You Win!")
                    if not test:
                        playAgain()

                    newGame = True
                    continue  # goto next iteration in the loop
            except Exception:  # DRAW
                print("> Draw!")
                if not test:
                    playAgain()
                puzzle = None
                newGame = True
                continue  # goto next iteration in the loop
        if 0 == len(commands): # reset
            commands = []
            cmd = 0
            test = False
        if len(commands)-1 >= cmd :  # if cmd is not greater than the number of commands
            userIn = str(  # replaces all the bad formatting
                ''.join(commands[cmd])).replace(']', '').replace('[', '').replace(',', '').replace("'", '').split(' ')

            if userIn[0] == "alert":
                print("\n--", ' '.join(userIn[1:]).replace(']', '').replace('[', '').replace(',', '').replace("'", ''),
                      "--")
                cmd += 1
                continue
            print("\n>>", ' '.join(userIn).replace(']', '').replace('[', '').replace(',', '').replace("'", ''))
        else:  # once the initiated commands are done, prompt the user for more commands
            if newGame:
                print("> Please enter a starting state value by typing setState <state> or random <number>, or"
                      " to start a game of TicTacToe(Extra Credit) ")
            userIn = input("\n>> ").split(' ')
        if userIn[0] == "quit" or userIn[0] == "q":
            quit()
        elif userIn[0] == "file" or userIn[0] == "test": # if commanded to read from file instead of directly
            if userIn[0] == "test" or len(userIn) == 1:
                test = True
                temp = readFile("test.txt")
                for command in range(len(temp)):
                    commands.append(temp[command])
                    cmd = -1

            elif not os.path.isfile(userIn[1]):  # looks for the commands
                error(str(
                    userIn[1]) + "could not be found. Creating file now. Please insert your commands into this file")

                createFile(userIn[1])
            else:
                temp = readFile(userIn[1])
                if userIn[1] == 'test.txt':
                    test = True
                    cmd = -1
                for command in range(len(temp)):
                    commands.append(temp[command])
            cmd +=1
            continue
        elif userIn[0] == 'ttt':  # set's puzzle to ttt
            if len(userIn) == 1:
                puzzle = ttt.TicTacToe()
            else:
                if len(userIn) >= 2: # if player and state given
                    puzzle = ttt.TicTacToe(player=userIn[1], state=' '.join(userIn[2:]).replace(' ',''))
                else: # if only player given
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
                print('\t maxNodes set to', userIn[1])
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
                        Beam.Beam(puzzle, maxNodes=maxNodes)
                    Beam.Beam(puzzle, userIn[2], maxNodes=maxNodes)  # takes puzzle and k value
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
                        if cmd <= len(commands):  # if cmd is not greater than the number of commands
                            cmd += 1  # incrememnt command
                        continue
                    puzzle.__str__()
            elif type(puzzle) is ttt.TicTacToe:
                if userIn[0] == 'move':  # user commands a move in a direction
                    try:
                        puzzle.placePiece(int(userIn[1]) - 1)
                    except IndexError:
                        error("Please enter a valid location")
                        if cmd <= len(commands):  # if cmd is not greater than the number of commands
                            cmd += 1  # incrememnt command
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
    parser.add_argument("-file", help="Read commands from txt file", dest="file", type=str)
    args = parser.parse_args()

    # converts input into something readable by the Main Loop
    if args.file is not None:  # if commanded to read from file instead of directly
        if not os.path.isfile(args.file):  # looks for the commands
            error(str(
                args.file) + "could not be found. Creating file now. Please insert your commands into this file")
            createFile(args.file)
        else:
            commands = readFile(args.file)  # read commands
    commandCenter(commands)  # passes commands along to the interpreter
