import random, sys

#Setting the recursion limit quite high as it is required for the recursive solve of the Sudoku puzzle
sys.setrecursionlimit(100000)

#A blank array, copied and used to initialize a few variables
blank_array = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]

class Board():
    solved_counter = []
    randOrder = [1,2,3,4,5,6,7,8,9]
    def __init__(self, pattern="000000000000000000000000000000000000000000000000000000000000000000000000000000000"):
        self.rows = blank_array.copy()
        self.columns = blank_array.copy()
        self.boxes = blank_array.copy()

        #Iterating through the pattern and assigning it to the pre-initalized self.rows variable
        rC = 0
        cC = 0
        for p in pattern:
            self.rows[rC][cC] = int(p)
            cC += 1
            if cC > 8:
                cC = 0
                rC += 1
        #Init the easy access self.valid variable and run a startup isValid() to get cols and boxes setups
        self.valid = self.isValid()

    #Prints the Board to the Console Window
    #Anything marked with a 0, means it is unsolved, like how a blank input board would be
    #Then the board can be solved, by running the recursive solve function (Maybe recursive)
    #Isn't neccessary for the Sudoku_Display.py, but kept in for debugging purposes
    def Print(self):
        row_counter = 0
        for row in self.rows:
            #Display certain text, based on which row to make the board look neat and readable
            if row_counter == 0 or row_counter == 3 or row_counter == 6:
                print("O-----O-----O-----O")
            elif row_counter == 1 or row_counter == 2 or row_counter == 4 or row_counter == 5 or row_counter == 7 or row_counter == 8:
                print("| . . | . . | . . |")
            else:
                print("-------------------")
            box_counter = 0
            for box in row:
                #Display certain text, based on which box to make the board look neat and readable
                if box_counter == 1 or box_counter == 2 or box_counter == 4 or box_counter == 5 or box_counter == 7 or box_counter == 8:
                    print(f" {box}", end='')
                else:
                    print(f"|{box}", end='')
                box_counter += 1
            print("|")
            row_counter += 1
        if row_counter == 9:
            print("O-----O-----O-----O")
        else:
            print("-------------------")

    #Check if the board follows all sudoku rules
    def isValid(self):
        self.valid = False
        self.columns = [[],[],[],[],[],[],[],[],[]]
        self.boxes = [[],[],[],[],[],[],[],[],[]]
        #Check Rows
        for row in self.rows:
            checker = []
            cCounter = 0
            
            #Since the rows variables is often the only one updated and tracked
            #This updates the boxes and columns variables making it easy to check for invalidity
            for box in row:
                if cCounter < 3:
                    if self.rows.index(row) < 3:
                        self.boxes[0].append(box)
                    elif self.rows.index(row) < 6:
                        self.boxes[1].append(box)
                    elif self.rows.index(row) < 9:
                        self.boxes[2].append(box)
                elif cCounter < 6:
                    if self.rows.index(row) < 3:
                        self.boxes[3].append(box)
                    elif self.rows.index(row) < 6:
                        self.boxes[4].append(box)
                    elif self.rows.index(row) < 9:
                        self.boxes[5].append(box)
                elif cCounter < 9:
                    if self.rows.index(row) < 3:
                        self.boxes[6].append(box)
                    elif self.rows.index(row) < 6:
                        self.boxes[7].append(box)
                    elif self.rows.index(row) < 9:
                        self.boxes[8].append(box)
                
                self.columns[cCounter].append(box)
                cCounter += 1
                if box == 0:
                    #print("Row Box is 0")
                    continue
                if box not in checker:                    
                    checker.append(box)
                    #print(f"Row Checker: {checker}")
                else:
                    #print(f"Row Error|r: {self.rows.index(row)}")
                    #print(f"b: {box}, checker: {checker}")
                    #print(f"row: {row}")
                    return False                

        #Check Columns   
        for col in self.columns:
            checker = [] 
            for box in col:
                if box == 0:
                    #print("Col Box is 0")
                    continue
                if box not in checker:
                    checker.append(box)
                    #print(f"Col Checker: {checker}")
                else:
                    #print(f"Col Error|c: {self.columns.index(col)}")
                    #print(f"b: {box}, checker: {checker}")
                    #print(f"col: {col}")
                    #print(self.columns)
                    return False

        #Check Big 3x3 Boxes
        for bigbox in self.boxes:
            checker = [] 
            for box in bigbox:
                #print("Box Box is 0")
                if box == 0:
                    continue
                if box not in checker:
                    checker.append(box)
                    #print(f"Box Checker: {checker}")
                else:
                    #print(f"Box Error|b: {self.boxes.index(bigbox)}")
                    #print(f"b: {box}, checker: {checker}")
                    #print(f"BigBox: {bigbox}")
                    return False
        self.valid = True
        return True

    #Checks if the board contains any 0s
    def isComplete(self):
        for row in self.rows:
            if 0 in row:
                return False
        return True

    #Returns tuple location of 1st occurance of search data
    def Find(self, search):
        result = []
        for row in self.rows:
            if search in row:
                result = [self.rows.index(row), row.index(search)]
                return result
        return result

    #Copies the Board by extracting the pattern and initializing a new object
    def Copy(self):
        newPattern = ""
        for row in self.rows:
            for box in row:
                newPattern += str(box)
        return Board(newPattern)

    #Solves the puzzle by trying each number in each spot and branching out on valid combinations, repeating the steps until
    #Either a solution will be reached and the solved board will be returned or the original board will be returned
    #When the original board returns it means there is no solution
    #Will not know if there are multiple solutions, will only check for 1
    def Solve(self, curr_board, depth=0):
        #if depth % 50 == 0:
            #print(depth)
        if curr_board.isValid() and curr_board.isComplete():
            return curr_board

        #Shuffles the order in which the numbers are tried this instanced
        #So instead of trying 1-9 in order, it randomly decides for each run of Solve the order
        #This allows multiple boards to be generated from a blank board, instead of getting the same array
        randNumbs = Board.randOrder.copy()
        random.shuffle(randNumbs)
        newBoards = [curr_board.Copy(),curr_board.Copy(),curr_board.Copy(),
                     curr_board.Copy(),curr_board.Copy(),curr_board.Copy(),
                     curr_board.Copy(),curr_board.Copy(),curr_board.Copy()]

        iCounter = 0
        bIndex = curr_board.Find(0)
        for newBoard in newBoards:
            newBoard.rows[bIndex[0]][bIndex[1]] = randNumbs[iCounter]            
            if newBoard.isValid():
                if newBoard.isComplete():
                    endBox = randNumbs[iCounter]
                    if endBox not in Board.solved_counter:
                        Board.solved_counter.append(endBox)
                        #newBoard.Print()
                        return newBoard
                    return curr_board
                futureBoard = self.Solve(newBoard, depth + 1)
                if futureBoard != newBoard:
                    return futureBoard
            iCounter += 1
        return curr_board

    #Uses the current board stored and generates a single solution sudoku based on the board (If possible)
    #First it solves the board, and tracks that solution as "The Solution"
    #It them randomly removes digits from the board, and resolves it every time
    #If a solution occurs where "The Solution" is not the soluion reached, it means there is a secondary solution
    #It then re-adds that last digit and returns the puzzle ready to be solved
    #The re-adding of the last digit is only intended as a fail safe if too many digits were requested to be removed and a unique puzzle could not be generated
    def Generate(self, remove_max):
        Board.solved_counter = []
        end_board = self.Solve(self.Copy())
        test_board = end_board.Copy()

        randX = random.randint(0,8)
        randY = random.randint(0,8)

        for i in range(remove_max):
            #Find a new non-empty cell to remove
            while test_board.rows[randY][randX] == 0:
                randX = random.randint(0,8)
                randY = random.randint(0,8)            

            #Save the number removed in case this removal brings additional solutions
            save_data = test_board.rows[randY][randX]
            test_board.rows[randY][randX] = 0

            futureBoard = self.Solve(test_board.Copy())
            if test_board.rows != futureBoard.rows and futureBoard.rows != end_board.rows:                    
                test_board.rows[randY][randX] = save_data
                return test_board
        #print("Generated Board")
        return test_board
