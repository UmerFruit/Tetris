import pygame
import sys
from game import Game
from colors import Colors
from blocks import*
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

