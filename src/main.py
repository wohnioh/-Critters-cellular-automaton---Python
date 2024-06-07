from tkinter import ttk, Tk

import sys
import time
from board import *
import pygame_widgets
from pygame_widgets.slider import Slider #pip install pygame widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import pygame
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile

from tkinter import ttk

windowScreenSize = (1000,600)
rect_size = 20
size = 100 #tylko parzyste liczby!!!
simulationSpeed = 50
simulationRunning = False

mainBoard = Board(size)

colorsFliped = False
delayVar = 0.1
screen = 0
window2 = 0
window1 = 0

centerX = 0
centerY = 0
m = 0
speedSlider = 100
speedText = 0
sizeSlider = 100
sizeText = 0

fileSelectButton = 0
apllyButton = 0
restartButton = 0
resetButton = 0
pauseButton = 0
iterationText = 0
reasumeButton = 0
flipColorsButton =0
greyBackground = 0
showGridButton = 0

colors = ["darkBlue", "white"]

currentIteration = 0

drawGrid = False

 # Act as label instead of textbox
def init():
    global screen
    global speedSlider
    global speedText
    global apllyButton
    global sizeText
    global sizeSlider
    global pauseButton
    global resetButton
    global reasumeButton
    global fileSelectButton
    global restartButton
    global flipColorsButton
    global iterationText
    global showGridButton
    pygame.init()
    screen = pygame.display.set_mode(windowScreenSize)
    speedSlider = Slider(screen, 25, 150, 350, 20, min=5, max=200, step=1)
    speedText = TextBox(screen, 25, 100, 160, 35, fontSize=20)
    sizeSlider = Slider(screen, 25, 250, 350, 20, min=2, max=50, step=1)
    sizeText = TextBox(screen, 25, 200, 150, 35, fontSize=20)
    apllyButton = Button(screen, 200, 20, 150, 30)
    apllyButton.setText("apply")
    resetButton = Button(screen, 25, 20, 150, 30)
    resetButton.setText("resetPos")
    reasumeButton = Button(screen, 200, 60, 150, 30)
    reasumeButton.setText("run")

    pauseButton = Button(screen, 25, 60, 150, 30)
    pauseButton.setText("pause")
    pauseButton.disable()
    restartButton = Button(screen, 40, 410, 300, 30)
    restartButton.setText("restart simulation")
    iterationText = TextBox(screen, 25, 450, 300, 35, fontSize=20)
    iterationText.setText("current Iteration = "+ str(currentIteration))

    flipColorsButton = Button(screen, 40, 300, 300, 30)
    flipColorsButton.setText("flip colors: False")

    showGridButton = Button(screen, 40, 340, 300, 30)
    showGridButton.setText("Show grid: False")

    showGridButton.setOnClick(showGridAction)
    flipColorsButton.setOnClick(flipColorsAction)
    restartButton.setOnClick(restartAction)
    apllyButton.setOnClick(applyAction)
    resetButton.setOnClick(resetPosAction)
    reasumeButton.setOnClick(reasumeAction)
    pauseButton.setOnClick(pauseAction)
    speedText.disable()

def showGridAction():
    global showGridButton
    global drawGrid
    if drawGrid == True:
        drawGrid = False
        showGridButton.setText("Show grid: False")
    else:
        drawGrid = True
        showGridButton.setText("Show grid: True")

def flipColorsAction():
    global colorsFliped
    global flipColorsButton
    if colorsFliped:
        colorsFliped = False
        flipColorsButton.setText("flip colors: False")
    else:
        colorsFliped = True
        flipColorsButton.setText("flip colors: True")
def applyAction():
    global simulationSpeed
    global sizeSlider
    global rect_size
    simulationSpeed = speedSlider.getValue()
    rect_size = sizeSlider.getValue()
def resetPosAction():
    global centerY
    global centerX
    centerX = 0
    centerY = 0
def reasumeAction():
    global simulationRunning
    global pauseButton
    global reasumeButton
    simulationRunning = True
    pauseButton.enable()
    reasumeButton.disable()

def pauseAction():
    global simulationRunning
    global pauseButton
    global reasumeButton
    simulationRunning = False

    pauseButton.disable()
    reasumeButton.enable()


def restartAction():
    global simulationRunning
    global pauseButton
    global reasumeButton
    global drawingParity
    global currentIteration

    simulationRunning = False
    pauseButton.disable()
    reasumeButton.enable()
    mainBoard.restartBoard()
    drawingParity =0
    currentIteration =0
    iterationText.setText("current Iteration = " + str(currentIteration))

def updateVariables(*args):
    global rect_size
    global delayVar
    global centerY
    global centerX
    '''
        rect_size = m.scaleScl.get()
    delayVar = m.timeScl.get()/10
    centerX = m.slider1.scl1.get()
    centerY = m.slider1.scl2.get()
    '''

    drawBoard()

def drawBoard():

    global greyBackground
    global colorsFliped
    global drawingParity


    width, height = windowScreenSize[0], windowScreenSize[1]
    movedX = centerX
    movedY = centerY

    for i in range(size):
        for j in range(size):
            correction = (size*rect_size)/2

            if colorsFliped:
                if drawingParity == 0:

                    pygame.draw.rect(screen, colors[mainBoard.getColorOfCell([i,j],False)], pygame.Rect(200+ width/2+ movedX + i*rect_size - correction,height/2+ movedY + j*rect_size - correction, rect_size, rect_size))
                else:

                    pygame.draw.rect(screen, colors[mainBoard.getColorOfCell([i, j], True)],
                                     pygame.Rect(200 + width / 2 + movedX + i * rect_size - correction,
                                                 height / 2 + movedY + j * rect_size - correction, rect_size,
                                                 rect_size))
            else:
                pygame.draw.rect(screen, colors[mainBoard.getColorOfCell([i, j], False)],
                                 pygame.Rect(200 + width / 2 + movedX + i * rect_size - correction,
                                             height / 2 + movedY + j * rect_size - correction, rect_size, rect_size))
    if drawGrid:
        if drawingParity ==0:
            for i in range(int(size/2)):
                j =0
                correction = (size * rect_size) / 2
                pygame.draw.rect(screen, "red",
                             pygame.Rect(200 + width / 2 + movedX + i*2 * rect_size - correction,
                                         height / 2 + movedY + j*2 * rect_size - correction, 2,
                                         size*rect_size))
            for j in range(int(size/2)):
                i =0
                correction = (size * rect_size) / 2
                pygame.draw.rect(screen, "red",
                             pygame.Rect(200 + width / 2 + movedX + i*2 * rect_size - correction,
                                         height / 2 + movedY + j*2 * rect_size - correction, size*rect_size,2
                                         ))
        else:
            for i in range(int(size/2)):
                j =0
                correction = (size * rect_size) / 2
                pygame.draw.rect(screen, "red",
                             pygame.Rect(rect_size+ 200 + width / 2 + movedX + i*2 * rect_size - correction,
                                         height / 2 + movedY + j*2 * rect_size - correction, 2,
                                         size*rect_size))
            for j in range(int(size/2)):
                i =0
                correction = (size * rect_size) / 2
                pygame.draw.rect(screen, "red",
                             pygame.Rect(200 + width / 2 + movedX + i*2 * rect_size - correction,rect_size+
                                         height / 2 + movedY + j*2 * rect_size - correction, size*rect_size,2
                                         ))
    greyBackground =pygame.Rect(0,0,400,height)

    pygame.draw.rect(screen,"white",greyBackground)
    pygame.draw.rect(screen, "darkgrey", pygame.Rect(20, 390, 360, 2))

firstTouch = True
initialPos = (0,0)
initialCenterX  = 0
initialCenterY =0
def game_event_loop():
    global firstTouch
    global initialPos
    global centerX
    global centerY
    global initialCenterX
    global initialCenterY
    events = pygame.event.get()
    pygame_widgets.update(events)
    pos = pygame.mouse.get_pos()
    state = pygame.mouse.get_pressed()
    if state[0] and not greyBackground.collidepoint(pos):
        if firstTouch:
            firstTouch = False
            initialPos = pos
            initialCenterX = centerX
            initialCenterY = centerY
        else:
            centerX = initialCenterX+ pos[0] - initialPos[0]
            centerY = initialCenterY+ pos[1] - initialPos[1]


    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONUP:
            firstTouch = True

        elif event.type == pygame.QUIT:
            pygame.quit(); sys.exit()



if __name__ == '__main__':
    global drawingParity
    drawingParity = 0
    #m = MainTkinter(updateVariables)
    mainBoard.load("../resource/b6.txt")  #b3.txt - widać glidery
    #b4 - widac glidery i wieksze pole
    #b6 - najciekawsza
    init()
    #m.window1.mainloop()
    refreshCounter = 0
    while True:


        screen.fill((0, 0, 0))
        drawBoard()

        if simulationRunning:
            refreshCounter += 1
            if refreshCounter >= simulationSpeed:
                currentIteration +=1
                mainBoard.updateBoard()
                if drawingParity == 0:
                    drawingParity = 1
                else:
                    drawingParity = 0
                refreshCounter = 0
                iterationText.setText("current Iteration = " + str(currentIteration))
        speedText.setText("speed: "+ str(speedSlider.getValue()*10)+" ms")
        sizeText.setText("size: " + str(sizeSlider.getValue() ) + " px")
        game_event_loop()
        pygame.display.flip()
        time.sleep(0.01)









