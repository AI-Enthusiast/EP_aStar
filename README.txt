1. "cd" into the directory containing "main.py"
2. Run the program by typing "python main.py [-file FILE]" (FILE is a csv for simplicities sake)
or
2. Directly pass instructions to the program using any of the following commands.
usage: main.py [-h] [-setState STATE] [-randomizeState RANDOM]
               [-maxNodes MAXNODES] [-aStar A_STAR] [-beam BEAM]
               [-print PRINT] [-file FILE]

optional arguments:
  -h, --help            show this help message and exit
  -setState STATE       e.g. 'b12 345 678' or 'b12345678' or 'random'
  -randomizeState RANDOM
                        Sets number of random moves to create the random board
  -maxNodes MAXNODES    The max depth A* can visit
  -aStar A_STAR         Solves the puzzle A* style. Given a heuristic and a
                        maxNodes
  -beam BEAM            Solves the puzzle Beam style. Given k as a limit
  -print PRINT          Prints the current state of the puzzle
  -file FILE            The file to read commands from, is a csv

2b. example commandline input: "python main.py -randomizeState 60 -aStar h2"
3. Once the commands are done executing you can directly interact with the program. 