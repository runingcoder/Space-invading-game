import pygame
import sys
import random
import math
from pygame import mixer
# initializing pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('backg.jpg')

#background sound

mixer.music.load("background.wav")
mixer.music.play(-1)


# Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

def game_over():
    over_text= over_font.render("GAME OVER!!", True, (0, 0, 0) )


    screen.blit(over_text, (200,250))



def score_board(x,y):
    score=font.render("Score:" + str(score_value), True, (255, 255, 255) )
    screen.blit(score, (x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))  # surface of the game


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# enemy.
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
noe = 6
for i in range(noe):
    enemyImg.append(pygame.image.load('rs.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(30)

# player
playerImg = pygame.image.load('si.png')
playerX = 370
playerY = 540
playerX_change = 0
playerY_change = 0

#score
score_value=0
font=pygame.font.Font("dak.otf", 64)

textX=10
textY=10


#game over text

over_font=pygame.font.Font("dak.otf", 128)



# bullet
# ready= cant see the bullet in the screen
# fire= its currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))





def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


# Game loop
running = True
while running:


        screen.fill((10, 24, 45))
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # RGB Values in screen.fill(r,g,b)
            # control the keyboard strokes being left or right
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_LEFT:
                    playerX_change = -2

                if event.key == pygame.K_RIGHT:
                    playerX_change = +2
                if event.key == pygame.K_UP:
                    playerY_change = -2

                if event.key == pygame.K_DOWN:
                    playerY_change = +2
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        pygame.mixer.music.load('laser.wav')
                        pygame.mixer.music.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change
        # player boundary
        if playerX < 0:
            playerX = 0
        if playerY < 0:
            playerY = 0
        if playerX > 720:
            playerX = 720
        if playerY > 520:
            playerY = 520
        # enemy boundary

        for i in range(noe):

            #game over
            if enemyY[i] > 440:
                for j in range(noe):
                    enemyY[j]=2000
                game_over()

                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] < 0:

                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] > 720:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]




        # collision detection
            collision = iscollision(enemyX [i], enemyY[i], bulletX, bulletY)
            if collision:
                collision_sound = mixer.Sound("explosion.wav")
                collision_sound.play()

                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 750)
                enemyY[i] = random.randint(50, 150)





            enemy(enemyX[i], enemyY[i], i)

            # bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        score_board(textX, textY)
        pygame.display.update()
