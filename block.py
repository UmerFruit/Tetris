from colors import Colors
from position import Position
import pygame


class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 37
        self.rowOffset = 0
        self.colOffset = 0
        self.RotationState = 0
        self.colors = Colors.getCell_Colors()

    def draw(self, screen , xOffset = 91,yOffset= 17):
        tiles = self.getCellpos()
        for tile in tiles:
            tileRect = pygame.Rect(tile.col*self.cell_size+ xOffset, tile.row *self.cell_size+ yOffset, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(screen, self.colors[self.id], tileRect)

    def draw_next(self, screen , xOffset = 91,yOffset= 17):
        tiles = self.getCellpos()
        for tile in tiles:
            tileRect = pygame.Rect(tile.col*30+ xOffset, tile.row *30+ yOffset, 30-1, 30-1)
            pygame.draw.rect(screen, self.colors[self.id], tileRect)

    def move(self, rows, cols):
        self.rowOffset += rows
        self.colOffset += cols

    def undorotate(self):
        self.RotationState -= 1
        if self.RotationState == -1:
            self.RotationState = len(self.cells) - 1

    def rotate(self):
        self.RotationState += 1
        if self.RotationState == len(self.cells):
            self.RotationState = 0

    def getCellpos(self):
        tiles = self.cells[self.RotationState]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.rowOffset,
                                position.col + self.colOffset)
            moved_tiles.append(position)
        return moved_tiles
