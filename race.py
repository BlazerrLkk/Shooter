import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Розміри екрану
WIDTH, HEIGHT = 600, 400

# Створення екрану
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гра про гонки")

# Гравець
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 2 * player_height

# Ворожий автомобіль
enemy_width, enemy_height = 50, 50
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 5

# Шрифт для виведення очок
font = pygame.font.SysFont(None, 30)

# Очки
score = 0

# Функція для виведення тексту на екрані
def display_score(score):
    score_text = font.render("Очки: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# Головний цикл гри
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Рух гравця
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += 5

    # Рух ворожого автомобіля
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = -enemy_height
        enemy_x = random.randint(0, WIDTH - enemy_width)
        score += 1

    # Виявлення зіткнення
    if (
        player_x < enemy_x + enemy_width
        and player_x + player_width > enemy_x
        and player_y < enemy_y + enemy_height
        and player_y + player_height > enemy_y
    ):
        game_over = True

    # Відображення на екрані
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, [player_x, player_y, player_width, player_height])
    pygame.draw.rect(screen, WHITE, [enemy_x, enemy_y, enemy_width, enemy_height])

    # Виведення очок
    display_score(score)

    pygame.display.flip()
    clock.tick(30)

# Завершення гри
pygame.quit()
sys.exit()