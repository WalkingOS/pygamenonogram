import random

WIDTH = 450
HEIGHT = 450

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (48,48,48)

boarddefault1 = [[random.randint(0, 1) for x in range(5)] for x in range(5)]

boarddefault = [[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]

tasktop = [[0,0,0],
         [0,0,0],
         [0,0,0],
         [0,0,0],
         [0,0,0]]

taskleft = [[0,0,0],
         [0,0,0],
         [0,0,0],
         [0,0,0],
         [0,0,0]]


gridPos = (100, 100)
cellSize = 50
gridSize = cellSize*5
