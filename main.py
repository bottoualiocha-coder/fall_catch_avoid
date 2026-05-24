import pygame
from random import randint

pygame.init()

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

comic_sans_font_60 = pygame.font.SysFont("comic sans", 60)

character_image = pygame.image.load("assets/personage-2-pixilart.png")
character_image = pygame.transform.rotozoom(character_image, 0, 0.5)
character_rect = character_image.get_rect(midbottom=(450, 700))

icon_image = pygame.image.load("assets/personage-pixilart.png")
icon_image = pygame.transform.rotozoom(icon_image, 0, 1.7)
icon_rect = icon_image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 80))

pygame.display.set_caption("Fall, Catch, Avoid")
pygame.display.set_icon(character_image)

bomb_image = pygame.image.load("assets/bomb-pixilart.png")
bomb_list = []

coin_image = pygame.image.load("assets/pixilart-coin.png")
coin_list = []

diamond_image = pygame.image.load("assets/diamond-pixilart.png")
diamond_image = pygame.transform.rotozoom(diamond_image, 45, 1)
diamond_list = []

heart_image = pygame.image.load("assets/pixel-heart-pixilart-removebg-preview.png")
heart_list = []

for i in range(3):
    heart_list.append(heart_image.get_rect(topright=(WIDTH - 10 - i * 82, 10)))

game_active = True
score = 0

SUMMON_BOMB = pygame.USEREVENT + 1
pygame.time.set_timer(SUMMON_BOMB, (500))

SUMMON_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SUMMON_COIN, (1500))

SUMMON_DIAMOND = pygame.USEREVENT + 3
pygame.time.set_timer(SUMMON_DIAMOND, (4500))

game_over_text = comic_sans_font_60.render("Game Over", True, (255, 0, 0))
game_over_text_rect = game_over_text.get_rect(midtop=(WIDTH / 2, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SUMMON_COIN:
            coin_list.append(coin_image.get_rect(midbottom=(randint(1, WIDTH), 0)))
        if event.type == SUMMON_BOMB:
            bomb_list.append(bomb_image.get_rect(midbottom=(randint(1, WIDTH - 50), 0)))
        if event.type == SUMMON_DIAMOND:
            diamond_list.append(diamond_image.get_rect(midbottom=(randint(1, WIDTH - 50), 0)))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not game_active:
            for i in range(3):
                heart_list.append(heart_image.get_rect(topright=(WIDTH - 10 - i * 82, 10)))
            game_active = True
            coin_list.clear()
            bomb_list.clear()
            diamond_list.clear()
            score = 0

    if game_active:

        score_text = comic_sans_font_60.render(f"Score : {score}", True, (0, 0, 255))
        score_text_rect = score_text.get_rect(midtop=(WIDTH / 2, 0))

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and character_rect.left > 0:
            character_rect.x -= 7
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and character_rect.right < WIDTH:
            character_rect.x += 7

        screen.fill("light blue")
        screen.blit(character_image, character_rect)
        screen.blit(score_text, score_text_rect)
        for heart_rect in heart_list:
            screen.blit(heart_image,heart_rect)

        for coin_rect in coin_list:
            screen.blit(coin_image, coin_rect)
            coin_rect.y += 10
            if coin_rect.top > HEIGHT:
                coin_list.remove(coin_rect)

        for bomb_rect in bomb_list:
            bomb_rect.y += 10
            screen.blit(bomb_image, bomb_rect)
            if bomb_rect.top > HEIGHT:
                bomb_list.remove(bomb_rect)

        for diamond_rect in diamond_list:
            diamond_rect.y += 10
            screen.blit(diamond_image, diamond_rect)
            if diamond_rect.top > HEIGHT:
                diamond_list.remove(diamond_rect)

        bomb_index = character_rect.collidelist(bomb_list)
        if bomb_index != -1:
            heart_list.pop()
            bomb_list.pop(bomb_index)
            if not heart_list:
                game_active = False

        coin_index = character_rect.collidelist(coin_list)
        if coin_index != -1:
            coin_list.pop(coin_index)
            score += 1

        diamond_index = character_rect.collidelist(diamond_list)
        if diamond_index != -1:
            diamond_list.pop(diamond_index)
            score += 5

    else:
        screen.fill("#f5d3a4")
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(icon_image, icon_rect)

    pygame.display.update()
    clock.tick(60)
