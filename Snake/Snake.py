#########################################
# File Name: SnakeTemplate.py
# Description: This program is a template for Snake Game.
#              It demonstrates how to move and lengthen the snake.
# Author: ICS2O
# Date: 02/11/2020
#########################################
from random import randint
import pygame
pygame.init()
WIDTH = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

TOP = 0
BOTTOM = HEIGHT
MIDDLE = WIDTH//2
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
BLUE = (0, 0, 255)
RED = (247, 27, 27)
BLOCK_SIZE = 25


BLOCK_R = 72
BLOCK_G = 0
BLOCK_B = 255

# Score
score = 0

# Fonts
scoreFont = pygame.font.SysFont("Bahnschrift", 30)
menuFont = pygame.font.Font("fonts/MENUFONT.ttf", 40)
menuFont2 = pygame.font.Font("fonts/MENUFONT.ttf", 20)

# Images
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)


# Timer
FPS = 60
fpsClock = pygame.time.Clock()
timeElapsed = 0

#---------------------------------------#
# functions                             #
#---------------------------------------#
def redrawGameWindow():
    global appleGenerated, timeElapsed
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255
    pygame.event.clear()
    gameWindow.fill(BLACK)
    
    for i in range(len(blocksX)):
        
        SEG_COLOUR = (BLOCK_R, BLOCK_G, BLOCK_B)
        coord_x = blocksX[i]
        coord_y = blocksY[i]
        pygame.draw.rect(gameWindow, SEG_COLOUR, (coord_x * BLOCK_SIZE, coord_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0, 3)
        if BLOCK_R + 20 <= 255:
            BLOCK_R += 10
        if BLOCK_G + 20 <= 255:
            BLOCK_G += 10

    for i in range(len(appleX)):
        apple_x = appleX[i]
        apple_y = appleY[i]
        pygame.draw.circle(gameWindow, RED, (apple_x * BLOCK_SIZE + BLOCK_SIZE/2, apple_y * BLOCK_SIZE + BLOCK_SIZE/2), BLOCK_SIZE/2)
    
    if not appleGenerated:
        generateApple()
        appleGenerated = True

    scoreRender = scoreFont.render(f"{score}", True, WHITE)
    gameWindow.blit(scoreRender, (770, 10))

    displayTime(timeElapsed, 10, 10)
    time = fpsClock.tick(FPS)
    timeElapsed += time / 1000
    
    pygame.display.update()
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255


def checkCollision():
    for i in range(len(blocksX) - 1):
        coord_x = blocksX[i + 1]
        coord_y = blocksY[i + 1]
        if blocksX[0] == coord_x and blocksY[0] == coord_y:
            return True
    return False
        

def generateApple() -> list:
    apple_x = randint(0, BLOCK_X)
    apple_y = randint(0, BLOCK_Y)
    while (apple_x in blocksX) and (apple_y in blocksY):
        apple_x = randint(0, BLOCK_X)
        apple_y = randint(0, BLOCK_Y)
    
    appleX.append(apple_x)
    appleY.append(apple_y)
    

def checkApple() -> bool:
    global appleX, appleY
    coord_x = blocksX[0]
    coord_y = blocksY[0]
    if coord_x in appleX and coord_y in appleY:
        appleX.clear()
        appleY.clear()
        return True
    
    return False

def displayTime(time: float, x: int, y: int):
    str_time = round(time, 1)
    stopwatch = scoreFont.render(f"{str_time}", True, WHITE)
    gameWindow.blit(stopwatch, (x, y))
    

#---------------------------------------#
# main program                          #
#---------------------------------------#
# apple coords - maybe more than 1 apple later
appleX = []
appleY = []


# snake's properties
stepX = 0
stepY = -1                          

BLOCK_X = WIDTH//BLOCK_SIZE
BLOCK_Y = HEIGHT//BLOCK_SIZE

head = [BLOCK_X//2, BLOCK_Y//2]

blocksX = []
blocksY = []


# direction constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
DIRECTION = UP
# 0 = up
# 1 = down
# 2 = left
# 3 = right

MOVE_Q = []
for i in range(4):                      # add coordinates for the head and 3 segments
    blocksX.append(BLOCK_X//2)
    blocksY.append(BLOCK_Y//2 + i)
    
#---------------------------------------#
appleGenerated = False
inPlay = True
restart = True
permaExit = False
endScreen = False
while restart:
    # reset time
    timeElapsed = 0
    fpsClock = pygame.time.Clock()
    
    while inPlay:
        pygame.event.clear()
        redrawGameWindow()
        pygame.time.delay(60)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            inPlay = False
            restart = False
            permaExit = True
            
        if keys[pygame.K_LEFT] and DIRECTION != 3:
            MOVE_Q.append(LEFT)
        if keys[pygame.K_RIGHT] and DIRECTION != 2:
            MOVE_Q.append(RIGHT)
        if keys[pygame.K_UP] and DIRECTION != 1:
            MOVE_Q.append(UP)
        if keys[pygame.K_DOWN]  and DIRECTION != 0:
            MOVE_Q.append(DOWN)
                
        if len(MOVE_Q) >= 1:
            DIRECTION = MOVE_Q.pop(0)
        
        
        if DIRECTION == LEFT:
            stepX = -1
            stepY = 0
        if DIRECTION == RIGHT:
            stepX = 1
            stepY = 0
        if DIRECTION == UP:
            stepX = 0
            stepY = -1
        if DIRECTION == DOWN:
            stepX = 0
            stepY = 1

        if checkApple():
            if len(blocksX) <= 1:           
                blocksX.append(blocksX[-1] - stepX)           
                blocksY.append(blocksY[-1] - stepY)
            else:
                change_X = blocksX[-1] - blocksX[-2]
                change_Y = blocksY[-1] - blocksY[-2]
                blocksX.append(blocksX[-1] + change_X)
                blocksY.append(blocksY[-1] + change_Y)
            appleGenerated = False
            score += 1
        
        
        # move the segments

        lastIndex = len(blocksX) - 1

        for i in range(lastIndex,0,-1):     
            blocksX[i] = blocksX[i-1]
            blocksY[i] = blocksY[i-1]

            change_X = blocksX[-1] - blocksX[-2]
            change_Y = blocksY[-1] - blocksY[-2]
            
        blocksX[0] += stepX
        blocksY[0] += stepY

        if blocksX[0] < 0 or blocksX[0] + 1 > BLOCK_X:
            inPlay = False

        if blocksY[0] < 0 or blocksY[0] + 1 > BLOCK_Y:
            inPlay = False

        if checkCollision():
            inPlay = False

        pygame.time.delay(10)

    if not permaExit:
        endScreen = True

    # resetting game
    blocksX.clear()
    blocksY.clear()

    appleX.clear()
    appleY.clear()
    
    score = 0
    DIRECTION = UP
    appleGenerated = False

    
    for i in range(4):
        blocksX.append(BLOCK_X//2)
        blocksY.append(BLOCK_Y//2 + i)

    if endScreen:
        pygame.event.clear()
        gameWindow.fill(BLACK)
        
        restartButton = pygame.draw.rect(gameWindow, WHITE, (270, 300, 280, 100), 4)
        exitButton = pygame.draw.rect(gameWindow, WHITE, (310, 490, 200, 60), 4)
        gameWindow.blit(icon, (280, 0))
        restartText = menuFont.render("Play Again?", True, WHITE)
        exitText = menuFont.render("Exit", True, WHITE)
        gameWindow.blit(restartText, (282, 325))
        gameWindow.blit(exitText, (365, 495))
        
        pygame.display.update()
        
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()[0]

        if restartButton.collidepoint(mousePos) and mousePressed:
            inPlay = True
        if exitButton.collidepoint(mousePos) and mousePressed:
            endScreen = False
            restart = False
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            inPlay = False
            restart = False
            permaExit = True
            
    
    
#---------------------------------------#    
pygame.quit()
