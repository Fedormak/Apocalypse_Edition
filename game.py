import pygame
import random
import sys

WIDTH = 50
HEIGHT = 30
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

    def move_player(self, player_pos, direction):
        x, y = player_pos
        dx, dy = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not self.maze[y][x][direction]:
            return nx, ny
        return x, y


class Monster:
    def __init__(self, maze):
        self.maze = maze
        self.position = self.random_position()

    def random_position(self):
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if not (self.maze.maze[y][x]['N'] or self.maze.maze[y][x]['S'] or
                    self.maze.maze[y][x]['W'] or self.maze.maze[y][x]['E']):
                continue
            return (x, y)

    def move(self, player_pos):
        player_x, player_y = player_pos
        x, y = self.position

        # Вычисление направления к игроку
        if x < player_x:
            direction = 'E'
        elif x > player_x:
            direction = 'W'
        elif y < player_y:
            direction = 'S'
        elif y > player_y:
            direction = 'N'
        else:
            return  # Монстр уже на позиции игрока

        self.move_towards_player(direction)

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

    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Лабиринт")
    clock = pygame.time.Clock()

    player_pos = (0, 0)
    monster1 = Monster(mazf)
    monster2 = Monster(mazf)

    running = True
    while running:
        screen.fill(WHITE)  # Очистка перед отрисовкой

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_pos = mazf.move_player(player_pos, 'N')
        if keys[pygame.K_DOWN]:
            player_pos = mazf.move_player(player_pos, 'S')
        if keys[pygame.K_LEFT]:
            player_pos = mazf.move_player(player_pos, 'W')
        if keys[pygame.K_RIGHT]:
            player_pos = mazf.move_player(player_pos, 'E')

        # Движение монстров
        monster1.move(player_pos)
        monster2.move(player_pos)

        # Проверка на столкновение
        if player_pos == monster1.position or player_pos == monster2.position:
            print("Game Over! The monster caught you!")
            running = False

        # Отрисовка лабиринта, игрока и монстров
        mazf.draw_maze(screen)
        px, py = player_pos
        pygame.draw.circle(screen, RED, (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        monster1.draw(screen)
        monster2.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()