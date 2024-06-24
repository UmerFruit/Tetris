import pygame
import sys
import random
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

class Position:
    def __init__(self,row,col):
        self.row = row
        self.col = col
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
class LBlock(Block):
    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0,5)

class JBlock(Block):
    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(2, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0,5)

class IBlock(Block):
    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1,5)

class OBlock(Block):
    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]
        }
        self.move(0,6)

class SBlock(Block):
    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0,5)

class TBlock(Block):

    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0,5)
class ZBlock(Block):
    def __init__(self):
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 2), Position(1, 1)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }  
        self.move(0,5)
class Colors:
    dark_grey = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    white = (255,255,255)
    dark_blue = (44, 44, 127)
    light_blue = (59,85,162)

    @classmethod
    def getCell_Colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
pygame.init()

title_font = pygame.font.Font(None,40)
score_surface = title_font.render("Score",True,Colors.white)
score_rect = pygame.Rect(820,55,170,60)
next_surface = title_font.render("Next",True,Colors.white)
next_rect = pygame.Rect(820,215,170,180)
lines_surface = title_font.render("Lines",True,Colors.white)
lines_rect = pygame.Rect(820,555,170,50)
gameOver_surface = title_font.render("GAME OVER",True,Colors.white)

screen = pygame.display.set_mode((500, 620),pygame.FULLSCREEN,32)
pygame.display.set_caption("Python Tetris")
game = Game()
fs = True
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE,200)

clock = pygame.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.gameover == True:
                game.gameover = False
                game.reset()
            if game.gameover == False:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0,1)
                if event.key == pygame.K_f:
                    fs = not fs
                if fs:
                    screen = pygame.display.set_mode((500, 620),pygame.FULLSCREEN,32)
                else:
                    screen = pygame.display.set_mode((500, 620),0,32)
                if event.key == pygame.K_UP:
                    game.rotate()
        if event.type == GAME_UPDATE and game.gameover == False :
            game.move_down()
    # Drawing
    screen.fill(Colors.dark_blue)
    scoreVal_surface = title_font.render(str(game.score),True,Colors.white)
    linesComp_surface = title_font.render(str(game.completeRows),True,Colors.white)
    screen.blit(score_surface,(865,20,50,50))
    screen.blit(next_surface,(875,180,50,50))
    screen.blit(lines_surface,(865,520,100,100))

    if game.gameover == True:
        screen.blit(gameOver_surface,(820,450,50,50))

    
    pygame.draw.rect(screen,Colors.light_blue,score_rect,0,10)
    screen.blit(scoreVal_surface,scoreVal_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    pygame.draw.rect(screen,Colors.light_blue,lines_rect,0,10)
    screen.blit(linesComp_surface,linesComp_surface.get_rect(centerx = lines_rect.centerx, centery = lines_rect.centery))

    pygame.draw.rect(screen,Colors.light_blue,next_rect,0,10)
    game.draw(screen)
    pygame.display.update()
    clock.tick(30)

