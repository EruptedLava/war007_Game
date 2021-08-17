import pygame
import time
import random
import math
from pygame import mixer


# initialising pygame
pygame.init()

# setting window size
gamewindow = pygame.display.set_mode((1000,600))

#setting window title
pygame.display.set_caption("Lava Game")
running = True

# Background image
background = pygame.image.load("background1.jpg")

# Background Sounds
mixer.music.load("background1.wav")
mixer.music.play(-1)

# setting up game logo
logo = pygame.image.load("hacker.png")
pygame.display.set_icon(logo)

# Some variables related to players
playerimg = pygame.image.load("jet.png")
playerX = 500
playerY = 480
X_Change = 0

enemyimg = []
enemyX = []
enemyY = []
eX_Change = []
eY_Change = []

no_of_enemys = 6
# Enemy
for i in range(no_of_enemys):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    eX_Change.append(0.5)
    eY_Change.append(40)


# Bullet
''''Ready state means we can't see the bullet '''
bulletimg = pygame.image.load("bullet1.png")
bulletX = 0
bulletY = 480
bX_Change = 0
bY_Change = 2
bullet_state = "ready"

# Scoreboard
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

game_over = pygame.font.Font('freesansbold.ttf',75)

def show_scoreboard(x,y):
    score = font.render("Score : "+str(score_value),True,(255,255,255))
    gamewindow.blit(score,(x,y))



def game_over_text():
    over = font.render("     GAME OVER    ",True,(255,255,255))
    gamewindow.blit(over,(350,300))


# Player Direction Controls
def player(x,y):
    gamewindow.blit(playerimg, (x,y))

def enemy(x,y):
    gamewindow.blit(enemyimg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    gamewindow.blit(bulletimg, (x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

# Main Game Loop
while running:
    gamewindow.fill((0,0,0))
    gamewindow.blit(background,(0,0))

    for i in range(no_of_enemys):

        # Game over
        if enemyY[i] >= 450:
            for _ in range(no_of_enemys):
                enemyY[_]=2000

            game_over_text()
            break


        enemyX[i]+= eX_Change[i]
        if enemyX[i]<=0:
            eX_Change[i] = 0.4
            enemyY[i]+= eY_Change[i]

        elif enemyX[i]>=950:
            eX_Change[i] = -0.4
            enemyY[i]+= eY_Change[i]


        colision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        #Colision state
        if colision:

            colision_sound = mixer.Sound("explosion.wav")
            colision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+= 1
            # print(score)
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i])


    playerX+= X_Change

    if playerX<=-50:
        playerX = 1000
    elif playerX>=1000:
        playerX = 0
   
    # For exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # print("KEY PRESSED")

            if event.key == pygame.K_LEFT:
                X_Change = -0.4
                # print("left key is pressed")
            if event.key == pygame.K_RIGHT:
                X_Change = 0.4
                # print("right key is pressed")

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_Change = 0
                # print("Key is being released")

    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bY_Change
    
    # colision = isCollision(enemyX, enemyY, bulletX, bulletY)

    # #Colision state
    # if colision:
    #     bulletY = 480
    #     bullet_state = "ready"
    #     score+= 1
    #     print(score)
    #     enemyX = random.randint(0,800)
    #     enemyY = random.randint(50,150)

    # enemy(enemyX, enemyY)
    show_scoreboard(textX,textY)
    player(playerX,playerY)
    pygame.display.update()
    