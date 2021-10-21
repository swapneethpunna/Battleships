"""
Battleship Project
Name:
Roll No:
"""

from typing import Collection
import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["boardsize"]=500
    data["cellsize"]=data["boardsize"]/data["cols"]
    data["user_ships"]=5
    data["comp_ships"]=5
    data["user_board"]=emptyGrid(data["rows"],data["cols"])        
   # data["user_board"]=emptyGrid(data["rows"],data["no_of_cols"])
    data["comp_board"]=emptyGrid(data["rows"],data["cols"])
    data["comp_board"]=addShips(data["comp_board"],data["comp_ships"])
    data["temp_ships"]=[]
    data["user_track"]=0  
    data["winner"] =None
    data["max_num_of_turns"]=50
    data["current_num_of_turns"]=0           
    return


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["user_board"],True)
    drawShip(data,userCanvas,data["temp_ships"])
    drawGrid(data,compCanvas,data["comp_board"],False)
    drawGameOver(data,userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keycode==13:
        makeModel(data)
    return


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"]!=None:
        return
    mouse = getClickedCell(data,event)
    if board=="user":
        clickUserBoard(data,mouse[0],mouse[1])
    elif board=="comp":
        runGameTurn(data,mouse[0],mouse[1])
    return


#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        col=[]
        for j in range(cols):
            col.append(EMPTY_UNCLICKED)
        grid.append(col)
    return grid

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    cent_rows=random.randint(1,8)
    cent_cols=random.randint(1,8)
    center=random.randint(0,1)
    if center==0:
        ship=[[cent_rows-1,cent_cols],[cent_rows,cent_cols],[cent_rows+1,cent_cols]]
    else:
        ship=[[cent_rows,cent_cols-1],[cent_rows,cent_cols],[cent_rows,cent_cols+1]]
    return ship
    


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in ship:
        if grid[i[0]][i[1]]!=EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShip):
    count=0 
    while count<numShip: 
        ship=createShip() 
        if checkShip(grid, ship)==True: 
            for i in ship: 
                grid[i[0]][i[1]]=SHIP_UNCLICKED 
            count=count+1 
    return grid

    


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            if grid[row][col]==SHIP_UNCLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="yellow")
            elif grid[row][col]==EMPTY_UNCLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="blue")
            elif grid[row][col]==SHIP_CLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="red")
            elif grid[row][col]==EMPTY_CLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="white")
            if grid[row][col]==SHIP_UNCLICKED and showShips==False:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="blue")

    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1] == ship[1][1] == ship[2][1] and ship[0][0]+1==ship[1][0]== ship[2][0]-1:
        return True
    return False



'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0] == ship[1][0] == ship[2][0] and ship[0][1]+1==ship[1][1]== ship[2][1]-1:
        return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x=int(event.x/data["cellsize"])
    y=int(event.y/data["cellsize"])
    return [y,x]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in range(len(ship)):
        canvas.create_rectangle(data["cellsize"]*(ship[i][1]), data["cellsize"]*(ship[i][0]), data["cellsize"]*(ship[i][1]+1), data["cellsize"]*(ship[i][0]+1), fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship)==3:
        if checkShip(grid,ship) and (isVertical(ship)  or isHorizontal(ship)):
            return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["user_board"],data["temp_ships"]):
        for i in data["temp_ships"]:
            data["user_board"][i[0]][i[1]]=SHIP_UNCLICKED
        data["user_track"]+=1 
    else:
        print("error:ship is invalid")
    data["temp_ships"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["user_track"]==5:
        print("you can start the game")
        return
    if [row,col] in data["temp_ships"]:
        return
    data["temp_ships"].append([row,col])
    if len(data["temp_ships"])==3:
        placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict
 mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
    elif board[row][col]==EMPTY_UNCLICKED:
        board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["comp_board"][row][col]==SHIP_CLICKED or data["comp_board"][row][col]==EMPTY_CLICKED:
        return
    else:
        updateBoard(data,data["comp_board"],row,col,"user")
    x= getComputerGuess(data["user_board"])
    updateBoard(data,data["user_board"],x[0],x[1],"comp")
    data["current_num_of_turns"]+=1
    if data["current_num_of_turns"]==data["max_num_of_turns"]:
        data["winner"]="draw"
    return
    


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row=random.randint(0,9)
    col=random.randint(0,9)
    while board[row][col]==SHIP_CLICKED or board[row][col]==EMPTY_CLICKED:
        row=random.randint(0,9)
        col=random.randint(0,9)
    if board[row][col]==EMPTY_UNCLICKED or board[row][col]==SHIP_UNCLICKED:
        
        return [row,col]
        


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range (len(board)):
        for col in range(len(board[row])):
            if board[row][col]==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]=="user":
        canvas.delete(ALL)
        canvas.create_text(300, 50, text="congrats! you won the game", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(300, 100, text="press enter to play again", fill="black", font=('Helvetica 15 bold'))
    elif data["winner"]=="comp":
        canvas.delete(ALL)
        canvas.create_text(300, 50, text="you lost the game", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(300, 100, text="press enter to play again", fill="black", font=('Helvetica 15 bold'))
    elif data["winner"]=="draw":
        canvas.delete(ALL)
        canvas.create_text(300, 50, text="you are out of moves, Draw", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(300, 100, text="press enter to play again", fill="black", font=('Helvetica 15 bold'))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    ## Finally, run the simulation to test it manually ##

    # test.testIsHorizontal()
    #test.testGetComputerGuess()
    runSimulation(500, 500)
