import pygame
import random

# Screen Settings
WIDTH = 700
HEIGHT = 650
FPS = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DRED = (139, 0, 0)

# init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Time
lastTime = 0
currentTime = 0

# Character
x = WIDTH // 2.4
y = HEIGHT // 1.13
hero = pygame.Rect(x, y, 60, 50)
heroImg = pygame.image.load('gunhand (1).png')
bg = pygame.image.load("PvZ2_lawn1_680.jpg")

# Enemy
enemies = []
enemycd = 5
enemyImage = pygame.image.load('zombie__1_-removebg-preview__1_-removebg-preview.png')
enemyRect = enemyImage.get_rect()
we = enemyRect.width
he = enemyRect.height
enemy_speed = 1
points = 0
last_points = 0

# bullet
wb = 2
hb = 5
bulletImg = pygame.image.load("bullet2 (1) (1).png")
bullets = []
isShot = False

# moving
moving = ''

# fonts
pointsT = pygame.font.SysFont("calibri", 12)
gameover = pygame.font.SysFont("Impact", 70)
sponsored = pygame.font.SysFont("calibri", 14)
gameover_text = gameover.render("YOU DIED", 0, DRED)
startgame = pygame.font.SysFont("Arial", 24)
welcometext = pygame.font.SysFont("calibri", 20)
tip = pygame.font.SysFont("Arial", 16)
openwar = pygame.font.SysFont("calibri", 15)

# HP
heart = pygame.image.load("hpbar1 (1) (1) (1).png")
hp = 10
hp_block = [False] * len(enemies)

END = False
running = True
gamemode = 1
while running:
    if gamemode == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 170 < event.pos[0] < 160 + 170 and 100 < event.pos[1] < 100 + 50:
                    gamemode = 2
                    list_of_hearts = [heart] * hp
                if 170 < event.pos[0] < 160 + 170 and 200 < event.pos[1] < 200 + 50:
                    if event.button == 1:
                        if hp > 5:
                            hp -= 1
                    if event.button == 3:
                        if hp < 15:
                            hp += 1
                if 170 < event.pos[0] < 160 + 170 and 300 < event.pos[1] < 300 + 50:
                    running = False

        text = pointsT.render("Difficulty (LMB-)(RMB+): " + str(hp), 1, BLACK)
        startgame_render = startgame.render("START", 1, BLACK)
        welcometext_render = welcometext.render("Добро пожаловать в игру - OPEN WAR!", 1, WHITE)
        openwar_render = openwar.render("OPEN WAR", 1, BLACK)
        tip_render = tip.render("TIP: In Every 10 Kills Zombie Becomes 2X Faster", 1, WHITE)

        screen.fill(BLACK)
        pygame.draw.rect(screen, (0, 255, 0), (250, 100, 160, 50))
        pygame.draw.rect(screen, (255, 255, 0), (250, 200, 160, 50))
        pygame.draw.rect(screen, (255, 0, 0), (250, 300, 160, 50))

        screen.blit(text, (255, 200))
        screen.blit(startgame_render, (287, 110))
        screen.blit(welcometext_render, (165, 20))
        screen.blit(openwar_render, (286, 300))
        screen.blit(tip_render, (10, 600))
    elif gamemode == 2:
        if END:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    running = False
            screen.fill(BLACK)
            screen.blit(gameover_text, (205, 100))

        else:
            screen.fill(BLACK)
            screen.blit(bg, (0, 0))
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    running = False
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_LEFT:
                        moving = 'LEFT'
                    if i.key == pygame.K_RIGHT:
                        moving = 'RIGHT'
                    if i.key == pygame.K_UP:
                        moving = 'UP'
                    if i.key == pygame.K_DOWN:
                        moving = 'DOWN'
                    if i.key == pygame.K_SPACE:
                        isShot = True
                if i.type == pygame.KEYUP:
                    if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT or i.key == pygame.K_UP or i.key == pygame.K_DOWN:
                        moving = 'STOP'

            # Character Moving
            if moving == 'LEFT' and hero.left > 0:
                hero.left -= 5
            if moving == 'RIGHT' and hero.right < WIDTH:
                hero.left += 5
            if moving == 'UP' and hero.top > 0:
                hero.top -= 5
            if moving == 'DOWN' and hero.bottom < HEIGHT:
                hero.top += 5

            # Colliderect
            # Enemy x Player
            for i in range(len(enemies)):
                if enemies[i].colliderect(hero):
                    if not hp_block[i]:
                        enemies.pop(i)
                        list_of_hearts.pop(0)
                        hp_block.pop(i)
                        break

            # Enemy x Bullet
            for bullet in bullets:
                for enemy in enemies:
                    if enemy.colliderect(bullet):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        points += 1

            # Points
            points_text = pointsT.render("POINTS: " + str(points), 1, (255, 255, 255))
            screen.blit(points_text, (10, 10))

            # Bullets
            # Bullet Create
            if isShot:
                bulRect = pygame.Rect(hero.left + 33, hero.top + 5, wb, hb)
                bullets.append(bulRect)
                isShot = False

            # Bullet blit
            for bullet in bullets:
                screen.blit(bulletImg, (bullet.left, bullet.top))
                bullet.top -= 5

            # Bullet Remove
            index_bul = 0
            for b in bullets:
                if b.bottom < -5:
                    bullets.pop(index_bul)
                index_bul += 1

            # Enemies
            currentTime = pygame.time.get_ticks()
            # Сreate Enemy
            if currentTime - lastTime > enemycd:
                x_enemy = random.randint(we, WIDTH - we)
                enemies.append(pygame.Rect(x_enemy, -he, we, he))
                lastTime = currentTime
                enemycd = random.randint(100, 5000)
                hp_block.append(False)

            if points % 10 == 0 and points != 0 and last_points < points:
                enemy_speed += 1
                last_points = points

            # Enemy blit
            for enemy in enemies:
                screen.blit(enemyImage, (enemy.left, enemy.top))
                enemy.top += enemy_speed

            index_enemy = 0
            # Enemy delete
            for enemy in enemies:
                if enemy.top > HEIGHT:
                    del enemies[index_enemy]
                    del hp_block[index_enemy]

            # Character blit2
            screen.blit(heroImg, (hero.left, hero.top))

            # Hearts
            # Heart blit
            for i in range(len(list_of_hearts)):
                screen.blit(heart, (WIDTH - heart.get_rect().width * (i + 1), 10))

            # if list_of_hearts is empty
            if len(list_of_hearts) == 0:
                END = True

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()