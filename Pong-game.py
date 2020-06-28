import pygame
from pygame.locals import *
import sys
import os
import random
pygame.init()
pygame.font.init()
SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
FPS_CLOCK = pygame.time.Clock()
sounds = {}
fps=70
white=(255,255,255)
black=(0,0,0)
green=(0,196,0)
red=(255,0,0)


def text_screen(text, color, x, y,font):# to write anything on the screen
    screen_text = font.render(text, True, color)
    SCREEN.blit(screen_text, [x, y])

def welcome():
    font = pygame.font.Font(myfontfile, 70)
    while True:
        SCREEN.fill(black)
        text_screen("Welcome to Pong",white,200,200,font)
        text_screen("Press Space Bar To Play", white, 140, 300,font)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE):
                instructions()
            pygame.display.update()

            FPS_CLOCK.tick(fps)
def instructions():
    font = pygame.font.Font(myfontfile, 40)
    while True:
        SCREEN.fill(black)
        
        text_screen("Instructions",white,300,100,font)
        text_screen("Press W to move up",green,50,200,font)
        text_screen("and S to move down",green,50,240,font)
        text_screen("Press up to move up",red,410,200,font)
        text_screen("and down to move down",red,410,240,font)
        text_screen("2 player",white,100,300,font)
        text_screen("Computer",white,400,300,font)
        text_screen("First player to reach 10 points wins the game",white,40,400,font)
        for event in pygame.event.get():
            pressed_key = pygame.key.get_pressed()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if 100+100>mouse[0]>100 and 300+40>mouse[1]>300:
                    maingame('2player')
                elif 400+110>mouse[0]>400 and 300+40>mouse[1]>300:
                    maingame('Computer') 
            pygame.display.update()

            FPS_CLOCK.tick(fps)
def gameover(winner):
    font = pygame.font.Font(myfontfile, 60)
    font2= pygame.font.Font(myfontfile, 50)
    while True:
        SCREEN.fill(black)
        text_screen("WINNER: "+winner,green,200,240,font)
        text_screen("Press space to start a new game",white,200,400,font2)
        for event in pygame.event.get():
            pressed_key = pygame.key.get_pressed()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE):
                welcome()
            pygame.display.update()

            FPS_CLOCK.tick(fps)
def maingame(type):
    rectx=6 #width of middle line
    recty=600 #height of middle line
    stick_x=6 #width of the sticks
    stick_y=170 # height of the sticks
    xpos1=0 # xcoordinate of the 1st stick
    ypos1=214 # ycoordinate of the 1st stick
    xpos2=790 # xcoordinate of the 2nd stick
    ypos2=214 # ycoordinate of the 2nd stick
    y1=0
    y2=0
    ball_x=400 #initial ball position
    ball_y=300
    ball_speed_x=8*random.choice([1,-1])
    ball_speed_y=8*random.choice([1,-1])
    flag1=False
    flag2=False
    score_1=0
    score_2=0
    score_1_color=green
    score_2_color=green
    winner="none"
    fps=70
    font = pygame.font.Font(myfontfile, 70)
    while True:
        if score_1==10 or score_2==10: # if anyone reacjes 10 points game finishes
            gameover(winner)
        else:
            SCREEN.fill(black)
            for event in pygame.event.get():
                pressed_key = pygame.key.get_pressed()
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type==KEYDOWN:
                    #move the sticks up and down
                    if type =="2player":
                        if pressed_key[pygame.K_DOWN]:
                            y2=10
                            flag2=True
                        elif pressed_key[pygame.K_UP]:
                            y2=-10
                            flag2=True
                        if pressed_key[pygame.K_w]:
                            y1=-10
                            flag1=True
                        elif pressed_key[pygame.K_s]:
                            y1=10
                            flag1=True
                    else:
                        if pressed_key[pygame.K_UP]:
                            y2=-10
                            flag2=True
                        elif pressed_key[pygame.K_DOWN]:
                            y2=10
                            flag2=True
                
                if event.type==KEYUP and (event.key==K_DOWN or event.key==K_UP):
                    flag2=False
                    y2=0
                if event.type==KEYUP and (event.key==K_w or event.key==K_s):
                    flag1=False
                    y1=0
                    
            if type=="Computer":
                if ball_y>(ypos1+3) and ball_y<(ypos1+165):
                    y1=0
                    flag1=False
                elif ball_y<ypos1:
                    y1=-10
                    flag1=True
                elif ball_y>(ypos1+170):
                    y1=10
                    flag1=True
            if flag1==True:#for ypos1
                if (ypos1+y1)<(SCREENHEIGHT-170) and (ypos1+y1)>=0:
                    ypos1+=y1
                elif (ypos1+y1)>=SCREENHEIGHT:
                    ypos1=SCREENHEIGHT
                elif (ypos1+y1)<0:
                    ypos1=0
                
            if flag2==True:#for ypos2
                if (ypos2+y2)<(SCREENHEIGHT-170) and (ypos2+y2)>=0:
                    ypos2+=y2
                elif (ypos2+y2)>=SCREENHEIGHT:
                    ypos2=SCREENHEIGHT
                elif (ypos2+y2)<0:
                    ypos2=0

            #make the ball move
            ball_x+=ball_speed_x 
            ball_y+=ball_speed_y

            #hit the balls
            if (ball_y+21)>=SCREENHEIGHT or ball_y<=0: #hit ball on up and down walls
                ball_speed_y*=-1
                sounds['wall_hit'].play()

            if ball_x>=(xpos2-6) and ball_y in [i for i in range(ypos2,ypos2+171)]: #hit ball in 2nd stick
                ball_speed_x*=-1
                sounds['paddle_hit'].play()
            elif (ball_x+21)>=SCREENWIDTH:# hit ball on the right wall and increase points of player 1
                ball_speed_x*=-1
                score_1+=1
                fps+=3
                sounds['wall_hit'].play()
                sounds['score'].play()
            
            if (ball_x)<=(xpos1) and ball_y in [i for i in range(ypos1,ypos1+172)]: #hit ball in 1st stick
                ball_speed_x*=-1
                sounds['paddle_hit'].play()
            elif (ball_x)<=0: # hit ball on the left wall and increase points of player 2
                ball_speed_x*=-1
                score_2+=1
                fps+=3
                sounds['wall_hit'].play()
                sounds['score'].play()

            #change colour of score and determine the winner
            if score_2>score_1:
                score_2_color=green
                score_1_color=red
                winner="Player 2"
            elif score_1>score_2:
                score_1_color=green
                score_2_color=red
                if type=="2player":
                    winner="Player 1"
                else:
                    winner="Computer"
            elif score_1==score_2:
                score_1_color=green
                score_2_color=green

            #show all the images on the screen
            text_screen(str(score_1),score_1_color,180,100,font)
            text_screen(str(score_2),score_2_color,580,100,font)
            pygame.draw.rect(SCREEN,white,[400,0,rectx,recty])
            pygame.draw.rect(SCREEN,white,[xpos1,ypos1,stick_x,stick_y])
            pygame.draw.rect(SCREEN,white,[xpos2,ypos2,stick_x,stick_y])
            pygame.draw.circle(SCREEN, green, (ball_x,ball_y), 15)
            pygame.display.update()
            FPS_CLOCK.tick(fps)
        
if __name__ == "__main__":
    pygame.mixer.init()
    pygame.init()
    pygame.display.set_caption("Pong by krishna")
    def resource_path(relative_path):
        try:
            base_path=sys._MEIPASS
        except Exception:
            base_path=os.path.abspath(".")
        return os.path.join(base_path,relative_path)
            
    #load sounds
    sounds['paddle_hit']=pygame.mixer.Sound(resource_path('data/paddle_hit.wav'))
    sounds['score']=pygame.mixer.Sound(resource_path('data/score.wav'))
    sounds['wall_hit']=pygame.mixer.Sound(resource_path('data/wall_hit.wav'))
    myfontfile=resource_path('data/myfont.ttf')
    welcome()
