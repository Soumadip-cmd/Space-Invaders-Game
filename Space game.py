import pygame
import random
import math
from pygame import mixer

pygame.init()
win = pygame.display.set_mode((900, 700))
pygame.display.set_caption('Space inverters')

# background img
bgimg = pygame.image.load('space bg.png')
#background Music
mixer.music.load('bg music.mp3')
mixer.music.play(-1)

#create icon
icon = pygame.image.load('spaceship (1).png')
pygame.display.set_icon(icon)

#create player image:
playerimg = pygame.image.load(
    "arcade-game.png")
player_x = 420
player_y = 600
playerx_change = 0


def player(x, y):
    win.blit(playerimg, (x, y))


#create enemy image:
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies=6

for i in range(num_enemies):
    enemyimg.append(pygame.image.load('alien (1).png'))
    enemyX.append(random.randint(0, (900-64))) 
    enemyY.append(random.randint(50,150))#that's mean (0,0) start from top left side but enemyY_change=45 so (0,45) and so on..
    enemyX_change.append(7)  # must imp ------{enemyX_change>0}
    enemyY_change.append(45)

def enemy(X, Y,i):
    win.blit(enemyimg[i], (X, Y))


#create Bullet image:
#ready ---> bullet image is not shown in pygame desktop
#fire ----> bullet is fired by player() and shown is by desktop

bulletimg = pygame.image.load('bullets.png')
bulletimg2 = pygame.transform.rotate(bulletimg, 90)
bulletX = 0
bulletY = 600  #for playerY=600
bulletX_change = 0
bulletY_change = 10  # bullet speed means 600 theke 40 kore komle speed besi hbei so bulletY_change=10
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(
        bulletimg2, (x + 15, y)
    )  # According to my player (x+20),(Y) is proper position to shoot bullet
    
#collison statement:
score=0

def collison(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
    if distance<27: #for bullet pixel 34 27 is appropriate...
        return True
    else:
        return False
    
#messAges:[Score :]
def score1(score):
    fonts=pygame.font.SysFont('Comic Sans MS',50)
    message=fonts.render('Score: '+str(score),True,(102,0,0))
    win.blit(message,(680,0))
    pygame.display.update()
    
def gameover():
    # win.fill((0,0,0))
    largefonts=pygame.font.SysFont('Bradley Hand ITC',80)
    mssg=largefonts.render('Game Over',True,(255,255,255))
    win.blit(mssg,(200,350))
    

run = True
while run:

    win.blit(bgimg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -6

            if event.key == pygame.K_RIGHT:
                playerx_change = 6

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletsound= mixer.Sound('shooting.wav')
                    bulletsound.play()
                    bulletX = player_x
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    #player movement:
    player_x += playerx_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= (900 - 64):  #64 pix img
        player_x = 900 - 64

    #enemy movement
    for i in  range(num_enemies):
        #game over
        if enemyY[i]>=570: # for player_y=600 and thats why 600-30 is perfect to game over its not dependent you have to see this from img and make a decision
            for j in range(num_enemies):
                enemyY[j]=2000
            gameover()
            break
        
        #enemy add
        enemyX[i]+= enemyX_change[i]
        
        if enemyX[i]<= 0:
            enemyX_change[i]= 7  #[-x](0)_________[+x](900)
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i]>= 900 - 64:
            enemyX_change[i]= -7  #[+x](900)_________[-x](0)
            enemyY[i]+= enemyY_change[i]

        
        #collison:
        collison1=collison(enemyX[i],enemyY[i],bulletX,bulletY)
        if collison1:
            bulletY=600 #reset the bullet when collison takes place
            bullet_state="ready" #and state is ready
            explosion_sound=mixer.Sound('explosion sound.wav')
            explosion_sound.play()
            score+=1
            
            enemyX[i] = random.randint(0, 836) #just for safety for errorless 900-64
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i], enemyY[i],i)


    #bullet Movement:
    if bulletY <= 0:
        bulletY = 600  #for player_y=600
        bullet_state = "ready"
    if bullet_state == "fire":
        bulletX = player_x
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    
        
    player(player_x, player_y)
    score1(score)
    
    pygame.display.update()

#-------------------------TOTAL CODE {1} -----------------------
