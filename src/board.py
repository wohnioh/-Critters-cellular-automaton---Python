import json
import random
class Board:
    def __init__(self,size ):
        self.size = size
        self.board = []
        self.beginningBoard = []
        self.grid =0
        for i in range(size):
            self.board.append([])
            self.beginningBoard.append([])
            for j in range(size):
                self.beginningBoard[i].append(0)
                self.board[i].append(0)

    def load(self,filename):
        self.grid = 0
        self.board = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(0)
        try:
            with open(filename,'r') as file:
                boardLoaded = json.load(file)
        except FileNotFoundError:
            print("File not found!!")
        if len(boardLoaded) <= len(self.board):
            diff = len(self.board) - len(boardLoaded)
            for i in range(len(boardLoaded)):
                for j in range(len(boardLoaded[i])):
                    self.board[int(diff/2)+i][int(diff/2)+j] = boardLoaded[i][j]
                    self.beginningBoard[int(diff/2)+i][int(diff/2)+j] = boardLoaded[i][j]
        else:
            print("error while opening board: chosen board is to big")
    def save(self,filename):
        with open(filename,'w') as file:
            json.dump(self.board, file)
    def __str__(self):
        s = ""
        for i in range(len(self.board)):
            s+= str(self.board[i])+"\n"
        return s
    def getBoard(self):
        return self.board

    def getBeginningBoard(self):
        return self.beginningBoard

    def restartBoard(self):
        for i in range(len(self.beginningBoard)):
            for j in range(len(self.beginningBoard[i])):
                self.board[i][j] = self.beginningBoard[i][j]
    def setCellLive(self,cell):
        self.board[cell[0]][cell[1]] = 1
    def changeSingleCell(self,cell):
        if self.board[cell[0]][cell[1]]== 1:
            self.board[cell[0]][cell[1]] =0
        else:
            self.board[cell[0]][cell[1]] =1

    def checkCaseOfCell(self,cell):
        liveCells = 0
        if cell[0] == self.size-1 and cell[1] == self.size-1: # prawy dolny róg
            liveCells = self.board[0][0] + self.board[self.size-1][0] + self.board[0][self.size-1] + self.board[self.size-1][self.size-1]
        elif cell[0] == self.size-1: #prawa strona
            liveCells = (self.board[0][cell[1]] + self.board[self.size-1][cell[1]] + self.board[0][cell[1]+1] + \
                         self.board[cell[0]][cell[1]+1])
        elif cell[1] == self.size-1: #dół
            liveCells = self.board[cell[0]][cell[1]] + self.board[cell[0]+1][cell[1]] + self.board[cell[0]][0] + \
                        self.board[cell[0]+1][0]
        else:
            liveCells = self.board[cell[0]][cell[1]]+self.board[cell[0]+1][cell[1]]+self.board[cell[0]][cell[1]+1]+self.board[cell[0]+1][cell[1]+1]
        return liveCells
    def rotateMultiCell(self,cell0,cell1,cell2,cell3):
        tempBoard = [self.board[cell3[0]][cell3[1]],self.board[cell2[0]][cell2[1]],self.board[cell1[0]][cell1[1]],self.board[cell0[0]][cell0[1]]]
        self.board[cell0[0]][cell0[1]] = tempBoard[0]
        self.board[cell1[0]][cell1[1]] = tempBoard[1]
        self.board[cell2[0]][cell2[1]] = tempBoard[2]
        self.board[cell3[0]][cell3[1]] = tempBoard[3]
    def changeMultiCell(self,cell): # case - który z przypadków zmiany zastosujemy
        liveCells = self.checkCaseOfCell(cell)

        if liveCells==2:
            pass
        elif liveCells==3:
            if cell[0] == self.size - 1 and cell[1] == self.size - 1:  # prawy dolny róg
                self.changeSingleCell([0,0])
                self.changeSingleCell([0, cell[1]])
                self.changeSingleCell([cell[0], 0])
                self.changeSingleCell([cell[0],cell[1]])
                self.rotateMultiCell([0,0],[0, cell[1]],[cell[0], 0],[cell[0],cell[1]])
            elif cell[0] == self.size - 1:  # prawa strona
                self.changeSingleCell([0,cell[1]])
                self.changeSingleCell([cell[0], cell[1]])
                self.changeSingleCell([0, cell[1]+1])
                self.changeSingleCell([cell[0],cell[1]+1])
                self.rotateMultiCell([0,cell[1]],[cell[0], cell[1]],[0, cell[1]+1],[cell[0],cell[1]+1])
            elif cell[1] == self.size - 1:  # dół
                self.changeSingleCell([cell[0], cell[1]])
                self.changeSingleCell([cell[0]+1, cell[1]])
                self.changeSingleCell([cell[0], 0])
                self.changeSingleCell([cell[0]+1, 0])
                self.rotateMultiCell([cell[0], cell[1]],[cell[0]+1, cell[1]],[cell[0], 0],[cell[0]+1, 0])
            else: # normalny przypadek
                self.changeSingleCell([cell[0], cell[1]])
                self.changeSingleCell([cell[0]+1, cell[1]])
                self.changeSingleCell([cell[0], cell[1] + 1])
                self.changeSingleCell([cell[0]+1, cell[1] + 1])
                self.rotateMultiCell([cell[0], cell[1]],[cell[0]+1, cell[1]],[cell[0], cell[1] + 1],[cell[0]+1, cell[1] + 1])
        else: # czyli 0,1,4 żywe komórki
            if cell[0] == self.size - 1 and cell[1] == self.size - 1:  # prawy dolny róg
                self.changeSingleCell([0,0])
                self.changeSingleCell([0, cell[1]])
                self.changeSingleCell([cell[0], 0])
                self.changeSingleCell([cell[0],cell[1]])
            elif cell[0] == self.size - 1:  # prawa strona
                self.changeSingleCell([0,cell[1]])
                self.changeSingleCell([cell[0], cell[1]])
                self.changeSingleCell([0, cell[1]+1])
                self.changeSingleCell([cell[0],cell[1]+1])
            elif cell[1] == self.size - 1:  # dół
                self.changeSingleCell([cell[0], cell[1]])
                self.changeSingleCell([cell[0]+1, cell[1]])
                self.changeSingleCell([cell[0], 0])
                self.changeSingleCell([cell[0]+1, 0])
            else: #normalny przypadek

                self.changeSingleCell([cell[0], cell[1]])
                self.changeSingleCell([cell[0]+1, cell[1]])
                self.changeSingleCell([cell[0], cell[1] + 1])
                self.changeSingleCell([cell[0]+1, cell[1] + 1])


    def updateBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                if i%2==self.grid and j%2==self.grid: #w jednym gridzie bierzemy same parzyste w innym same nieparzyste
                    self.changeMultiCell([i,j])


        if self.grid==0:
            self.grid=1
        else:
            self.grid=0
    def getColorOfCell(self,cell,flip):
        if self.board[cell[0]][cell[1]]== 1:
            if flip==True:
                return 0
            else:
                return 1
        else:
            if flip==True:
                return 1
            else:
                return 0
if __name__ == '__main__':
    size = 40
    b = Board(size)
    for i in range(800):
        b.setCellLive([random.randint(0,size-1), random.randint(0,size-1)])

    print(b)

    b.save("../resource/b6.txt")
