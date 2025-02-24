import pygame
import csv
import os
from game import main

# Инициализация Pygame
pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{30},{50}"

# Настройки окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Приветственное окно")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Шрифты
font = pygame.font.Font(None, 36)

# Поле для ввода
input_box = pygame.Rect(150, 150, 300, 50)
input_text = ''
active = False

# Кнопка "Играть"
button = pygame.Rect(250, 250, 100, 50)

# CSV-файл для записи
csv_file = "players.csv"

# Создание файла, если он не существует
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nickname", "Score"])  # Заголовки столбцов

# Функция для записи данных в CSV
def write_to_csv(nickname, score=0):
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([nickname, score])

# Основной цикл
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка нажатия на поле ввода
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            # Проверка нажатия на кнопку "Играть"
            if button.collidepoint(event.pos) and input_text.strip():
                write_to_csv(input_text.strip())  # Запись ника в CSV
                print(f"Игрок {input_text.strip()} добавлен в CSV!")
                running = False  # Закрыть окно после нажатия
                main()
                exit()
        elif event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_RETURN:  # Нажатие Enter
                if input_text.strip():
                    write_to_csv(input_text.strip())
                    print(f"Игрок {input_text.strip()} добавлен в CSV!")
                    running = False
                    main()
                    exit()
            elif event.key == pygame.K_BACKSPACE:  # Удаление символа
                input_text = input_text[:-1]
            else:
                input_text += event.unicode  # Добавление символа

    # Рисование поля ввода
    pygame.draw.rect(screen, BLUE if active else GRAY, input_box, 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    # Рисование кнопки "Играть"
    pygame.draw.rect(screen, GRAY, button)
    button_text = font.render("Играть", True, BLACK)
    screen.blit(button_text, (button.x + 10, button.y + 10))

    # Инструкция
    instruction = font.render("Введите ваш ник:", True, BLACK)
    screen.blit(instruction, (150, 100))

    # Обновление экрана
    pygame.display.flip()

pygame.quit()