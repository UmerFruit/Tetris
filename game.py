import random
from grid import Grid
from blocks import *
from block import Block
class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(),
                       SBlock(), TBlock(), ZBlock()]
        self.currBlock = self.get_randBlock()
        self.nextBlock = self.get_randBlock()
        self.gameover = False
        self.score = 0
        self.completeRows = 0

    def update_score(self,linesCleared,move_downPoints):
        if linesCleared == 1:
            self.score += 100
        if linesCleared == 2:
            self.score += 300
        if linesCleared == 3:
            self.score += 500
        if linesCleared == 4:
            self.score += 700
        self.completeRows += linesCleared
        self.score += move_downPoints
    def get_randBlock(self):
        if len(self.blocks) == 0:
            self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(),
                           SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def draw(self, screen):
        self.grid.draw(screen)
        self.currBlock.draw(screen)
        if self.nextBlock.id == 3:
            self.nextBlock.draw_next(screen,695,290)
        elif self.nextBlock.id == 4:
            self.nextBlock.draw_next(screen,695,280)
        else:
            self.nextBlock.draw_next(screen,710,270)

    def move_left(self):
        self.currBlock.move(0, -1)
        if self.block_inside() == False or self.blockFits() == False:
            self.currBlock.move(0, 1)

    def move_right(self):
        self.currBlock.move(0, 1)
        if self.block_inside() == False or self.blockFits() == False:
            self.currBlock.move(0, -1)

    def move_down(self):
        self.currBlock.move(1, 0)
        if self.block_inside() == False or self.blockFits() == False:
            self.currBlock.move(-1, 0)
            self.lockBlock()

    def blockFits(self):
        tiles = self.currBlock.getCellpos()
        for tile in tiles:
            if self.grid.empty(tile.row, tile.col) == False:
                return False
        return True

    def reset(self):
        self.grid.reset()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.currBlock = self.get_randBlock()
        self.nextBlock = self.get_randBlock()
        self.score = 0

    def lockBlock(self):
        tiles = self.currBlock.getCellpos()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.currBlock.id
        self.currBlock = self.nextBlock
        self.nextBlock = self.get_randBlock()
        rows_cleared = self.grid.clearFullrows()
        self.update_score(rows_cleared,0)
        if self.blockFits() == False:
            self.gameover = True

    def block_inside(self):
        tiles = self.currBlock.getCellpos()
        for tile in tiles:
            if (self.grid.inside(tile.row, tile.col) == False):
                return False
        return True

    def rotate(self):
        self.currBlock.rotate()
        if self.block_inside() == False or self.blockFits() == False:
            self.currBlock.undorotate()
