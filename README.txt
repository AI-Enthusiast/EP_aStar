1. "cd" into the directory containing "main.py"
2. Run the program by typing "python3 main.py [-file FILE]" (FILE delimiter is '\n')
or
2. Directly pass instructions to the program using any of the following commands:
	usage: main.py [-h][-file FILE]

	optional arguments:
  		-h, --help  show this help message and exit
		-file FILE  Read commands from txt file


2b. example commandline inputs: 
	"python main.py -file test.txt"

3. Once the commands are done executing you can directly interact with the program. 
	Commands:
		quit/q : to quit
		file FILE : to read from specified file
		test : to run test file commands
		randomizeState N : where N is the number of moves random moves made; Default = 42
		maxNodes N : where N is the number of max nodes; Default = 5000
		print/printState : to print the current state
		move DIRECTION : where DIRECTION is a codinal direction "up,down,left,right"
		solve astar H : where H is a heuristic function, "h1-h4"
		solve beam K : where K is the number of nodes to be considered at a time
		ttt PLAYER : to initialize a game of ttt where PLAYER is either 'X' or 'O'; Default = 'X'
EXTRA CREDIT:
1. Once all your commands have run and you are directly interacting with the script, input "ttt <player (either 'X' or 'O")>" to initiallize a game of ttt.
2. You are playing against the computer
3. Move by entering "move <Row,Col>" (0,0) is in the top left, (2,2) is in the bottom right. Eg type "move 1 2"

Good Luck! :)