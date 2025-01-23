import pygame as pg

class monster():
    def __init__(self, h, v, pos, screen):
        super().__init__()
        self.screen = screen
        self.radius = h
        self.v = v
        self.x, self.y = pos
        self.clock = pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.xn, self.yn = event.pos
                    self.move()


    def move(self):
        while self.x != self.xn or self.y != self.yn:
            self.drag([self.xn, self.yn])


    def drag(self, coords):
        x, y = coords
        if self.x < x:
            self.x += self.v
        elif self.x > x:
            self.x -= self.v
        if self.y < y:
            self.y += self.v
        elif self.y > y:
            self.y -= self.v
        pg.draw.circle(self.screen, 'red', [self.x, self.y], self.radius)
        pg.display.flip()




if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode([400, 800])
    m = monster(10, 5, [10, 10], screen)
    while pg.event.wait().type != pg.QUIT:
        pass
    quit()
