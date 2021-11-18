#########################################
# File Name: Snake.py
# Description: This program is a fully functional Snake Game.
#
# Author: Harry Xu
# Date: 11/17/2021
#########################################
from random import randint, uniform
import pygame
pygame.init()
WIDTH = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

# Colours
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
BLUE = (0, 0, 255)
RED = (255, 66, 66)
GREY = (25, 25, 25)
LGREY = (140, 140, 140)
ORANGE = (240, 147, 55)

# Menu Colours
VLCOLOUR = WHITE
LCOLOUR = WHITE
NCOLOUR = WHITE
SCOLOUR = WHITE

# Blcok size and roundedness
BLOCK_SIZE = 25
ROUNDEDNESS = int((BLOCK_SIZE * 3)//25)
ROUNDEDNESS_OBS = 3

BLOCK_X = WIDTH//BLOCK_SIZE
BLOCK_Y = HEIGHT//BLOCK_SIZE

BLOCK_R = 72
BLOCK_G = 0
BLOCK_B = 255

# Score
score = 0
totalScore = 0

# Levels
level = 1
applesNeeded = 8

# Fonts
scoreFont = pygame.font.SysFont("Bahnschrift", 30)
menuFontLarger = pygame.font.Font("fonts/MENUFONT.ttf", 120)
menuFontLarge = pygame.font.Font("fonts/MENUFONT.ttf", 60)
menuFont = pygame.font.Font("fonts/MENUFONT.ttf", 40)
menuFont2 = pygame.font.Font("fonts/MENUFONT.ttf", 20)

# Images
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

trophy = pygame.image.load("images/trophy.png")
trophy = pygame.transform.scale(trophy, (200, 200))

clock = pygame.image.load("images/clock.png")
clock = pygame.transform.scale(clock, (200, 200))

## Sounds ##

# Theme
pygame.mixer.init()
pygame.mixer.music.load("sounds/THEME.mp3")
pygame.mixer.music.set_volume(0.8)

# Apple Eat
appleEat = pygame.mixer.Sound("sounds/APPLEEAT.wav")
appleEat.set_volume(0.75)

# Lose the game
lose = pygame.mixer.Sound("sounds/LOSE.wav")
lose.set_volume(0.75)

# When button is clicked
menuNav = pygame.mixer.Sound("sounds/MENUNAV.wav")
menuNav.set_volume(0.75)

# Timer
FPS = 60
fpsClock = pygame.time.Clock()
timeLeft = 180
stopwatch = 0

# Time since the last apple was eaten
lastApple = 0
delay = 65

# Game log
games = []
#---------------------------------------#
# functions                             #
#---------------------------------------#
def redrawGameWindow():
    global appleGenerated, lastApple, timeLeft, applesNeeded, stopwatch
    TIME_COLOUR = WHITE
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255
    pygame.event.clear()
    gameWindow.fill(BLACK)
    if timeLeft <= 10:
        TIME_COLOUR = RED
    
    for i in range(round(BLOCK_X)):
        for j in range(round(BLOCK_Y)):
            if i % 2 == 0 and j % 2 == 0:
                pygame.draw.rect(gameWindow, GREY, (i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                
    for i in range(round(BLOCK_X)):
        for j in range(round(BLOCK_Y)):
            if i % 2 == 1 and j % 2 == 1:
                pygame.draw.rect(gameWindow, GREY, (i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for i in range(round(BLOCK_Y)):
        pygame.draw.rect(gameWindow, GREY, (0, i * BLOCK_SIZE, WIDTH, 1))    

    for i in range(len(obstaclesX)):
        obsCoordX = obstaclesX[i]
        obsCoordY = obstaclesY[i]
        pygame.draw.rect(gameWindow, ORANGE, (obsCoordX * BLOCK_SIZE, obsCoordY * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0, ROUNDEDNESS_OBS)

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

    scoreRender = ""
    # Setting for endless/adventure
    if level > 0:
        scoreRender = scoreFont.render(f"{score}/{applesNeeded}", True, WHITE)
    elif level == -1:
        leadZero = "0" if score < 10 else ""
        scoreRender = scoreFont.render(f"{leadZero}{score}", True, WHITE)

    gameWindow.blit(scoreRender, (WIDTH - 50, 10))
    # Setting for endless/adventure
    if level > 0:
        displayTime(timeLeft, 10, 10, TIME_COLOUR)
    elif level == -1:
        displayTime(stopwatch, 10, 10, TIME_COLOUR)
    time = fpsClock.tick(FPS)
    timeLeft -= time / 1000
    stopwatch += time / 1000
    lastApple += time / 1000
    if timeLeft <= 0:
        inPlay = False
    
    if lastApple >= 15:
        appleGenerated = False
        lastApple = 0
    
    pygame.display.update()
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255


def drawMenu(mousePos, clicked):
    pygame.event.clear()
    gameWindow.fill(BLACK)
    global LCOLOUR, NCOLOUR, SCOLOUR, VLCOLOUR, menu, BLOCK_SIZE, inPlay

    titleRender = menuFontLarge.render("Grid Size", True, WHITE)
    gameWindow.blit(titleRender, (260, 20))
    
    smallButton = pygame.draw.rect(gameWindow, LCOLOUR, (100, 120, 250, 150), 4)
    largeButton = pygame.draw.rect(gameWindow, NCOLOUR, (100, 370, 250, 150), 4)
    normalButton = pygame.draw.rect(gameWindow, SCOLOUR, (450, 120, 250, 150), 4)
    veryLargeButton = pygame.draw.rect(gameWindow, VLCOLOUR, (450, 370, 250, 150), 4)

    # Buttons
    LargeGridRender = menuFont.render("Small", True, WHITE)
    LargeGridRenderSub = menuFont2.render(f"{int(WIDTH//40)} x {int(HEIGHT//40)}", True, WHITE)
    gameWindow.blit(LargeGridRender, (165, 150))
    gameWindow.blit(LargeGridRenderSub, (185, 205))

    LargeGridRender = menuFont.render("Normal", True, WHITE)
    LargeGridRenderSub = menuFont2.render(f"{int(WIDTH//25)} x {int(HEIGHT//25)}", True, WHITE)
    gameWindow.blit(LargeGridRender, (500, 150))
    gameWindow.blit(LargeGridRenderSub, (535, 205))

    normalGridRender = menuFont.render("Large", True, WHITE)
    normalGridRenderSub = menuFont2.render(f"{int(WIDTH//12.5)} x {int(HEIGHT//12.5)}", True, WHITE)
    gameWindow.blit(normalGridRender, (165, 400))
    gameWindow.blit(normalGridRenderSub, (185, 455))

    LargeGridRender = menuFont.render("Very Large", True, WHITE)
    LargeGridRenderSub = menuFont2.render(f"{int(WIDTH//10)} x {int(HEIGHT//10)}", True, WHITE)
    gameWindow.blit(LargeGridRender, (460, 400))
    gameWindow.blit(LargeGridRenderSub, (530, 455))

    # Small button
    if smallButton.collidepoint(mousePos):
        LCOLOUR = LGREY

    if not smallButton.collidepoint(mousePos):
        LCOLOUR = WHITE

    if smallButton.collidepoint(mousePos) and clicked:
        menuNav.play()
        BLOCK_SIZE = 40
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()
    
    # Normal button
    if normalButton.collidepoint(mousePos):
        SCOLOUR = LGREY

    if not normalButton.collidepoint(mousePos):
        SCOLOUR = WHITE

    if normalButton.collidepoint(mousePos) and clicked:
        menuNav.play()
        BLOCK_SIZE = 25
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()        
    
    # Large button
    if largeButton.collidepoint(mousePos):
        NCOLOUR = LGREY

    if not largeButton.collidepoint(mousePos):
        NCOLOUR = WHITE

    if largeButton.collidepoint(mousePos) and clicked:
        menuNav.play()
        BLOCK_SIZE = 12.5
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()
        
    # Very Large button
    if veryLargeButton.collidepoint(mousePos):
        VLCOLOUR = LGREY

    if not veryLargeButton.collidepoint(mousePos):
        VLCOLOUR = WHITE

    if veryLargeButton.collidepoint(mousePos) and clicked:
        menuNav.play()
        BLOCK_SIZE = 12.5
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()
        
    pygame.display.update()

def drawTypeMenu(mousePos, clicked):
    pygame.event.clear()
    gameWindow.fill(BLACK)
    global LCOLOUR, NCOLOUR, SCOLOUR, VLCOLOUR, menu, BLOCK_SIZE, inPlay, endless

    titleRender = menuFontLarge.render("Game Mode", True, WHITE)
    gameWindow.blit(titleRender, (230, 20))
    
    smallButton = pygame.draw.rect(gameWindow, LCOLOUR, (100, 120, 250, 450), 4)
    veryLargeButton = pygame.draw.rect(gameWindow, VLCOLOUR, (450, 120, 250, 450), 4)

    gameWindow.blit(trophy, (125, 340))
    gameWindow.blit(clock, (475, 340))
    
    # Buttons
    SmallGridRender = menuFont.render("Adventure", True, WHITE)
    SmallGridRenderSub = menuFont2.render(f"", True, WHITE)
    gameWindow.blit(SmallGridRender, (115, 200))
    gameWindow.blit(SmallGridRenderSub, (185, 255))

    LargeGridRender = menuFont.render("Endless", True, WHITE)
    LargeGridRenderSub = menuFont2.render(f"", True, WHITE)
    gameWindow.blit(LargeGridRender, (500, 200))
    gameWindow.blit(LargeGridRenderSub, (530, 255))

    # Small button
    if smallButton.collidepoint(mousePos):
        LCOLOUR = LGREY

    if not smallButton.collidepoint(mousePos):
        LCOLOUR = WHITE

    if smallButton.collidepoint(mousePos) and clicked:
        menuNav.play()
        
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()
   
    # Very Large button
    if veryLargeButton.collidepoint(mousePos):
        VLCOLOUR = LGREY

    if not veryLargeButton.collidepoint(mousePos):
        VLCOLOUR = WHITE

    if veryLargeButton.collidepoint(mousePos) and clicked:
        menuNav.play()
        BLOCK_SIZE = 12.5
        menu = False
        inPlay = False
        endless = True

        gameWindow.fill(BLACK)
        pygame.display.update()
        
    pygame.display.update()


def checkCollision():
    # The snake has hit the walls
    if blocksX[0] < 0 or blocksX[0] + 1 > BLOCK_X:
        lose.play()
        return True

    if blocksY[0] < 0 or blocksY[0] + 1 > BLOCK_Y:
        lose.play()
        return True

    # The snake head as hit itself
    for i in range(len(blocksX) - 1):
        coord_x = blocksX[i + 1]
        coord_y = blocksY[i + 1]
        if blocksX[0] == coord_x and blocksY[0] == coord_y:
            lose.play()
            return True

    # The snake has hit an obstacle
    for i in range(len(obstaclesX)):
        coord_x = obstaclesX[i]
        coord_y = obstaclesY[i]
        if blocksX[0] == coord_x and blocksY[0] == coord_y:
            lose.play()
            return True

    # Nothing has been hit
    return False
        

def generateApple() -> list:
    apple_x = randint(0, BLOCK_X - 1)
    apple_y = randint(0, BLOCK_Y - 1)
    # Keeps generating until apple isn't in an obstacle or a snake
    while not generateAppleCheck(apple_x, apple_y):
        apple_x = randint(0, BLOCK_X - 1)
        apple_y = randint(0, BLOCK_Y - 1)
        
    appleX.append(apple_x)
    appleY.append(apple_y)
    

def generateAppleCheck(apple_x, apple_y):
    for i in range(len(blocksX)):
        if apple_x == blocksX[i] and apple_y == blocksY[i]:
            return False

    for i in range(len(obstaclesX)):
        if apple_x == obstaclesX[i] and apple_y == obstaclesY[i]:
            return False
        
    return True


def checkApple() -> bool:
    global appleX, appleY, appleGenerated, lastApple
    coord_x = blocksX[0]
    coord_y = blocksY[0]
    if coord_x in appleX and coord_y in appleY:
        for i in range(len(appleX) - 1, -1, -1):
            if appleX[i] == coord_x and appleY[i] == coord_y:
                del appleX[i]
                del appleY[i]

        if len(appleX) == 0:
            appleGenerated = False
            lastApple = 0
        appleEat.play()
        return True
    
    return False

def displayTime(time: float, x: int, y: int, COLOUR):
    timeToDisplay = ""
    strTime = round(time)
    leadingZero = 0 if strTime % 60 < 10 else ""
    if strTime >= 60:
        timeToDisplay = f"{int(strTime // 60)}:{leadingZero}{round(strTime % 60, 1)}"
    else:
        timeToDisplay = f"{round(strTime % 60, 1)}"
        
        
    stopwatch = scoreFont.render(f"{timeToDisplay}", True, COLOUR)
    gameWindow.blit(stopwatch, (x, y))

def checkScore():
    global score, delay
    if score % 3 == 0:
        speedMultiplier = score // 3
        newDelay = delay - speedMultiplier * 2
        if newDelay <= 10:
            newDelay = 10
        delay = newDelay


def checkWin():
    global score, inPlay
    if len(blocksX) >= BLOCK_X * BLOCK_Y:
        inPlay = False

def generateCheckLevel(obs_x, obs_y):
    # Prevents obstacles from being spawned directly in front of the snake head
    for i in range(4):
        if obs_x == BLOCK_X//2 and obs_y == BLOCK_Y//2 + 1:
            return False
        
    return True


def checkLevel(goal, timer):
    global score, level, inPlay, nextLevel, delay
    if score >= goal and timer > 0:
        level += 1 
        inPlay = False
        nextLevel = True
        if level == 2:
            obstaclesX.clear()
            obstaclesY.clear()
            for i in range(int(BLOCK_X * BLOCK_Y//184)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)
            delay = 60
            
        elif level == 3:
            obstaclesX.clear()
            obstaclesY.clear()
            for i in range(int(BLOCK_X * BLOCK_Y//144)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)
            delay = 55
            
        elif level == 4:
            obstaclesX.clear()
            obstaclesY.clear()
            for i in range(int(BLOCK_X * BLOCK_Y//112)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)
            delay = 52

        elif level == 5:
            obstaclesX.clear()
            obstaclesY.clear()
            for i in range(int(BLOCK_X * BLOCK_Y//96)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)
            delay = 50

        elif level >= 6:
            obstaclesX.clear()
            obstaclesY.clear()
            for i in range(int(BLOCK_X * BLOCK_Y//64)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)
            delay = 48


def displayLevel(levelToDisplay: int, endlessMode = False):
    gameWindow.fill(BLACK)
    levelText = menuFont.render(f"Level {levelToDisplay}", True, WHITE)
    if endlessMode:
        levelText = menuFont.render(f"Endless Mode", True, WHITE)
    if not endlessMode:
        gameWindow.blit(levelText, (330, 260))
    else:
        gameWindow.blit(levelText, (260, 260))
    pygame.display.update()
    pygame.time.delay(1000)
    

#---------------------------------------#
# main program                          #
#---------------------------------------#
# apple coords - maybe more than 1 apple later
appleX = []
appleY = []


# snake's properties
stepX = 0
stepY = -1                          

# each of the blocks X and Y coordinates
blocksX = []
blocksY = []

# each of the obstacles X and Y coordinates
obstaclesX = []
obstaclesY = []

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
nextLevel = False
endless = False

pygame.mixer.music.play(-1)
while inPlay:

    pygame.event.clear()

    if menu:
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
        drawTypeMenu(mousePos, mousePressed)

if not permaExit:
    inPlay = True

menu = True

pygame.time.delay(400)

while inPlay:

    pygame.event.clear()
    
    if menu:
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

if not permaExit:
    inPlay = True

menu = True

if endless:
    level =-1

pygame.time.delay(400)

BLOCK_X = WIDTH//BLOCK_SIZE
BLOCK_Y = HEIGHT//BLOCK_SIZE

# Displaying level if adventure mode, diplays "Endless Mode" is endless mode is on
if not endless:
    displayLevel(level)
elif endless:
    displayLevel(0, endlessMode=True)
    
while restart:
    # reset time
    fpsClock = pygame.time.Clock()
    pygame.mixer.music.play(-1)

    # Level
    if level == 1:
        timeLeft = 180
        applesNeeded = 8
    elif level == 2:
        timeLeft = 180
        applesNeeded = 10
    elif level == 3:
        timeLeft = 170
        applesNeeded = 10
    elif level == 4:
        timeLeft = 160
        applesNeeded = 10
    elif level == 5:
        timeLeft = 150
        applesNeeded = 10
    elif level >= 6:
        timeLeft = 140
        applesNeeded = 12
    while inPlay:
        # Checks
        pygame.event.clear()
        redrawGameWindow()
        checkWin()
        if not endless:
            checkLevel(applesNeeded, timeLeft)

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
            checkScore()
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
        
        if checkCollision():
            inPlay = False
            gameLogString = ""
            if level > 0:
                gameLogString = f"ADVENTURE | Level {level} : {score}/{applesNeeded} Apples"
            else:
                gameLogString = f"ENDLESS | Time : {round(stopwatch, 2)} | Score: {score}"
            games.append(gameLogString)

        if timeLeft < 0:
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

    pygame.mixer.music.pause()
    if nextLevel:
        displayLevel(level)
        inPlay = True
        endScreen = False
        nextLevel = False

        # Resetting for next level
        blocksX.clear()
        blocksY.clear()

        for i in range(4):
            blocksX.append(BLOCK_X//2)
            blocksY.append(BLOCK_Y//2 + i)
        appleX.clear()
        appleY.clear()

        score = 0
        MOVE_Q.clear()
        DIRECTION = UP
        appleGenerated = False
    
        lastApple = 0
    
    if endScreen:
        level = 1
        obstaclesX.clear()
        obstaclesY.clear()
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
            if endless:
                level =-1
            # Displaying level if adventure mode, diplays "Endless Mode" is endless mode is on
            if not endless:
                displayLevel(level)
            elif endless:
                displayLevel(0, endlessMode=True)
                
            inPlay = True
            lose.stop()
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


with open("logs.txt", 'a', 1) as log:
    for game in games:
        log.write(game + "\n")

with open("logs.txt", 'r', 1) as log:
    print(log.read())
    
pygame.quit()
