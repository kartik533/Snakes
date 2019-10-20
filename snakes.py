import pygame
import time
import random
import os
import pymysql

pygame.init()

db=pymysql.connect("localhost","anirudh","ani123","game")
cursor=db.cursor()
sql2="INSERT INTO Snakes(Score)VALUES('%d')" %(0)
cursor.execute(sql2)
db.commit()

#sql="""CREATE TABLE Snakes(Score INT)ENGINE=InnoDB"""
#cursor.execute(sql)

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

green = (34,177,76)
light_green = (0,255,0)

display_width = 800
display_height  = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

icon = pygame.image.load('apple2.png')
pygame.display.set_icon(icon)

img = pygame.image.load('head.png')
appleimg = pygame.image.load('apple2.png')

clock = pygame.time.Clock()
click = pygame.mouse.get_pressed()

AppleThickness = 30
block_size = 20
FPS = 15

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          size="large")

        message_to_screen("Press C to continue or Q to quit.",
                          black,
                          25)
        pygame.display.update()
        clock.tick(5)
                    

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))
    randAppleY = round(random.randrange(0, display_height-AppleThickness))

    return randAppleX,randAppleY


def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "menu":
                pygame.quit()
                os.system('python project.py')
                quit()
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                game_controls()

            if action == "play":
                gameLoop()

            if action == "intro":
                game_intro()
            
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))
    text_to_button(text,black,x,y,width,height)




def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
   
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)

        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)

        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)

        button("Play", 50,500,100,50, green, light_green, action="play")
        button("Controls", 250,500,100,50, yellow, light_yellow, action="controls")
        button("Quit", 450,500,100,50, red, light_red, action ="quit")
        button("Menu", 650,500,100,50, red, light_red, action ="menu")
    
        pygame.display.update()
        clock.tick(15)
        
        
def game_controls():

    cont = True

    while cont:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    cont = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if click[0] == 1 and action != None:
                if action == "quit":
                    pygame.quit()
                    quit()

                if action == "play":
                    cont = False
                    gameLoop()

                if action == "intro":
                    cont = False
                    game_intro()
   
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("Go Left : LEFT ARROW",
                          black,
                          -30)

        message_to_screen("Go Up : UP ARROW ",
                          black,
                          10)

        message_to_screen("Go Right : RIGHT ARROW ",
                          black,
                          50)
        message_to_screen("Go Down : DOWN ARROW ",
                          black,
                          90)
        button("Play", 50,500,100,50, green, light_green, action="play")
        button("Back", 250,500,100,50, yellow, light_yellow, action="intro")
        button("Quit", 450,500,100,50, red, light_red, action ="quit")
        button("Menu", 650,500,100,50, red, light_red, action ="menu")
    
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakelist):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)

    if direction == "left":
        head = pygame.transform.rotate(img, 90)

    if direction == "up":
        head = img

    if direction == "down":
        head = pygame.transform.rotate(img, 180)
        
    
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    
    return textSurface, textSurface.get_rect()
    
    
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    global direction

    direction = 'right'
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX,randAppleY = randAppleGen()
    
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            sql1="SELECT Score FROM Snakes ORDER BY Score DESC"
            cursor.execute(sql1)
            last=cursor.fetchone()
            message_to_screen("Your High Score: " + str(last),red,y_displace=-90,size="medium")
            message_to_screen("Your New Score: "+str(snakeLength-1),
                              red,
                              y_displace=-30,
                              size="medium")
            sql4="INSERT INTO Snakes(Score)VALUES('%d')" %(snakeLength-1)

            cursor.execute(sql4)
            db.commit()            
            button("Play", 150,500,100,50, green, light_green, action="play")
            button("Quit", 350,500,100,50, red, light_red, action ="quit")
            button("Menu", 550,500,100,50, red, light_red, action ="menu")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0

                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
      

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.fill(white)

        
        
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))


        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        
        snake(block_size, snakeList)

        score(snakeLength-1)

        
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:

                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:

                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)
        
    pygame.quit()
    quit()

game_intro()
gameLoop()
db.close()