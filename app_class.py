import pygame, sys
import requests
import numpy as np
from copy import deepcopy
#from bs4 import Be autifulSoup

from settings import *
from buttonClass import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((352, 352))
        self.running = True
        self.grid = boarddefault
        self.gridtop = tasktop
        self.gridleft = taskleft
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.selectedCells = []
        self.font = pygame.font.SysFont("arial", cellSize//2)


    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            if self.allCellsDone():
                if self.checkRows() == True and self.checkCols() == True:
                    print("win")
                    self.state = "done"
                    self.running = False
                    pygame.quit()
                    sys.exit()
                else:
                    self.grid = [[0 for x in range(5)] for x in range(5)]

                    self.state = "playing"
                    self.running = True
                    self.selectedCells = []




### EVENT

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None

                if self.selected != None and self.selected != False:
                    if self.selected not in self.selectedCells:
                        self.grid[self.selected[1]][self.selected[0]] = 1
                        self.selectedCells.append(self.selected)
                    else:
                        selected = None
                        self.selectedCells.remove(self.selected)
                        self.grid[self.selected[1]][self.selected[0]] = 0
### update
    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()

# DRAW

    def playing_draw(self):
        self.window.fill(WHITE)
        #if self.selected:
        #    self.drawSelection(self.window, self.selected)
        self.drawNumbersBoard(self.window)
        self.shadeSelectedCells(self.window, self.selectedCells)
        self.drawNumbersTop(self.window)
        self.drawNumbersLeft(self.window)
        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

###  CHECKING

    def numofboard(self):
        sum = 0
        for yidx, row in enumerate(self.gridleft):
            for xidx, num in enumerate(row):
                sum=sum+num
        return sum

    def numofrow(self, rowleft):
        sum = 0
        for x, row in enumerate(self.gridleft[rowleft]):
            sum=sum+row
        return sum

    def numofcolums(self, colums):
        sum = 0
        for x, row in enumerate(self.gridtop[colums]):
            sum=sum+row
        return sum

    def rowDone(self, row):
        sum = 0
        for x in self.grid[row]:
            sum = sum + x
        if sum == self.numofrow(row):
            return True
        else:
            return False

    def columsDone(self, colums):
        sum = 0
        for yidx, row in enumerate(self.grid):
            sum = sum + self.grid[yidx][colums]
        if sum == self.numofcolums(colums):
            return True
        else:
            return False

    def allCellsDone(self):
        sum = 0
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                sum+=num
        if sum == self.numofboard():
            return True
        else:
            return False

    def checkAllCells(self):
        flag = None
        if self.allCellsDone():
            for x in range(5):
                if self.columsDone(x) and self.rowDone(x):
                    flag = True
        return flag

    def checkRows(self):
        for  i in range(len(self.grid)):
            constraint = deepcopy(self.gridleft[i])
            currentConstraint = 0
            for j in range(len(self.grid[i])):
                if(currentConstraint >= len(constraint) ):
                    break

                if(self.grid[i][j] == 1):
                    constraint[currentConstraint] = constraint[currentConstraint] - 1
                elif(j > 0
                    and self.grid[i][j-1] == 1
                    and self.grid[i][j] == 0):
                    currentConstraint += 1
            allZeros = not np.any(constraint)
            if allZeros == False:
                return False
        return True

    def checkCols(self):
        for i in range(len(self.grid[0])):
            constraint = deepcopy(self.gridtop[i])
            currentConstraint=0
            for j in range(len(self.grid)):
                if(currentConstraint >= len(constraint)):
                    break

                if(self.grid[j][i] == 1):
                    constraint[currentConstraint] = constraint[currentConstraint] - 1
                elif( j > 0 and self.grid[j-1][i] == 1 and self.grid[j][i] == 0):
                    currentConstraint += 1
            allZeros = not np.any(constraint)

            #Wenn eine Reihe/Spalte noch nicht gelöst ist
            if allZeros == False:
                return False
        return True


### HELPER FUNCTION

    #def createnono(self):
    #    sum = 0
    #    for yidx, row in enumerate(self.grid):
    #        for xidx, num in enumerate(row):
    #            pass


    def shadeSelectedCells(self, window, selection):
        for cell in selection:
            pygame.draw.rect(window, GREY, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    def drawNumbersBoard(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [xidx*cellSize+gridPos[0], yidx*cellSize+gridPos[1]]
                    self.textToScreen(window, str(num), pos)

    def drawNumbersLeft(self, window):
        for yidx, row in enumerate(self.gridleft):
            for xidx, num in enumerate(row):
                if num != 0 and num < 6:
                    if len(row) == 3:
                        pos = [xidx*cellSize//1.5+gridPos[0]-110, yidx*cellSize+gridPos[1]]
                        self.textToScreen(window, str(num), pos)
                    if len(row) == 2:
                        pos = [xidx*cellSize//1.5+gridPos[0]-76, yidx*cellSize+gridPos[1]]
                        self.textToScreen(window, str(num), pos)
                    if len(row) == 1:
                        pos = [xidx*cellSize//1.5+gridPos[0]-44, yidx*cellSize+gridPos[1]]
                        self.textToScreen(window, str(num), pos)

    def drawNumbersTop(self, window):
        for yidx, row in enumerate(self.gridtop):
            for xidx, num in enumerate(row):
                if num != 0 and num < 6:
                    if len(row) == 3:
                        pos = [yidx*cellSize+gridPos[0], xidx*cellSize//1.5+gridPos[1]-110]
                        self.textToScreen(window, str(num), pos)
                    if len(row) == 2:
                        pos = [yidx*cellSize+gridPos[0], xidx*cellSize//1.5+gridPos[1]-76]
                        self.textToScreen(window, str(num), pos)
                    if len(row) == 1:
                        pos = [yidx*cellSize+gridPos[0], xidx*cellSize//1.5+gridPos[1]-44]
                        self.textToScreen(window, str(num), pos)

    def drawSelection(self, windows, pos):
        pygame.draw.rect(windows, GREY, ((pos[0]*cellSize)+gridPos[0], (pos[1]*cellSize)+gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH-200, HEIGHT-200), 4)
        for x in range(6):
            pygame.draw.line(window, BLACK, (gridPos[0]+(x*cellSize), gridPos[1]-(2*cellSize)), (gridPos[0]+(x*cellSize), gridPos[1]+250), 2)
            pygame.draw.line(window, BLACK, (gridPos[0]-(2*cellSize), gridPos[1]+(x*cellSize)), (gridPos[0]+250, gridPos[1]+(x*cellSize)), 2)

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1]+gridSize:
            return False
        return ((self.mousePos[0]-gridPos[0])//cellSize, (self.mousePos[1]-gridPos[1])//cellSize)

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth)//2
        pos[1] += (cellSize - fontHeight)//2
        window.blit(font, pos)
