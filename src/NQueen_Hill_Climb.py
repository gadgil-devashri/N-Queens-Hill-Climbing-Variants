import copy
from random import Random, randint
import numpy as np
steps = 0
avgSuccessSteps = 0
avgFailureSteps = 0
successCount = 0
failureCount = 0

class Node:
    def __init__(self, board, hvalue) -> None:
        self.board = board
        self.hvalue = hvalue
    
    def printBoard(self):
        print(np.matrix(self.board))
    
class NQueen:
    def __init__(self, size) -> None:
        self.size = size
    
    # Generates a random board configuration by placing the queens at random rows in each column
    def generateRandomPosition(self):
        numOfQueens = self.size
        mat = [['-' for i in range(numOfQueens)] for j in range(numOfQueens)]
        for y in range(numOfQueens): 
            queenPositionx = randint(0, self.size - 1)
            for x in range(numOfQueens):
                if (x == queenPositionx):
                    mat[x][y] = 'Q'
                else:
                    mat[x][y] = '-'
        return mat

    def heuristicFunction(self, board):
        heuristicValueRows = 0
        size = len(board)
        # Calculate the number of queens in the same row thus calculating the heuristic value of rows
        for x in board:
            count = x.count('Q')
            # More than one queen in the row, add to the heuristic value
            if(count > 1):
                heuristicValueRows = heuristicValueRows + (sum(range(x.count('Q'))))
        heuristicValueDiagonal = 0

        # Calculate the heuristic of diagonal, from left to right
        for y in range(size-1, -1, -1):
            numQueen = 0
            col = 0
            row = y
            while(col < size and row < size):
                value = board[row][col]
                if(value == 'Q'):
                    numQueen = numQueen + 1
                col = col + 1
                row = row + 1
            if(numQueen > 1):
                heuristicValueDiagonal = heuristicValueDiagonal + (sum(range(numQueen)))
        for y in range(size-1, 0, -1):
            numQueen = 0
            col = y
            row = 0
            while(col < size and row < size):
                value = board[row][col]
                if(value == 'Q'):
                    numQueen = numQueen + 1
                col = col + 1
                row = row + 1
            if(numQueen > 1):
                heuristicValueDiagonal = heuristicValueDiagonal + (sum(range(numQueen)))
        
        #Calculate the heuristic of the diagonal, from right to left
        for y in range(size-1, -1, -1):
            numQueen = 0
            col = y
            row = 0
            while(col >= 0 and row < size):
                value = board[row][col]
                if(value == 'Q'):
                    numQueen = numQueen + 1
                col = col - 1
                row = row + 1
            if(numQueen > 1):
                heuristicValueDiagonal = heuristicValueDiagonal + (sum(range(numQueen)))
        for y in range(size-1, 0, -1):
            numQueen = 0
            col = size-1
            row = y
            while(col >= 0 and row < size):
                value = board[row][col]
                if(value == 'Q'):
                    numQueen = numQueen + 1
                col = col - 1
                row = row + 1
            if(numQueen > 1):
                heuristicValueDiagonal = heuristicValueDiagonal + (sum(range(numQueen)))
        # Calculate the total heuristic value as the sum of row and diagonal heuristic
        heuristicValue = heuristicValueRows + heuristicValueDiagonal
        return heuristicValue

    # Generate the successors of the current configuration and select 
    # the successor with lowest configuration for further evaluation                  
    def generateSuccessors(self, Node):
        row = -1
        column = -1
        currentBoard = Node.board
        currentHeuristic = Node.hvalue
        queenPosition = [None] * len(currentBoard)
        boardChange = False
        # Make copy of the current board configuration
        tempBoard = copy.deepcopy(currentBoard)
        # Iteration for column
        for y in range (0,len(currentBoard)):
            # Iteration for row
            for x in range (0,len(currentBoard)):
                # Store the position of queen in current column
                if currentBoard[x][y] == 'Q':
                    queenPosition[y] = x
        for y in range (0,len(currentBoard)):
            if(boardChange == True):
                break
            # Put the current queen position in the temp variable
            currentQueenPosition = queenPosition[y]
            # Remove the queen from the current position to generate successors
            tempBoard[currentQueenPosition][y] = '-'          
            for x in range (0,len(currentBoard)):
                # Put the queen on each position in column apart from the current position 
                # and calculate the heuristic
                if x != currentQueenPosition:
                    tempBoard[x][y] = 'Q'
                    tempHeuristic = self.heuristicFunction(tempBoard)
                    # If the heuristic of the new configuration is less than current configuration, 
                    # make it the current configuration for further evaluation
                    if currentHeuristic > tempHeuristic:
                        column = y
                        row = x
                        currentHeuristic = tempHeuristic
                        tempBoard[x][y] = '-'
                        boardChange = True
                        break
                # Remove the queen from the temp position for next positions
                tempBoard[x][y] = '-'
            # When all rows of the column are evaluated,put the queen at the original position
            tempBoard[currentQueenPosition][y] = 'Q'

        # Solution was not found
        if column == -1 and row == -1:
            return False
        # Configuration with lower heuristic was found. Replace the current board configuration
        # with the new configuration
        currentBoard[queenPosition[column]][column] = '-'
        currentBoard[row][column] = 'Q'
        Node.hvalue = currentHeuristic
        print("Current Board:")
        Node.printBoard()
        print("Current Heuristic: ",currentHeuristic)
        return True

    def hillClimb(self):
        # Generate random position of the board
        board = NQueen.generateRandomPosition(self)
        current = Node(board, 0)
        current.printBoard()
        #Calculate no of queens under attack(heuristic)
        current.hvalue = self.heuristicFunction(current.board)
        
        # Loop until the heuristic function becomes zero or heuristic value of successors is more than the current node
        while current.hvalue !=0:
            global steps
            steps = steps + 1
            # Call the generate successors functions
            end = self.generateSuccessors(current)
            # Failure
            if end == False:
                break
        # Success! Solution has been found for the problem - Calculate the Success metrics
        if current.hvalue == 0:
            global successCount
            global avgSuccessSteps
            avgSuccessSteps = steps + avgSuccessSteps
            successCount = successCount + 1
            steps = 0
            print("Solution found")
            current.printBoard()
        # Calculate the failure metrics
        else:
            global failureCount
            global avgFailureSteps
            avgFailureSteps = steps + avgFailureSteps
            failureCount = failureCount + 1
            steps = 0
            print("Failure")
        
        
# Input the no. of Queens to solve the problem
print("Enter number of Queens:")
noOfQueens = int(input())
# N-Queens can only be solved for size greater than 3
if(noOfQueens < 4):
    print("Problem cannot be solved for queens less than 4")
# No of iterations
print("How many times you want to run problem:")
counter = int(input())
iteration = 1
nQueen = NQueen(noOfQueens)
while counter != 0:
    print("Iteration ",iteration)
    nQueen.hillClimb()
    iteration = iteration + 1
    counter = counter - 1

print("Success Count: ",successCount)
print("Failure Count: ",failureCount)
print("Success Rate", (successCount/(successCount+failureCount)*100))
print("Failure Rate", (failureCount/(successCount+failureCount)*100))
print("Avg Success Steps", (avgSuccessSteps/(successCount)))
print("Avg Failure Steps", (avgFailureSteps/(failureCount)))