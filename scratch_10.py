import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smooth Chasing Circle")

# Цвета
red = (255, 0, 0)
background_color = (255, 255, 255)

# Позиция кружка
circle_pos = [width // 2, height // 2]
circle_radius = 30
# Скорость движения круга
speed = 0.03

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получение позиции мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Проверка, находится ли мышка в пределах окна
    if 0 <= mouse_x <= width and 0 <= mouse_y <= height:
        # Плавное движение круга
        circle_pos[0] += (mouse_x - circle_pos[0]) * speed
        circle_pos[1] += (mouse_y - circle_pos[1]) * speed

    # Очистка экрана
    screen.fill(background_color)

    # Рисование кружка
    pygame.draw.circle(screen, red, (int(circle_pos[0]), int(circle_pos[1])), circle_radius)

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(60)
