import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка размеров окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Погоня красного кружка за мышкой")

# Цвета
red = (255, 0, 0)
background_color = (255, 255, 255)

# Параметры кружка
circle_radius = 20
circle_speed = 5

# Начальная позиция кружка
circle_x, circle_y = width // 2, height // 2

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получение позиции мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Проверка, находится ли мышь в пределах экрана
    if 0 <= mouse_x < width and 0 <= mouse_y < height:
        # Вычисление направления движения кружка
        if circle_x < mouse_x:
            circle_x += circle_speed
        elif circle_x > mouse_x:
            circle_x -= circle_speed

        if circle_y < mouse_y:
            circle_y += circle_speed
        elif circle_y > mouse_y:
            circle_y -= circle_speed

    # Очистка экрана
    screen.fill(background_color)

    # Рисование кружка
    pygame.draw.circle(screen, red, (circle_x, circle_y), circle_radius)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение кадров в секунду
    pygame.time.Clock().tick(60)
