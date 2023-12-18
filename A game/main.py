import pygame
import random
import math

from pygame import mixer

pygame.init()
# window configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load("bg_800x600.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # loops the music through out the game

# Title and Icon
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load("ufo.png")

pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load("arcade-game.png")
# coordinates
playerX = 369
playerY = 520
playerX_change = 0

# ENEMY
enemyImg = []
# coordinates
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))

    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# BULLET
# Ready - you can't see the bullet
# Fire - the bullet is moving(is in motion)
bulletImg = pygame.image.load("bullet.png")
# coordinates
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.2
bullet_state = "Ready"


def player(x, y):
    screen.blit(playerImg, (x, y))  # func draws the player on the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # func draws the enemy on the screen


def fire_bullet(x, y):
    global bullet_state  # creating the global variable so the state can be accessed from within the func
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # try removing the 16 and 10 values


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyY - bulletY), 2) + math.pow((enemyX - bulletX), 2))
    if distance < 27:
        return True
    return False


def game_over_text():
    text = over_text.render("GAME OVER", True, (192, 192, 190))
    screen.blit(text, (250, 280))


# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
test_y = 10

# Game over text
over_text = pygame.font.Font("freesansbold.ttf", 50)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (192, 192, 192))
    screen.blit(score, (x, y))


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystrokes
        if event.type == pygame.KEYDOWN:  # checks if any key is being pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8

            # condition to fire the bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    # Getting the current X coordinate spaceship to fire the bullet from there
                    # bullet sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:  # check for key released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    # if we want anything to persist through out the session we add it in the while loop

    # Background
    # Player movement
    playerX += playerX_change

    # Enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Adding boundaries for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 10

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement (bullet start continuously appearing on the screen)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state is "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Adding boundaries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player(playerX, playerY)
    show_score(text_x, test_y)
    pygame.display.update()
