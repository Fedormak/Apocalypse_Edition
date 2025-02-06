import pygame
import random
import sys

WIDTH = 50
HEIGHT = 30
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class maz:
    def __init__(self):


# Направления движения
        self.DIRECTIONS = {
    'N': (0, -1),
    'S': (0, 1),
    'W': (-1, 0),
    'E': (1, 0)
}

# Обратные направления
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


    def fihish(self):
        pass


def main():
    pygame.init()
    mazf = maz()
    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Лабиринт")
    clock = pygame.time.Clock()

    maze = mazf.generate_maze(WIDTH, HEIGHT)

    player_pos = (0, 0)

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_pos = mazf.move_player(player_pos, 'N')
        if keys[pygame.K_DOWN]:
            player_pos = mazf.move_player( player_pos, 'S')
        if keys[pygame.K_LEFT]:
            player_pos = mazf.move_player( player_pos, 'W')
        if keys[pygame.K_RIGHT]:
            player_pos = mazf.move_player( player_pos, 'E')

        mazf.draw_maze(screen)

        px, py = player_pos
        pygame.draw.circle(screen, RED, (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()