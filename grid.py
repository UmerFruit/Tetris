import pygame
from colors import Colors


class Grid:
    def __init__(self):
        self.rows = 20
        self.cols = 15
        self.cell_size = 37
        self.grid = [[0 for j in range(self.cols)]for i in range(self.rows)]
        self.colors = Colors.getCell_Colors()

    def printG(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.grid[row][col], end=" ")
            print()

    def empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False

    def rowFull(self, row):
        for col in range(self.cols):
            if self.grid[row][col] == 0:
                return False
        return True

    def moveRowdown(self, row, numrows):
        for col in range(self.cols):
            self.grid[row+numrows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clearFullrows(self):
        completed = 0
        for row in range(self.rows-1,0,-1):
            if self.rowFull(row):
                self.clearRow(row)
                completed += 1
            elif completed>0:
                self.moveRowdown(row,completed)
        return completed



    def clearRow(self, row):
        for col in range(self.cols):
            self.grid[row][col] = 0

    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col]=0
    # Draws the grid on to a surface
    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                cellVal = self.grid[row][col]
                cellRect = pygame.Rect(
                    col*self.cell_size+91, row*self.cell_size+17, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(screen, self.colors[cellVal], cellRect)

    def inside(self, row, col):
        if (row >= 0 and row < self.rows and col >= 0 and col < self.cols):
            return True
        return False
