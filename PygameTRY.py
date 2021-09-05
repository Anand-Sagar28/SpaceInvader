import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen(WIDTH , HEIGHT)
screen = pygame.display.set_mode((800, 600))

# Adding background image
background = pygame.image.load('Background.png')

# TITLE < LOGO
pygame.display.set_caption('Space Invader')  # Title
icon = pygame.image.load('ufo (1).png')  # Icon of the game
pygame.display.set_icon(icon)

# Adding background music
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 is added to make it run continously from start to stop

# Adding Player image
player_img = pygame.image.load('spaceship.png')
playerX = 370
playerY = 500
playerX_change = 0

# Adding Enemy randomly anywhere in the screen.
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(10, 200))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Adding bullet in the game.
# Ready  = Bullet is in not fired yet Cant see on screen.
# Fire = Bullet is moving
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    game_overfont = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_overfont, (200, 240))


def player(x, y):
    screen.blit(player_img, (x, y))  # This blit method is used to draw in the screen the image of player.


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


# Collision between enemy and bullet can be done using distance.
# same distance == collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game LOOP
running = True
while running:
    # Screen Should appear above everything..
    screen.fill((0, 0, 0))  # Changing Colors to RGB = (RED, GREEN, BLUE)
    # Background image
    screen.blit(background, (0, 0))
    # playerX += 0.3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change += -4
            if event.key == pygame.K_RIGHT:
                playerX_change += 4
                # print('Right Key is pressed')
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # getting the x coordinate of the bullet.
                    bulletX = playerX  # Assigning a fixed position for the origin of bullet from the spaceship.
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Assigning Movement of the player of pressing the left and right key
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # If collision then respawning the enemy in diff location and the score is increased by1 in each collision.
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 500
            bullet_state = 'ready'
            score_value += 1
            # print(score_value)
            # Respawning enemy in a random location after bullet hits the enemy.
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(10, 200)
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

        enemy(enemyX[i], enemyY[i], i)

    # Creating multiple bullets to hit
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # It Should be called inside while loop as for the game is running inside it.
    show_score(textX, textY)
    pygame.display.update()
