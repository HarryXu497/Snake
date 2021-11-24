#########################################
# File Name: Snake.py
# Description: This program is a fully functional Snake Game.
#
# Author: Harry Xu
# Date: 11/17/2021
#########################################
from random import randint
import datetime
import pygame

# initializing python
pygame.init()

WIDTH = 800
HEIGHT = 600

# Colours #####################################################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 66, 66)
SCORE_RED = (255, 0, 0)
DRED = (222, 33, 33)
GREY = (25, 25, 25)
LGREY = (140, 140, 140)
ORANGE = (240, 147, 55)
# PURPLE = (72, 0, 255)

# Menu Colours
VLCOLOUR = WHITE
LCOLOUR = WHITE
NCOLOUR = WHITE
SCOLOUR = WHITE

# Exit screen colours
RCOLOUR = WHITE
ECOLOUR = WHITE

# --------------------------------------------------------------------------- #

# Block size and roundedness
BLOCK_SIZE = 25
ROUNDEDNESS = int((BLOCK_SIZE * 3) // 25)  # Keeps the rounded-ness proportional to the size of the square
ROUNDEDNESS_OBS = 3  # rounded-ness of the obstacles

# The width and height of the coordinate plane
BLOCK_X = WIDTH // BLOCK_SIZE
BLOCK_Y = HEIGHT // BLOCK_SIZE

# Initial segments that you start with
INITIAL_SEGMENTS = 4

# Score #######################################################
score = 0
totalScore = 0

# Levels ######################################################
level = 1
applesNeeded = 8

ENDLESS = -1

# Setting game window
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
# gameWindow = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF, pygame.FULLSCREEN)

# Images ######################################################
icon = pygame.image.load("images/icon.png")

trophy = pygame.image.load("images/trophy.png")
trophy = pygame.transform.scale(trophy, (200, 200))

clock = [
    pygame.image.load("images/clock/clock1.png"),
    pygame.image.load("images/clock/clock2.png"),
    pygame.image.load("images/clock/clock3.png"),
    pygame.image.load("images/clock/clock4.png"),
    pygame.image.load("images/clock/clock5.png"),
    pygame.image.load("images/clock/clock6.png"),
    pygame.image.load("images/clock/clock7.png"),
    pygame.image.load("images/clock/clock8.png"),
]

for i in range(len(clock)):
    clock[i] = pygame.transform.scale(clock[i], (200, 200))

# For controlling clock animation
clockNum = 0

# Responsible for icon bobbing
iconBobbing = 0

# Icon, Caption and Cursor ####################################
pygame.display.set_icon(icon)  # setting icon
pygame.display.set_caption("Snake")
pygame.mouse.set_cursor(pygame.cursors.diamond)

# Fonts #######################################################
scoreFont = pygame.font.SysFont("Bahnschrift", 30)
menuFontLarger = pygame.font.Font("fonts/MENUFONT.ttf", 120)
menuFontLarge = pygame.font.Font("fonts/MENUFONT.ttf", 60)
menuFont = pygame.font.Font("fonts/MENUFONT.ttf", 40)
menuFont2 = pygame.font.Font("fonts/MENUFONT.ttf", 20)

menuFontTitle = pygame.font.Font("fonts/MENUFONTITLE.ttf", 80)

# Sounds ######################################################################

# Theme
pygame.mixer.init()  # I don't think this is needed - test later
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

# When button is clicked
nextLevelSound = pygame.mixer.Sound("sounds/NEXTLEVEL.wav")
nextLevelSound.set_volume(0.75)

# --------------------------------------------------------------------------- #


# Time #######################################################################
FPS = 60
fpsClock = pygame.time.Clock()
timeLeft = 180
stopwatch = 0

# Time since the last apple was eaten
lastApple = 0

# when lastApple is equal to this, a new apple is generated
LASTAPPLETIME = 15

# speed
delay = 65

# death animation time - speeds up the death animation after the sound effect ends
deathAnimationTime = 0

# death stopwatch time - to control the rate at which the snake "dies"
deathAnimationStopwatch = 0

# The rate of the death animation
# we use 2 variables because we need to reset the rate of death to the same as before between levels
rateOfDeathAnimationInit = 10

rateOfDeathAnimation = rateOfDeathAnimationInit

# --------------------------------------------------------------------------- #


# Snake properties ############################################################
# how much to move by
stepX = 0
stepY = 0

# each of the blocks X and Y coordinates
blocksX = []
blocksY = []

# --------------------------------------------------------------------------- #


# Apple properties ############################################################

# apple coordinates
appleX = []
appleY = []

# --------------------------------------------------------------------------- #


# Obstacle properties #########################################################

# each of the obstacles X and Y coordinates
obstaclesX = []
obstaclesY = []

# --------------------------------------------------------------------------- #

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

# Movement queue
MOVE_Q = []

# Game logs
games = []


###############################################################################
#
# Functions
#
###############################################################################
def redrawGameWindow() -> None:
    """
    Redraws the game window when called. Draws the snake segments,
    grid, apples and obstacles

    Return => None
    """
    global appleGenerated, lastApple, timeLeft, applesNeeded, stopwatch, inPlay, win, flipSegmentColour
    TIME_COLOUR = WHITE
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255

    pygame.event.clear()

    gameWindow.fill(BLACK)

    # Turns the timer colour to red if there is less than 10 seconds
    if timeLeft <= 20:
        if round(timeLeft) % 2 == 0:
            TIME_COLOUR = SCORE_RED
        else:
            TIME_COLOUR = WHITE

    # Ends the game if time runs out
    if timeLeft <= 0:
        inPlay = False

    # Draws the grid ##########################################################
    for j in range(round(BLOCK_X)):
        for k in range(round(BLOCK_Y)):
            if j % 2 == 0 and k % 2 == 0:
                pygame.draw.rect(gameWindow, GREY, (j * BLOCK_SIZE, k * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for j in range(round(BLOCK_X)):
        for k in range(round(BLOCK_Y)):
            if j % 2 == 1 and k % 2 == 1:
                pygame.draw.rect(gameWindow, GREY, (j * BLOCK_SIZE, k * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # ----------------------------------------------------------------------- #

    # Draws the obstacles #####################################################
    for j in range(len(obstaclesX)):
        obsCoordX = obstaclesX[j]
        obsCoordY = obstaclesY[j]
        pygame.draw.rect(gameWindow, ORANGE, (obsCoordX * BLOCK_SIZE, obsCoordY * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                         0, ROUNDEDNESS_OBS)

    # ----------------------------------------------------------------------- #

    # Draws the snake segments ################################################
    for j in range(len(blocksX)):
        SEG_COLOUR = (BLOCK_R, BLOCK_G, BLOCK_B)
        coord_x = blocksX[j]
        coord_y = blocksY[j]

        pygame.draw.rect(gameWindow, SEG_COLOUR, (coord_x * BLOCK_SIZE, coord_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                         0, ROUNDEDNESS)

        # Changes the color to make a gradient
        if BLOCK_R + 20 <= 255 and not flipSegmentColour:
            BLOCK_R += 10

        elif BLOCK_R + 20 > 255:
            flipSegmentColour = True

        if BLOCK_G + 20 <= 255 and not flipSegmentColour:
            BLOCK_G += 10

        if BLOCK_R > 82 and flipSegmentColour:
            BLOCK_R -= 10

        elif BLOCK_R <= 82:
            flipSegmentColour = False

        if BLOCK_G - 20 >= 0 and flipSegmentColour:
            BLOCK_G -= 10

        # ----------------------------------------------------------------------- #

    # Draws the apples ########################################################
    for j in range(len(appleX)):
        apple_x = appleX[j]
        apple_y = appleY[j]
        pygame.draw.circle(gameWindow, RED,
                           (apple_x * BLOCK_SIZE + BLOCK_SIZE / 2, apple_y * BLOCK_SIZE + BLOCK_SIZE / 2),
                           BLOCK_SIZE / 2)
        pygame.draw.circle(gameWindow, DRED,
                           (apple_x * BLOCK_SIZE + BLOCK_SIZE / 2, apple_y * BLOCK_SIZE + BLOCK_SIZE / 2),
                           BLOCK_SIZE / 2, 2)

    # ----------------------------------------------------------------------- #

    # Generates apple if there are none
    if not appleGenerated:
        generateApple()
        appleGenerated = True

    # Setting the score for endless/adventure #################################
    if level > 0 and not win:
        # Renders the font, depending on the game mode
        scoreRender = scoreFont.render(f"{score}/{applesNeeded}", True, WHITE)
        gameWindow.blit(scoreRender, (WIDTH - 70, 10))

    elif level == ENDLESS and not win:
        # Renders the font, depending on the game mode
        leadZero = "0" if score < 10 else ""
        scoreRender = scoreFont.render(f"{leadZero}{score}", True, WHITE)
        gameWindow.blit(scoreRender, (WIDTH - 50, 10))

    # ----------------------------------------------------------------------- #

    # Setting clock to timer/stopwatch for endless/adventure ##################
    if level >= 0 and not win:
        displayTime(timeLeft, 10, 10, TIME_COLOUR)

    elif level == ENDLESS and not win:
        displayTime(stopwatch, 10, 10, TIME_COLOUR)

    # ----------------------------------------------------------------------- #

    # Accumulating time
    time = fpsClock.tick(FPS)
    timeLeft -= time / 1000  # Adventure mode timer
    stopwatch += time / 1000  # Endless mode stopwatch
    lastApple += time / 1000  # Records the time since the last apple was eaten

    # Generates apple if no apples are consumed in the last n seconds
    if lastApple >= LASTAPPLETIME:
        appleGenerated = False
        lastApple = 0

    # Updating screen
    pygame.display.update()


def drawMenu(mousePosition: tuple[int, int], mouseClicked: bool) -> None:
    """
    Draws the grid size menu. The mouse position and left click are passed as parameters

    Parameters:
        mousePosition -> a tuple of the mouse's x and y position.
        clicked -> a boolean for whether left click is clicked or not

    Return => None
    """
    pygame.event.clear()
    gameWindow.fill(BLACK)

    global LCOLOUR, NCOLOUR, SCOLOUR, VLCOLOUR, menu, BLOCK_SIZE, inPlay

    # Title
    titleRender = menuFontTitle.render("Grid Size", True, WHITE)
    gameWindow.blit(titleRender, (235, 20))

    # Button rectangles/outlines
    smallButton = pygame.draw.rect(gameWindow, LCOLOUR, (100, 120, 250, 200), 4)
    normalButton = pygame.draw.rect(gameWindow, SCOLOUR, (450, 120, 250, 200), 4)
    largeButton = pygame.draw.rect(gameWindow, NCOLOUR, (100, 370, 250, 200), 4)
    veryLargeButton = pygame.draw.rect(gameWindow, VLCOLOUR, (450, 370, 250, 200), 4)

    # Button Text #############################################################

    # Small grid button
    smallGridRender = menuFont.render("Small", True, WHITE)
    smallGridRenderSub = menuFont2.render(f"{int(WIDTH // 40)} x {int(HEIGHT // 40)}", True, WHITE)
    gameWindow.blit(smallGridRender, (165, 175))
    gameWindow.blit(smallGridRenderSub, (185, 230))

    # Normal grid button
    normalGridRender = menuFont.render("Normal", True, WHITE)
    normalGridRenderSub = menuFont2.render(f"{int(WIDTH // 25)} x {int(HEIGHT // 25)}", True, WHITE)
    gameWindow.blit(normalGridRender, (500, 175))
    gameWindow.blit(normalGridRenderSub, (535, 230))

    # Large grid button
    largeGridRender = menuFont.render("Large", True, WHITE)
    largeGridRenderSub = menuFont2.render(f"{int(WIDTH // 12.5)} x {int(HEIGHT // 12.5)}", True, WHITE)
    gameWindow.blit(largeGridRender, (165, 425))
    gameWindow.blit(largeGridRenderSub, (185, 480))

    # Very Large grid button
    veryLargeGridRender = menuFont.render("Very Large", True, WHITE)
    veryLargeGridRenderSub = menuFont2.render(f"{int(WIDTH // 10)} x {int(HEIGHT // 10)}", True, WHITE)
    gameWindow.blit(veryLargeGridRender, (460, 425))
    gameWindow.blit(veryLargeGridRenderSub, (535, 480))

    # ----------------------------------------------------------------------- #

    # Button Collisions #######################################################

    ## Small button ###########################################
    if smallButton.collidepoint(mousePosition):
        # changes colour to grey on hover
        LCOLOUR = BLACK  # turns original rectangle black and makes a slightly larger grey one
        smallButton = pygame.draw.rect(gameWindow, LGREY, (98, 118, 254, 204), 4)

    if not smallButton.collidepoint(mousePosition):
        LCOLOUR = WHITE

    if smallButton.collidepoint(mousePosition) and mouseClicked:
        # Button is clicked; start game
        menuNav.play()
        BLOCK_SIZE = 40
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()

    # ------------------------------------------------------- #

    ## Normal button ##########################################
    if normalButton.collidepoint(mousePosition):
        # changes colour to grey on hover
        SCOLOUR = BLACK  # turns original rectangle black and makes a slightly larger grey one
        normalButton = pygame.draw.rect(gameWindow, LGREY, (448, 118, 254, 204), 4)

    if not normalButton.collidepoint(mousePosition):
        SCOLOUR = WHITE

    if normalButton.collidepoint(mousePosition) and mouseClicked:
        # Button is clicked; start game
        menuNav.play()
        BLOCK_SIZE = 25
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()

    # ------------------------------------------------------- #

    ## Large button ###########################################
    if largeButton.collidepoint(mousePosition):
        # changes colour to grey on hover
        NCOLOUR = BLACK  # turns original rectangle black and makes a slightly larger grey one
        largeButton = pygame.draw.rect(gameWindow, LGREY, (98, 368, 254, 204), 4)

    if not largeButton.collidepoint(mousePosition):
        NCOLOUR = WHITE

    if largeButton.collidepoint(mousePosition) and mouseClicked:
        # Button is clicked; start game
        menuNav.play()
        BLOCK_SIZE = 12.5
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()

    # ------------------------------------------------------- #

    ## Very Large button ######################################
    if veryLargeButton.collidepoint(mousePosition):
        # changes colour to grey on hover
        VLCOLOUR = BLACK  # turns original rectangle black and makes a slightly larger grey one
        veryLargeButton = pygame.draw.rect(gameWindow, LGREY, (448, 368, 254, 204), 4)

    if not veryLargeButton.collidepoint(mousePosition):
        VLCOLOUR = WHITE

    if veryLargeButton.collidepoint(mousePosition) and mouseClicked:
        # Button is clicked; start game
        menuNav.play()
        BLOCK_SIZE = 10
        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()

    # ------------------------------------------------------- #

    # ----------------------------------------------------------------------- #

    pygame.display.update()


def drawTypeMenu(mousePosition: tuple[int, int], mouseClicked: bool) -> None:
    """
    Draws the game mode menu. The mouse position and left click are passed as parameters

    Parameters:
        mousePosition -> a tuple of the mouse's x and y position.
        clicked -> a boolean for whether left click is clicked or not

    Return => None
    """

    pygame.event.clear()
    gameWindow.fill(BLACK)

    global LCOLOUR, NCOLOUR, SCOLOUR, VLCOLOUR, menu, BLOCK_SIZE, inPlay, endless, clockNum, iconBobbing

    # Title
    titleRender = menuFontTitle.render("Game Mode", True, WHITE)
    gameWindow.blit(titleRender, (190, 20))

    # Button rectangles/outline
    adventureButton = pygame.draw.rect(gameWindow, LCOLOUR, (100, 120, 250, 450), 4)
    endlessButton = pygame.draw.rect(gameWindow, VLCOLOUR, (450, 120, 250, 450), 4)

    # Blitting the icons to the game modes
    gameWindow.blit(trophy, (125, 330 if iconBobbing > 4 else 340))
    gameWindow.blit(clock[int(clockNum)] if endlessButton.collidepoint(mousePosition) else clock[0], (475, 340 if iconBobbing > 4 else 330))

    # Button Text #############################################################
    SmallGridRender = menuFont.render("Adventure", True, WHITE)
    SmallGridRenderSub = menuFont2.render(f"", True, WHITE)
    gameWindow.blit(SmallGridRender, (115, 200))
    gameWindow.blit(SmallGridRenderSub, (185, 255))

    LargeGridRender = menuFont.render("Endless", True, WHITE)
    LargeGridRenderSub = menuFont2.render(f"", True, WHITE)
    gameWindow.blit(LargeGridRender, (500, 200))
    gameWindow.blit(LargeGridRenderSub, (530, 255))

    # ----------------------------------------------------------------------- #

    # Button Collisions #######################################################

    # Adventure button ########################################
    if adventureButton.collidepoint(mousePosition):
        # button turns grey on hover
        LCOLOUR = BLACK  # turns original rectangle black and makes a slightly larger grey one
        adventureButton = pygame.draw.rect(gameWindow, LGREY, (98, 118, 254, 454), 4)

    if not adventureButton.collidepoint(mousePosition):
        LCOLOUR = WHITE

    if adventureButton.collidepoint(mousePosition) and mouseClicked:
        # Button is clicked; start game
        menuNav.play()

        menu = False
        inPlay = False

        gameWindow.fill(BLACK)
        pygame.display.update()
    # ------------------------------------------------------- #

    # Endless button ##########################################
    if endlessButton.collidepoint(mousePosition):
        # button turns grey on hover
        VLCOLOUR = BLACK  # turns original rectangle black and makes a slightly larger grey one
        endlessButton = pygame.draw.rect(gameWindow, LGREY, (448, 118, 254, 454), 4)

    if not endlessButton.collidepoint(mousePosition):
        clockNum = 0
        VLCOLOUR = WHITE

    if endlessButton.collidepoint(mousePosition) and mouseClicked:
        # Button is clicked; start game
        menuNav.play()
        menu = False
        inPlay = False
        endless = True

        gameWindow.fill(BLACK)
        pygame.display.update()
    # ------------------------------------------------------- #

    # ----------------------------------------------------------------------- #

    clockNum += 0.005
    iconBobbing += 0.005
    if iconBobbing >= 8:
        iconBobbing = 0

    if clockNum >= len(clock):
        clockNum = 0

    pygame.display.update()


def drawEndMenu(mousePosition: tuple[int, int], mouseClicked: bool) -> None:
    """
    Draws the end screen menu. The mouse position and left click are passed as parameters

    Parameters:
        mousePosition -> a tuple of the mouse's x and y position.
        clicked -> a boolean for whether left click is clicked or not

    Return => None
    """
    global RCOLOUR, ECOLOUR, level, win, inPlay, endScreen, restart, keys, deathAnimation, clockNum
    pygame.event.clear()
    gameWindow.fill(BLACK)

    # Draws the exit and play again buttons
    restartButton = pygame.draw.rect(gameWindow, RCOLOUR, (270, 300, 280, 100), 4)
    exitButton = pygame.draw.rect(gameWindow, ECOLOUR, (310, 490, 200, 60), 4)

    # Endscreen Text
    restartText = menuFont.render("Play Again?", True, WHITE)
    exitText = menuFont.render("Exit", True, WHITE)
    gameWindow.blit(restartText, (282, 325))
    gameWindow.blit(exitText, (365, 495))

    # Draws icons depending on game mode ######################################
    if win:
        deathAnimation = False
        if level > 0:
            gameWindow.blit(trophy, (315, 30))
        if level == ENDLESS:
            gameWindow.blit(clock[int(clockNum)], (315, 30))

    # You lost :(
    else:
        gameWindow.blit(icon, (270, 0))

    # ----------------------------------------------------------------------- #

    # Button changes color on hover ###########################################

    if restartButton.collidepoint(mousePosition):
        # changes colour to grey on hover
        RCOLOUR = LGREY

    if not restartButton.collidepoint(mousePosition):
        RCOLOUR = WHITE

    # ----------------------------------------------------------------------- #

    # Resets if restart is pressed ############################################
    if restartButton.collidepoint(mousePosition) and mouseClicked:
        # Stops sounds
        nextLevelSound.stop()
        lose.stop()

        # Sets level if endless mode is on
        if endless:
            level = ENDLESS
        else:
            level = 1

        # Displaying level if adventure mode, displays "Endless Mode" is endless mode is on
        if not endless:
            displayLevel(level)
        elif endless:
            displayLevel(0, endlessMode=True)
        inPlay = True
        deathAnimation = False
        win = False

    # ----------------------------------------------------------------------- #

    # Button changes color on hover ###########################################
    if exitButton.collidepoint(mousePosition):
        # changes colour to grey on hover
        ECOLOUR = LGREY

    if not exitButton.collidepoint(mousePosition):
        ECOLOUR = WHITE

    # ----------------------------------------------------------------------- #

    # Resets if restart is pressed ############################################
    if exitButton.collidepoint(mousePosition) and mouseClicked:
        endScreen = False
        restart = False

    # ----------------------------------------------------------------------- #

    # Checks ESC and QUIT buttons
    checkQuit()

    clockNum += 0.005
    if clockNum >= len(clock):
        clockNum = 0


    # Updating Screen
    pygame.display.update()


def drawDeathAnimation() -> None:
    """
    Redraws the game window when called. Draws the snake segments,
    grid, apples and obstacles

    Return => None
    """
    global appleGenerated, lastApple, timeLeft, applesNeeded, stopwatch, inPlay, win, flipSegmentColour, deathAnimation, deathAnimationTime, deathAnimationStopwatch, rateOfDeathAnimation, endScreen
    TIME_COLOUR = WHITE
    BLOCK_R = 72
    BLOCK_G = 0
    BLOCK_B = 255

    pygame.event.clear()

    gameWindow.fill(BLACK)

    # Turns the timer colour to red if there is less than 10 seconds
    if timeLeft <= 20:
        if round(timeLeft) % 2 == 0:
            TIME_COLOUR = SCORE_RED
        else:
            TIME_COLOUR = WHITE

    # Draws the grid ##########################################################
    for j in range(round(BLOCK_X)):
        for k in range(round(BLOCK_Y)):
            if j % 2 == 0 and k % 2 == 0:
                pygame.draw.rect(gameWindow, GREY, (j * BLOCK_SIZE, k * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for j in range(round(BLOCK_X)):
        for k in range(round(BLOCK_Y)):
            if j % 2 == 1 and k % 2 == 1:
                pygame.draw.rect(gameWindow, GREY, (j * BLOCK_SIZE, k * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # ----------------------------------------------------------------------- #

    # Draws the obstacles #####################################################
    for j in range(len(obstaclesX)):
        obsCoordX = obstaclesX[j]
        obsCoordY = obstaclesY[j]
        pygame.draw.rect(gameWindow, ORANGE, (obsCoordX * BLOCK_SIZE, obsCoordY * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                         0, ROUNDEDNESS_OBS)

    # ----------------------------------------------------------------------- #

    # Draws the snake segments ################################################
    for j in range(len(blocksX)):
        SEG_COLOUR = (BLOCK_R, BLOCK_G, BLOCK_B)
        coord_x = blocksX[j]
        coord_y = blocksY[j]

        pygame.draw.rect(gameWindow, SEG_COLOUR, (coord_x * BLOCK_SIZE, coord_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                         0, ROUNDEDNESS)

        # Changes the color to make a gradient
        if BLOCK_R + 20 <= 255 and not flipSegmentColour:
            BLOCK_R += 10

        elif BLOCK_R + 20 > 255:
            flipSegmentColour = True

        if BLOCK_G + 20 <= 255 and not flipSegmentColour:
            BLOCK_G += 10

        if BLOCK_R > 82 and flipSegmentColour:
            BLOCK_R -= 10

        elif BLOCK_R <= 82:
            flipSegmentColour = False

        if BLOCK_G - 20 >= 0 and flipSegmentColour:
            BLOCK_G -= 10

        # ----------------------------------------------------------------------- #

    # Draws the apples ########################################################
    for j in range(len(appleX)):
        apple_x = appleX[j]
        apple_y = appleY[j]
        pygame.draw.circle(gameWindow, RED,
                           (apple_x * BLOCK_SIZE + BLOCK_SIZE / 2, apple_y * BLOCK_SIZE + BLOCK_SIZE / 2),
                           BLOCK_SIZE / 2)
        pygame.draw.circle(gameWindow, DRED,
                           (apple_x * BLOCK_SIZE + BLOCK_SIZE / 2, apple_y * BLOCK_SIZE + BLOCK_SIZE / 2),
                           BLOCK_SIZE / 2, 2)

    # ----------------------------------------------------------------------- #

    # Setting the score for endless/adventure #################################
    if level > 0 and not win:
        # Renders the font, depending on the game mode
        scoreRender = scoreFont.render(f"{score}/{applesNeeded}", True, WHITE)
        gameWindow.blit(scoreRender, (WIDTH - 70, 10))

    elif level == ENDLESS and not win:
        # Renders the font, depending on the game mode
        leadZero = "0" if score < 10 else ""
        scoreRender = scoreFont.render(f"{leadZero}{score}", True, WHITE)
        gameWindow.blit(scoreRender, (WIDTH - 50, 10))

    # ----------------------------------------------------------------------- #

    # Setting clock to timer/stopwatch for endless/adventure ##################
    if level >= 0 and not win:
        displayTime(timeLeft, 10, 10, TIME_COLOUR)

    elif level == ENDLESS and not win:

        displayTime(stopwatch, 10, 10, TIME_COLOUR)

    # ----------------------------------------------------------------------- #

    if deathAnimation:
        # Accumulating time
        time = fpsClock.tick(FPS)
        deathAnimationStopwatch += time / 1000  # "rate of death"
        deathAnimationTime += time / 1000  # actual - to speed up death after the sound effect ends

        # stops the music
        pygame.mixer.music.stop()

        # if space is pressed, skip through the animation
        if keys[pygame.K_SPACE]:
            deathAnimation = False
            inPlay = False
            endScreen = True

        # when the sound effect ends, speed up the death animation
        if deathAnimationTime > 2.8:
            rateOfDeathAnimation = 2

        if int(deathAnimationStopwatch) % rateOfDeathAnimation == 0:
            # if there are elements, pop them
            if len(blocksX) >= 1:
                blocksX.pop(0)
                blocksY.pop(0)
            # end the animation if there are no more elements
            else:
                pygame.time.delay(300)
                deathAnimation = False
                inPlay = False
        deathAnimationStopwatch += 1

    if win:
        deathAnimation = False
    # Updating screen
    pygame.display.update()


def checkCollision() -> bool:
    """
    Checks:
        a) If the snake has hit the walls
        b) If the snake has hit itself
        c) If the snake has hit an obstacle
    and returns True if any have been hit, and False otherwise

    Return => bool
    """
    # The snake has hit the walls #############################################
    if blocksX[0] < 0 or blocksX[0] + 1 > BLOCK_X:
        lose.play()
        return True

    if blocksY[0] < 0 or blocksY[0] + 1 > BLOCK_Y:
        lose.play()
        return True
    # ----------------------------------------------------------------------- #

    # The snake head has hit itself ###########################################
    for j in range(len(blocksX) - 1):
        coord_x = blocksX[j + 1]
        coord_y = blocksY[j + 1]
        if blocksX[0] == coord_x and blocksY[0] == coord_y:
            lose.play()
            return True

    # ----------------------------------------------------------------------- #

    # The snake has hit an obstacle ###########################################
    for j in range(len(obstaclesX)):
        coord_x = obstaclesX[j]
        coord_y = obstaclesY[j]
        if blocksX[0] == coord_x and blocksY[0] == coord_y:
            lose.play()
            return True

    # ----------------------------------------------------------------------- #

    # Nothing has been hit
    return False


def generateApple() -> None:
    """
    Generates an apple that isn't in the snake body or an obstacles.
    Uses the generateAppleCheck(apple_x, apple_y) function to aid in doing this.

    Return => None
    """
    # Initializes the apple_x and apple_y variables
    apple_x = randint(0, BLOCK_X - 1)
    apple_y = randint(0, BLOCK_Y - 1)

    # Keeps generating until apple isn't in an obstacle or a snake or in another apple
    while not generateAppleCheck(apple_x, apple_y):
        apple_x = randint(0, BLOCK_X - 1)
        apple_y = randint(0, BLOCK_Y - 1)

    # If the apple's coordinates are valid, append them to the lists
    appleX.append(apple_x)
    appleY.append(apple_y)


def generateAppleCheck(apple_x: int, apple_y: int) -> bool:
    """
    Checks if the apple is in the snake or in an obstacles, returning True if it is
    and False otherwise.

    Parameters:
        apple_x -> the x coordinate of the attempted generated apple.
        apple_y -> the y coordinate of the attempted generated apple.

    Return => bool
    """
    # Checks if the apple is in the snake
    for j in range(len(blocksX)):
        if apple_x == blocksX[j] and apple_y == blocksY[j]:
            return False

    # Checks if the apple is in the obstacle
    for j in range(len(obstaclesX)):
        if apple_x == obstaclesX[j] and apple_y == obstaclesY[j]:
            return False

    # The apple's coordinates are valid
    return True


def checkApple() -> bool:
    """
    Checks if the head of the snake is in an apple, and deletes the apple if so.
    Also is responsible for generating a new apple if there are none

    Return => bool
    """
    global appleX, appleY, appleGenerated, lastApple
    # getting the coordinates of the head
    coord_x = blocksX[0]
    coord_y = blocksY[0]

    # Iterating through the apple coordinate lists
    if coord_x in appleX and coord_y in appleY:
        for j in range(len(appleX) - 1, -1, -1):  # Goes backward as to not cause an IndexError: "index out of range"
            if appleX[j] == coord_x and appleY[j] == coord_y:
                del appleX[j]
                del appleY[j]

        # If there are no apples, generated one
        if len(appleX) == 0:
            appleGenerated = False
            lastApple = 0
        appleEat.play()
        return True

    # Apple not eaten
    return False


def displayTime(time: float, x: int, y: int, colour: tuple[int, int, int]) -> None:
    """
    Displays the time at a certain x and y with a certain colour

    Parameters:
        time -> the time to display.
        x -> the x coordinate of the displayed time.
        y -> the y coordinate of the displayed time.
        colour -> the colour of the time displayed

    Return => None
    """
    strTime = round(time)
    # Adds leading zero if the seconds is less than 10
    leadingZero = 0 if strTime % 60 < 10 else ""
    # Displaying time with minutes and seconds
    if strTime >= 60:
        timeToDisplay = f"{int(strTime // 60)}:{leadingZero}{round(strTime % 60, 1)}"
    else:
        timeToDisplay = f"{round(strTime % 60, 1)}"

    stopwatchRender = scoreFont.render(f"{timeToDisplay}", True, colour)
    gameWindow.blit(stopwatchRender, (x, y))


def checkScore() -> None:
    """
    Checks the score and reduces the delay depending on the score,
    effectively speeding up the game

    Return => None
    """
    global score, delay
    if score % 3 == 0:
        speedMultiplier = score // 3
        newDelay = delay - speedMultiplier
        if newDelay <= 30:
            newDelay = 30
        delay = newDelay


def checkWin() -> None:
    """
    Checks if the length of the snake is equal to the area of the screen(endless mode),
    or if the max level has been exceeded. In both theses scenarios,
    the player has won and the game will end.

    Return => None
    """
    global score, inPlay, win, level
    if len(blocksX) >= BLOCK_X * BLOCK_Y or level > 10:
        nextLevelSound.stop()  # stops sound to prevent overlap
        nextLevelSound.play()
        win = True
        inPlay = False
        if level > 0:  # the icon displayed for win depends on the level: if its > 0 or ENDLESS
            level = 1  # sets level to 1 after win in adventure mode


def generateCheckLevel(obs_x: int, obs_y: int) -> bool:
    """
    Checks if the obstacle is directly in front of the snake and returns true if so

    Parameters:
        obs_x -> the x coordinate of the obstacle
        obs_y -> the y coordinate of the obstacle

    Return => bool
    """
    # Prevents obstacles from being spawned directly in front of the snake head
    for j in range(int(BLOCK_Y // 5)):
        if obs_x == BLOCK_X // 2 and obs_y == BLOCK_Y // 2 + 1:
            return False

    # Prevents obstacles from being spawned in the snake
    for j in range(int(INITIAL_SEGMENTS)):
        if obs_x == BLOCK_X // 2 and obs_y == BLOCK_Y // 2 - j:
            return False

    return True


def checkLevel(goal: int, timer: int) -> None:
    """

    Parameters:
        goal -> the amount of apples needed to go to the next level.
        timer -> the time left on the clock

    Return => None
    """
    global score, level, inPlay, nextLevel, delay
    # If you reach the goal before hit runs out
    if score >= goal and timer > 0:
        # increments the level and tells the program to start the next level
        level += 1
        inPlay = False
        nextLevel = True

        # Sets the obstacles and speed for level 2 ############################
        if level == 2:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 184)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 60

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 3 ############################
        elif level == 3:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 144)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 55

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 4 ############################
        elif level == 4:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 112)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 52

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 5 ############################
        elif level == 5:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 96)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 50

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 6 ############################
        elif level == 6:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 64)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 48

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 7 ############################
        elif level == 7:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 52)):
                obstacle_x = randint(4, BLOCK_X - 4)
                obstacle_y = randint(4, BLOCK_Y - 4)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 4)
                    obstacle_y = randint(4, BLOCK_Y - 4)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 48

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 8 ############################
        elif level == 8:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 44)):
                obstacle_x = randint(4, BLOCK_X - 3)
                obstacle_y = randint(4, BLOCK_Y - 3)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 3)
                    obstacle_y = randint(4, BLOCK_Y - 3)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 48

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 9 ############################
        elif level == 9:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 36)):
                obstacle_x = randint(4, BLOCK_X - 3)
                obstacle_y = randint(4, BLOCK_Y - 3)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 3)
                    obstacle_y = randint(4, BLOCK_Y - 3)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 46

        # ------------------------------------------------------------------- #

        # Sets the obstacles and speed for level 10 ############################
        elif level == 10:
            # Clearing previous obstacles
            obstaclesX.clear()
            obstaclesY.clear()

            # Generating obstacles depending on the level
            for j in range(int(BLOCK_X * BLOCK_Y // 32)):
                obstacle_x = randint(4, BLOCK_X - 2)
                obstacle_y = randint(4, BLOCK_Y - 2)

                # Makes sure the obstacles aren't directly in front of the snake
                while not generateCheckLevel(obstacle_x, obstacle_y):
                    obstacle_x = randint(4, BLOCK_X - 2)
                    obstacle_y = randint(4, BLOCK_Y - 2)
                obstaclesX.append(obstacle_x)
                obstaclesY.append(obstacle_y)

            # Setting the delay/speed
            delay = 45

        # ------------------------------------------------------------------- #


def checkLevelParams() -> None:
    """
    Sets the appropriate goal and time left for each level
    A lot of if/elifs :(
    I wish there were switch-case statements

    Return => None
    """
    global level, timeLeft, applesNeeded, win
    # Sets the goal and time for level 1 ######################################
    if level == 1:
        timeLeft = 180
        applesNeeded = 8


    # Sets the goal and time for level 2 ######################################
    elif level == 2:
        timeLeft = 180
        applesNeeded = 10


    # Sets the goal and time for level 3 ######################################
    elif level == 3:
        timeLeft = 170
        applesNeeded = 10


    # Sets the goal and time for level 4 ######################################
    elif level == 4:
        timeLeft = 160
        applesNeeded = 10


    # Sets the goal and time for level 5 ######################################
    elif level == 5:
        timeLeft = 150
        applesNeeded = 10


    # Sets the goal and time for level 6 ######################################
    elif level == 6:
        timeLeft = 140
        applesNeeded = 12


    # Sets the goal and time for level 7 ######################################
    elif level == 7:
        timeLeft = 130
        applesNeeded = 12


    # Sets the goal and time for level 8 ######################################
    elif level == 8:
        timeLeft = 125
        applesNeeded = 14


    # Sets the goal and time for level 9 ######################################
    elif level == 9:
        timeLeft = 120
        applesNeeded = 14


    # Sets the goal and time for level 10 #####################################
    elif level == 10:
        timeLeft = 100
        applesNeeded = 16


    # The player has won the game  ############################################
    elif level > 10:
        timeLeft = 0
        applesNeeded = 0
        win = True
        nextLevelSound.stop()


def displayLevel(levelToDisplay: int, endlessMode: bool = False) -> None:
    """
    Displays the level or "Endless Mode" if endless mode is on

    Parameters:
        levelToDisplay -> Displays the level before it commences
        endlessMode -> If true, it will just display "Endless Mode" instead of the level

    Return => None
    """
    gameWindow.fill(BLACK)

    # Changes the text depending on the game mode
    levelText = menuFont.render(f"Level {levelToDisplay}", True, WHITE)
    if endlessMode:
        levelText = menuFont.render(f"Endless Mode", True, WHITE)

    # Blits the text in different places depending on game mode
    if not endlessMode:
        gameWindow.blit(levelText, (330, 260))
    else:
        gameWindow.blit(levelText, (260, 260))

    nextLevelSound.play()  # Plays sound

    pygame.display.update()  # Updates

    pygame.time.delay(1200)


def checkQuit():
    global inPlay, restart, permaExit, menu, restart, deathAnimation, endScreen

    # ESC key and QUIT button
    if keys[pygame.K_ESCAPE]:
        inPlay = False
        restart = False
        permaExit = True
        menu = False
        restart = False
        deathAnimation = False
        endScreen = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
            restart = False
            permaExit = True
            menu = False
            restart = False
            deathAnimation = False
            endScreen = False


###############################################################################
#
# Main Program
#
###############################################################################


# System Variables # DO NOT TOUCH
appleGenerated = False
inPlay = True
menu = True
restart = True
permaExit = False
endScreen = False
nextLevel = False
endless = False
win = False
flipSegmentColour = False
deathAnimation = False

# --------------------------------------------------- #
#
# Game Mode Menu
#
# --------------------------------------------------- #

# starts the music
pygame.mixer.music.play(-1)

while inPlay:

    pygame.event.clear()

    if menu:
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed(3)[0]
        keys = pygame.key.get_pressed()

        # Draws the menu with the mouse position and buttons as arguments
        drawTypeMenu(mousePos, clicked)

        # ESC key and QUIT button
        checkQuit()

# If ESC or QUIT was pressed, we do not run the rest of the code
if not permaExit:
    inPlay = True

# Allows next menu to run
menu = True

# Delay
pygame.time.delay(400)

# --------------------------------------------------- #
#
# Grid Size Menu
#
# --------------------------------------------------- #
while inPlay:

    pygame.event.clear()

    # ESC key and QUIT button
    checkQuit()

    if menu:
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed(3)[0]
        keys = pygame.key.get_pressed()

        # Draws the menu with the mouse position and buttons as arguments
        drawMenu(mousePos, clicked)

# If ESC or QUIT was pressed, we do not run the rest of the code
if not permaExit:
    inPlay = True

# Sets the level to ENDLESS(-1) if endless mode is on
if endless:
    level = ENDLESS

pygame.time.delay(400)

# Setting the BLOCK_X and BLOCK_Y for the new grid size
BLOCK_X = WIDTH // BLOCK_SIZE
BLOCK_Y = HEIGHT // BLOCK_SIZE

# pausing music for level display
pygame.mixer.music.pause()

# Displaying level if adventure mode, displays "Endless Mode" is endless mode is on
if not endless and restart:
    displayLevel(level)

elif endless and restart:
    displayLevel(0, endlessMode=True)


while restart:
    # reset time and clock
    fpsClock = pygame.time.Clock()
    pygame.mixer.music.play(-1)

    # Checks the level and sets the parameters
    checkLevelParams()

    # add coordinates for the head and 3 segments
    if inPlay:  # we don't want to add segments just to clear them later
        for i in range(INITIAL_SEGMENTS):
            blocksX.append(BLOCK_X // 2)
            blocksY.append(BLOCK_Y // 2 + i)

    # --------------------------------------------------- #
    #
    # Game loop
    #
    # --------------------------------------------------- #
    while inPlay:

        pygame.event.clear()

        # Redraws the game window
        redrawGameWindow()

        # Checks if the player has won
        checkWin()

        # Sets the level parameters if adventure mode is on
        if not endless:
            checkLevel(applesNeeded, timeLeft)

        # Sets the speed
        pygame.time.delay(delay)

        # Gets all keys
        keys = pygame.key.get_pressed()

        # Checks ESC and QUIT key
        checkQuit()

        # Mapping directions to keys
        if keys[pygame.K_LEFT] and DIRECTION != 3:
            MOVE_Q.append(LEFT)
        elif keys[pygame.K_RIGHT] and DIRECTION != 2:
            MOVE_Q.append(RIGHT)
        elif keys[pygame.K_UP] and DIRECTION != 1:
            MOVE_Q.append(UP)
        elif keys[pygame.K_DOWN] and DIRECTION != 0:
            MOVE_Q.append(DOWN)

        # pops the first element in the movement queue if there is an element
        if MOVE_Q:  # Easier way to check if a lists is empty or not
            DIRECTION = MOVE_Q.pop(0)

        # Mapping directions to stepX and stepY increments
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

        # Checks if the snake has eaten an apple
        if checkApple():

            # Checks the score to decreases speed if it is necessary
            checkScore()

            # If the snake is only the head, add the new element in the opposite direction
            if len(blocksX) <= 1:
                # Appending to blocks list
                blocksX.append(blocksX[-1] - stepX)
                blocksY.append(blocksY[-1] - stepY)

            # If there is more than 1 element, add a new one depending on the position of the last 2 elements
            else:
                change_X = blocksX[-1] - blocksX[-2]
                change_Y = blocksY[-1] - blocksY[-2]

                # Appending to blocks list
                blocksX.append(blocksX[-1] + change_X)
                blocksY.append(blocksY[-1] + change_Y)

            # Incrementing score when apple eaten
            score += 1

        # Moving the snake ####################################################
        # Goes backwards through the blocks list
        # Each segment takes the position of the one in front of it
        for i in range(len(blocksX) - 1, 0, -1):
            blocksX[i] = blocksX[i - 1]
            blocksY[i] = blocksY[i - 1]

            change_X = blocksX[-1] - blocksX[-2]
            change_Y = blocksY[-1] - blocksY[-2]

        # Moves the head of the snake
        blocksX[0] += stepX
        blocksY[0] += stepY

        # ------------------------------------------------------------------- #

        # Check for collision #################################
        if checkCollision():
            deathAnimation = False if win else True
            inPlay = False

            # Sets logging string
            gameLogString = ""
            if level > 0:
                gameLogString = f"ADVENTURE @ {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')} [ Level {level} | {score}/{applesNeeded} Apples ]"
            else:
                gameLogString = f"ENDLESS @ {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')} [ Time : {round(stopwatch, 2)} | Score: {score} ] "

            # Adds game to the game log
            games.append(gameLogString)

        # --------------------------------------------------- #

        # Checks for time; ends if time runs out
        if timeLeft < 0:
            inPlay = False

    # If ESC or QUIT was pressed, we do not run the rest of the code
    if not permaExit:
        endScreen = True

    while deathAnimation:
        keys = pygame.key.get_pressed()
        drawDeathAnimation()
        checkQuit()

    # Resetting game ##########################################################
    # clears the blocks
    blocksX.clear()
    blocksY.clear()

    # clears the apples
    appleX.clear()
    appleY.clear()

    # Resets score, movement queue, direction and more
    score = 0
    MOVE_Q.clear()
    DIRECTION = UP
    appleGenerated = False
    lastApple = 0

    # death animation reset
    # death animation time - speeds up the death animation after the sound effect ends
    deathAnimationTime = 0

    # death stopwatch time - to control the rate at which the snake "dies"
    deathAnimationStopwatch = 0

    rateOfDeathAnimation = rateOfDeathAnimationInit

    # ----------------------------------------------------------------------- #

    # Resetting for next level and setting values #############################
    pygame.mixer.music.pause()
    if nextLevel:
        if level <= 10:
            displayLevel(level)
            pygame.mixer.music.play(-1)
        inPlay = True
        endScreen = False
        nextLevel = False

    # Endscreen - You lose or win the game ####################################
    if endScreen:
        # resets level to 1 if adventure mode and the player has not won
        if not endless:
            level = 1

        # Clears obstacles - MIGHT NOT BE NEEDED, TEST LATER
        obstaclesX.clear()
        obstaclesY.clear()

        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed(3)[0]

        drawEndMenu(mousePos, clicked)

# ---------------------------------------#

# Stores logs in txt file
with open("logs.txt", 'a', 1) as log:
    for game in games:
        log.write(game + "\n")

with open("logs.txt", 'r', 1) as log:
    print(log.read())

pygame.quit()
