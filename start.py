import pygame
import sys
import os

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
OBSTACLE_SIZE = 100
fps = 30
V = 40


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Player:
    # класс героя, пока это шарик
    def __init__(self, screen):
        self.x_pos = 0
        self.v = 40
        self.screen = screen
        self.y_pos = 200
        self.going = True

    def run(self, clock):
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x_pos), self.y_pos), 20)
        # print('герой', clock.tick())
        if self.x_pos < 400:
            self.x_pos += V * clock.tick() / 1000
        else:
            self.going = False

    def change(self, *args):
        keys = args[0]
        clock = args[1]
        if keys[pygame.K_DOWN]:
            self.y_pos = self.y_pos + 100

        elif keys[pygame.K_UP]:
            self.y_pos = self.y_pos - 100

    def is_ball_going(self):
        return self.going


class Field:
    def __init__(self, screen):
        self.screen = screen

    def draw_lines(self):
        for i in range(50, 450, 100):
            pygame.draw.line(self.screen, 'White', (0, i), (WINDOW_WIDTH, i), 2)


def return_list(name_file='one'):
    # вот эта функция должна будет по имени текстового файла вернуть список
    return [[0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0], [0, 0, 0],
            [0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0]]
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0],
            #[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 0, 0], [1, 1, 0], [0, 0, 0]]


class Obstacle(pygame.sprite.Sprite):
    image = load_image("obst2.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Obstacle.image
        self.rect = self.image.get_rect()
        self.rect.x = OBSTACLE_SIZE * x
        self.rect.y = 50 + y * OBSTACLE_SIZE
        self.v = 20

    def update(self, *args):
        self.rect.x -= self.v / fps
        clock = args[0]
        print('ost', clock.tick())

        self.rect.x = self.rect.x - clock.tick()
        print(self.rect.x)


def main():
    pygame.init()
    pygame.display.set_caption('попытка 1')
    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)

    running = True

    player = Player(screen)
    field = Field(screen)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    some = return_list()
    for i in range(len(some)):
        for j in range(3):
            if some[i][j] == 1:
                Obstacle(i, j, all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                player.change(pygame.key.get_pressed(), clock)

        screen.fill((0, 0, 0))

        field.draw_lines()

        all_sprites.draw(screen)
        if not player.going:
            all_sprites.update(clock)
        #
        player.run(clock)

        pygame.display.flip()
    pygame.quit()


main()