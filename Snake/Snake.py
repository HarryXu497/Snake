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

# Colours
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
BLUE = (0, 0, 255)
RED = (247, 27, 27)
GREY = (30, 30, 30)
LGREY = (140, 140, 140)

LCOLOUR = WHITE
NCOLOUR = WHITE
SCOLOUR = WHITE
VSCOLOUR = WHITE

BLOCK_SIZE = 25
ROUNDEDNESS = int((BLOCK_SIZE * 3)//25)

BLOCK_X = WIDTH//BLOCK_SIZE
BLOCK_Y = HEIGHT//BLOCK_SIZE

BLOCK_R = 72
BLOCK_G = 0
BLOCK_B = 255

# Score
score = 0

# Fonts
scoreFont = pygame.font.SysFont("Bahnschrift", 30)
menuFontLarge = pygame.font.Font("fonts/MENUFONT.ttf", 60)
menuFont = pygame.font.Font("fonts/MENUFONT.ttf", 40)
menuFont2 = pygame.font.Font("fonts/MENUFONT.ttf", 20)

# Images
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# Sounds
pygame.mixer.init()
pygame.mixer.music.load("sounds/THEME.mp3")

# Timer
FPS = 60
fpsClock = pygame.time.Clock()
timeElapsed = 0
lastApple = 0
delay = 70

#---------------------------------------#
# functions                             #
#---------------------------------------#
def redrawGameWindow():
    global appleGenerated, timeElapsed, lastApple
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255
    pygame.event.clear()
    gameWindow.fill(BLACK)

    for i in range(round(BLOCK_X)):
        pygame.draw.rect(gameWindow, GREY, (i * BLOCK_SIZE, 0, 1, HEIGHT))

    for i in range(round(BLOCK_Y)):
        pygame.draw.rect(gameWindow, GREY, (0, i * BLOCK_SIZE, WIDTH, 1))    


    for i in range(len(blocksX)):
        
        SEG_COLOUR = (BLOCK_R, BLOCK_G, BLOCK_B)
        coord_x = blocksX[i]
        coord_y = blocksY[i]
        pygame.draw.rect(gameWindow, SEG_COLOUR, (coord_x * BLOCK_SIZE, coord_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0, ROUNDEDNESS)
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
    lastApple += time / 1000
    
    if lastApple >= 30:
        appleGenerated = False
        lastApple = 0
    
    pygame.display.update()
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255


def drawMenu(mousePos, clicked):
    pygame.event.clear()
    gameWindow.fill(BLACK)
    global LCOLOUR, NCOLOUR, SCOLOUR, VSCOLOUR, menu, BLOCK_SIZE

    titleRender = menuFontLarge.render("Grid Size", True, WHITE)
    gameWindow.blit(titleRender, (260, 20))
    
    
    largeButton = pygame.draw.rect(gameWindow, LCOLOUR, (100, 120, 250, 150), 4)
    normalButton = pygame.draw.rect(gameWindow, NCOLOUR, (100, 370, 250, 150), 4)
    smallButton = pygame.draw.rect(gameWindow, SCOLOUR, (450, 120, 250, 150), 4)
    verySmallButton = pygame.draw.rect(gameWindow, VSCOLOUR, (450, 370, 250, 150), 4)

    # Buttons
    LargeGridRender = menuFont.render("Small", True, WHITE)
    LargeGridRenderSub = menuFont2.render("16 x 12", True, WHITE)
    gameWindow.blit(LargeGridRender, (165, 150))
    gameWindow.blit(LargeGridRenderSub, (185, 205))

    LargeGridRender = menuFont.render("Normal", True, WHITE)
    LargeGridRenderSub = menuFont2.render("32 x 24", True, WHITE)
    gameWindow.blit(LargeGridRender, (500, 150))
    gameWindow.blit(LargeGridRenderSub, (535, 205))

    normalGridRender = menuFont.render("Large", True, WHITE)
    normalGridRenderSub = menuFont2.render("64 x 48", True, WHITE)
    gameWindow.blit(normalGridRender, (165, 400))
    gameWindow.blit(normalGridRenderSub, (185, 455))

    LargeGridRender = menuFont.render("Very Large", True, WHITE)
    LargeGridRenderSub = menuFont2.render("80 x 60", True, WHITE)
    gameWindow.blit(LargeGridRender, (460, 400))
    gameWindow.blit(LargeGridRenderSub, (530, 455))

    # Large button
    if largeButton.collidepoint(mousePos):
        LCOLOUR = LGREY

    if not largeButton.collidepoint(mousePos):
        LCOLOUR = WHITE

    if largeButton.collidepoint(mousePos) and clicked:
        BLOCK_SIZE = 40
        menu = False

    # Normal button
    if normalButton.collidepoint(mousePos):
        NCOLOUR = LGREY

    if not normalButton.collidepoint(mousePos):
        NCOLOUR = WHITE

    if normalButton.collidepoint(mousePos) and clicked:
        BLOCK_SIZE = 12.5
        menu = False

    # Small button
    if smallButton.collidepoint(mousePos):
        SCOLOUR = LGREY

    if not smallButton.collidepoint(mousePos):
        SCOLOUR = WHITE

    if smallButton.collidepoint(mousePos) and clicked:
        BLOCK_SIZE = 25
        menu = False
        
    # Very Small button
    if verySmallButton.collidepoint(mousePos):
        VSCOLOUR = LGREY

    if not verySmallButton.collidepoint(mousePos):
        VSCOLOUR = WHITE

    if verySmallButton.collidepoint(mousePos) and clicked:
        BLOCK_SIZE = 10
        menu = False
        
    pygame.display.update()


def checkCollision():
    for i in range(len(blocksX) - 1):
        coord_x = blocksX[i + 1]
        coord_y = blocksY[i + 1]
        if blocksX[0] == coord_x and blocksY[0] == coord_y:
            return True
    return False
        

def generateApple() -> list:
    apple_x = randint(0, BLOCK_X - 1)
    apple_y = randint(0, BLOCK_Y - 1)
    # Keeps generating until apple isn't in 
    while (apple_x in blocksX) and (apple_y in blocksY):
        apple_x = randint(0, BLOCK_X)
        apple_y = randint(0, BLOCK_Y)
    
    appleX.append(apple_x)
    appleY.append(apple_y)
    

def checkApple() -> bool:
    global appleX, appleY, appleGenerated
    coord_x = blocksX[0]
    coord_y = blocksY[0]
    if coord_x in appleX and coord_y in appleY:
        for i in range(len(appleX) - 1, -1, -1):
            if appleX[i] == coord_x and appleY[i] == coord_y:
                del appleX[i]
                del appleY[i]
        appleGenerated = False
        return True
    
    return False

def displayTime(time: float, x: int, y: int):
    str_time = round(time, 1)
    stopwatch = scoreFont.render(f"{str_time}", True, WHITE)
    gameWindow.blit(stopwatch, (x, y))

def checkScore():
    global score, delay
    speedMultiplier = score // 3
    newDelay = 70 - speedMultiplier * 4
    delay = newDelay
    

#---------------------------------------#
# main program                          #
#---------------------------------------#
# apple coords - maybe more than 1 apple later
appleX = []
appleY = []


# snake's properties
stepX = 0
stepY = -1                          

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
menu = True
restart = True
permaExit = False
endScreen = False

while menu:
    mousePos = pygame.mouse.get_pos()
    mousePressed = pygame.mouse.get_pressed()[0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
        restart = False
        permaExit = True
        menu = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
            restart = False
            permaExit = True
            menu = False
    drawMenu(mousePos, mousePressed)

BLOCK_X = WIDTH//BLOCK_SIZE
BLOCK_Y = HEIGHT//BLOCK_SIZE
pygame.mixer.music.play(-1)
while restart:
    # reset time
    timeElapsed = 0
    fpsClock = pygame.time.Clock()
    
    while inPlay:
        pygame.event.clear()
        redrawGameWindow()
        checkScore()
        pygame.time.delay(delay)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            inPlay = False
            restart = False
            permaExit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
                restart = False
                permaExit = True
        
        if keys[pygame.K_a] and DIRECTION != 3:
            MOVE_Q.append(LEFT)
        elif keys[pygame.K_d] and DIRECTION != 2:
            MOVE_Q.append(RIGHT)
        elif keys[pygame.K_w] and DIRECTION != 1:
            MOVE_Q.append(UP)
        elif keys[pygame.K_s]  and DIRECTION != 0:
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
            print("collision")
            inPlay = False

    if not permaExit:
        endScreen = True

    # resetting game
    blocksX.clear()
    blocksY.clear()

    appleX.clear()
    appleY.clear()
    
    score = 0
    MOVE_Q.clear()
    DIRECTION = UP
    appleGenerated = False

    lastApple = 0
    
    for i in range(4):
        blocksX.append(BLOCK_X//2)
        blocksY.append(BLOCK_Y//2 + i)

    if endScreen:
        pygame.event.clear()
        gameWindow.fill(BLACK)
        
        restartButton = pygame.draw.rect(gameWindow, WHITE, (270, 300, 280, 100), 4)
        exitButton = pygame.draw.rect(gameWindow, WHITE, (310, 490, 200, 60), 4)
        gameWindow.blit(icon, (270, 0))
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
                restart = False
                permaExit = True
        
            
    
    
#---------------------------------------#    
pygame.quit()
