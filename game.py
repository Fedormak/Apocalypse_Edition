import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Run from the Monster!")

# Цвета
hero_color = (0, 255, 0)
monster_color = (255, 0, 0)
wall_color = (0, 0, 255)
background_color = (255, 255, 255)

# Параметры героя
hero_pos = [width // 2, height // 2]
hero_size = 20
hero_speed = 5

# Параметры монстра
monster_pos = [random.randint(0, width - 20), random.randint(0, height - 20)]
monster_size = 20

# Генерация стен
walls = []
for _ in range(10):  # 10 случайных стен
    wall_x = random.randint(0, width - 50)
    wall_y = random.randint(0, height - 50)
    wall_rect = pygame.Rect(wall_x, wall_y, 50, 10)  # Прямоугольные стены
    walls.append(wall_rect)


# Функция для проверки столкновения
def check_collision(rect, walls):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False


# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление героем
    keys = pygame.key.get_pressed()
    new_hero_pos = hero_pos[:]

    if keys[pygame.K_LEFT]:
        new_hero_pos[0] -= hero_speed
    if keys[pygame.K_RIGHT]:
        new_hero_pos[0] += hero_speed
    if keys[pygame.K_UP]:
        new_hero_pos[1] -= hero_speed
    if keys[pygame.K_DOWN]:
        new_hero_pos[1] += hero_speed

    # Проверка выхода за границы экрана
    new_hero_pos[0] = max(0, min(new_hero_pos[0], width - hero_size))
    new_hero_pos[1] = max(0, min(new_hero_pos[1], height - hero_size))

    # Проверка столкновения героя со стенами
    hero_rect = pygame.Rect(new_hero_pos[0], new_hero_pos[1], hero_size, hero_size)
    if not check_collision(hero_rect, walls):
        hero_pos = new_hero_pos

    # Логика движения монстра
    if hero_pos[0] < monster_pos[0]:
        monster_pos[0] -= 2  # Двигаем монстра влево
    elif hero_pos[0] > monster_pos[0]:
        monster_pos[0] += 2  # Двигаем монстра вправо

    if hero_pos[1] < monster_pos[1]:
        monster_pos[1] -= 2  # Двигаем монстра вверх
    elif hero_pos[1] > monster_pos[1]:
        monster_pos[1] += 2  # Двигаем монстра вниз

    # Проверка выхода монстра за границы экрана
    monster_pos[0] = max(0, min(monster_pos[0], width - monster_size))
    monster_pos[1] = max(0, min(monster_pos[1], height - monster_size))

    # Проверка столкновения монстра со стенами
    monster_rect = pygame.Rect(monster_pos[0], monster_pos[1], monster_size, monster_size)
    if check_collision(monster_rect, walls):
        if hero_pos[0] < monster_pos[0]:
            monster_pos[0] += 2
        elif hero_pos[0] > monster_pos[0]:
            monster_pos[0] -= 2

        if hero_pos[1] < monster_pos[1]:
            monster_pos[1] += 2
        elif hero_pos[1] > monster_pos[1]:
            monster_pos[1] -= 2

    # Очистка экрана
    screen.fill(background_color)

    # Рисование стен
    for wall in walls:
        pygame.draw.rect(screen, wall_color, wall)

    # Рисование героя и монстра
    pygame.draw.rect(screen, hero_color, (hero_pos[0], hero_pos[1], hero_size, hero_size))
    pygame.draw.rect(screen, monster_color, (monster_pos[0], monster_pos[1], monster_size, monster_size))

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(100)
