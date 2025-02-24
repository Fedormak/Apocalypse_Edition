import pygame
import random
import sys
import time

WIDTH = 50
HEIGHT = 30
CELL_SIZE = 30

TRANSPARENT_GRAY = (128, 128, 128, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player:
    def __init__(self, maze):
        self.maze = maze

    def generate_posion_player(self):
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if not (self.maze.maze[y][x]['N'] or self.maze.maze[y][x]['S'] or
                    self.maze.maze[y][x]['W'] or self.maze.maze[y][x]['E']):
                continue
            return (x, y)


class Maz:
    def __init__(self):
        self.DIRECTIONS = {
            'N': (0, -1),
            'S': (0, 1),
            'W': (-1, 0),
            'E': (1, 0)
        }
        self.OPPOSITE = {
            'N': 'S',
            'S': 'N',
            'W': 'E',
            'E': 'W'
        }

    def generate_maze(self, width, height):
        self.maze = [[{'N': True, 'S': True, 'W': True, 'E': True} for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

        start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            x, y = stack[-1]
            neighbors = []
            for direction, (dx, dy) in self.DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and not self.visited[ny][nx]:
                    neighbors.append((nx, ny, direction))

            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self.maze[y][x][direction] = False
                self.maze[ny][nx][self.OPPOSITE[direction]] = False
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        print(self.maze)
        return self.maze

    def draw_maze(self, screen):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                cell = self.maze[y][x]
                px, py = x * CELL_SIZE, y * CELL_SIZE
                if cell['N']:
                    pygame.draw.line(screen, BLACK, (px, py), (px + CELL_SIZE, py), 2)
                if cell['S']:
                    pygame.draw.line(screen, BLACK, (px, py + CELL_SIZE), (px + CELL_SIZE, py + CELL_SIZE), 2)
                if cell['W']:
                    pygame.draw.line(screen, BLACK, (px, py), (px, py + CELL_SIZE), 2)
                if cell['E']:
                    pygame.draw.line(screen, BLACK, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 2)

    def caught(self, surface, start_time):
        font = pygame.font.Font(None, 50)
        text = font.render("Меню", True, WHITE)
        restart_text = font.render("Нажмите R, чтобы начать заново", True, RED)

        # Центрируем текст
        surface.blit(text, (WIDTH * CELL_SIZE // 2 - text.get_width() // 2, HEIGHT * CELL_SIZE // 2 - 100))
        surface.blit(restart_text, (WIDTH * CELL_SIZE // 2 - restart_text.get_width() // 2, HEIGHT * CELL_SIZE // 2))

        # Проверяем, что start_time не равен None
        if start_time is not None:
            elapsed_time = time.time() - start_time
            elapsed_time_text = font.render(f"Время игры: {int(elapsed_time)} сек.", True, WHITE)
            surface.blit(elapsed_time_text,
                         (WIDTH * CELL_SIZE // 2 - elapsed_time_text.get_width() // 2, HEIGHT * CELL_SIZE // 2 + 50))

    def move_player(self, player_pos, direction):
        x, y = player_pos
        dx, dy = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not self.maze[y][x][direction]:
            return nx, ny
        return x, y


import time  # Импортируем модуль для работы с временем

class Monster:
    def __init__(self, maze, player_pos):
        self.maze = maze
        self.player_pos = player_pos
        self.position = self.random_position()
        while self.position == player_pos:
            self.position = self.random_position()
        self.x, self.y = self.position
        self.direction = random.choice(["E", "W", "S", "N"])
        self.last_move_time = time.time()  # Время последнего движения
        self.move_delay = 0.3  # Задержка между движениями (в секундах)

    def random_position(self):
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if not (self.maze.maze[y][x]['N'] or self.maze.maze[y][x]['S'] or
                    self.maze.maze[y][x]['W'] or self.maze.maze[y][x]['E']):
                continue
            return (x, y)

    def move(self, player_pos):
        current_time = time.time()  # Текущее время
        if current_time - self.last_move_time < self.move_delay:  # Проверяем задержку
            return  # Если задержка не прошла, монстр не двигается

        self.last_move_time = current_time  # Обновляем время последнего движения
        self.player_pos = player_pos
        player_x, player_y = player_pos
        x, y = self.position

        # Вычисление направления к игроку
        if (abs(player_x - x) <= 5) and (abs(player_y - y) <= 5):
            if x < player_x:
                self.direction = 'E'
            elif x > player_x:
                self.direction = 'W'
            elif y < player_y:
                self.direction = 'S'
            elif y > player_y:
                self.direction = 'N'
            else:
                return  # Монстр уже на позиции игрока

            self.move_towards_player(self.direction)
        else:
            self.move_monster()

    def move_monster(self):
        new_x, new_y = self.position

        # Двигаемся в текущем направлении
        if self.direction == "N" and not self.maze.maze[new_y][new_x]['N']:
            new_y -= 1
        elif self.direction == "S" and not self.maze.maze[new_y][new_x]['S']:
            new_y += 1
        elif self.direction == "W" and not self.maze.maze[new_y][new_x]['W']:
            new_x -= 1
        elif self.direction == "E" and not self.maze.maze[new_y][new_x]['E']:
            new_x += 1
        else:
            self.direction = random.choice(["E", "W", "S", "N"])

        self.position = (new_x, new_y)

    def move_towards_player(self, direction):
        x, y = self.position

        # Двигаем монстра в указанном направлении, если это возможно
        if direction == 'N' and not self.maze.maze[y][x]['N']:
            y -= 1
        elif direction == 'S' and not self.maze.maze[y][x]['S']:
            y += 1
        elif direction == 'W' and not self.maze.maze[y][x]['W']:
            x -= 1
        elif direction == 'E' and not self.maze.maze[y][x]['E']:
            x += 1

        self.position = (x, y)

    def draw(self, screen):
        px, py = self.position
        pygame.draw.circle(screen, GREEN, (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

def main():
    pygame.init()
    mazf = Maz()
    maze = mazf.generate_maze(WIDTH, HEIGHT)

    player = Player(mazf)
    player_pos = player.generate_posion_player()

    N_mosters = 15
    listOfMomster = list()
    MonsterPosition = list()
    for _ in range(N_mosters):
        monster = Monster(mazf, player_pos)
        listOfMomster.append(monster)

    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Лабиринт")
    clock = pygame.time.Clock()

    start_time = time.time()  # Запись времени начала игры

    isEnd = False
    menu_surface = pygame.Surface((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE), pygame.SRCALPHA)
    menu_surface.fill(TRANSPARENT_GRAY)

    #Указать количество монстров

    running = True
    while running:
        screen.fill(WHITE)  # Очистка перед отрисовкой

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Нажатие пробела
                    isEnd = not isEnd  # Переключение меню
                elif event.key == pygame.K_r and isEnd:  # Нажатие R для перезапуска
                    isEnd = False  # Закрыть меню
                    mazf.generate_maze(WIDTH, HEIGHT)
                    player_pos = player.generate_posion_player()
                    screen.fill(WHITE)
                    listOfMomster.clear()
                    MonsterPosition.clear()
                    for _ in range(N_mosters):
                        monster = Monster(mazf, player_pos)
                        listOfMomster.append(monster)

        keys = pygame.key.get_pressed()
        if not isEnd:
            if keys[pygame.K_UP]:
                player_pos = mazf.move_player(player_pos, 'N')
            if keys[pygame.K_DOWN]:
                player_pos = mazf.move_player(player_pos, 'S')
            if keys[pygame.K_LEFT]:
                player_pos = mazf.move_player(player_pos, 'W')
            if keys[pygame.K_RIGHT]:
                player_pos = mazf.move_player(player_pos, 'E')

        # Проверка на достижение угла карты
        if player_pos == (0, 0) or \
                player_pos == (WIDTH - 1, 0) or \
                player_pos == (0, HEIGHT - 1) or \
                player_pos == (WIDTH - 1, HEIGHT - 1):
            # Генерация новой карты и монстров
            mazf.generate_maze(WIDTH, HEIGHT)
            player_pos = player.generate_posion_player()
            listOfMomster.clear()
            MonsterPosition.clear()
            for _ in range(N_mosters):
                monster = Monster(mazf, player_pos)
                listOfMomster.append(monster)

        # Движение монстров
        for monster in listOfMomster:
            monster.move(player_pos)
            MonsterPosition.append(monster.position)

        # Отрисовка лабиринта, игрока и монстров
        mazf.draw_maze(screen)
        px, py = player_pos

        # Проверка на столкновение
        if not isEnd and player_pos in MonsterPosition:
            isEnd = True
            print("Game Over! The monster caught you!")

        # Отрисовка элементов после того как тебя поймали
        if isEnd:
            screen.blit(menu_surface, (0, 0))
            mazf.caught(screen, start_time)
            start_time = None  # Чтобы не считалось время некст раунда

        pygame.draw.circle(screen, RED, (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 4)

        for monster in listOfMomster:
            monster.draw(screen)

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()