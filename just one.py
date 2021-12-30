import pygame
import sys
import os

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
OBSTACLE_SIZE = 100
fps = 30
V = 80
R = 30
dragon_sprites = pygame.sprite.Group()
W = 50  # разница между цнтром круга и координатой откуда должен начинатсья отсчет для динозавтра


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x=0, y=150):
        super().__init__(dragon_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        self.rect.x = args[0]
        self.rect.y = args[1]
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

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
        self.screen = screen
        self.y_pos = WINDOW_HEIGHT / 2
        self.going = True

    def draw(self):
        pass
        # я поставила pass чтобы шарик не рисовался
        # pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x_pos), self.y_pos), R)

    def run_start(self):
        if self.x_pos < WINDOW_WIDTH // 2:
            self.x_pos += V / 1000
        else:
            self.going = False

    def run_end(self):
        pass

    def change(self, *args):
        keys = args[0]
        if keys[pygame.K_DOWN] and self.y_pos < WINDOW_HEIGHT / 2 + OBSTACLE_SIZE:
            self.y_pos = self.y_pos + OBSTACLE_SIZE
        elif keys[pygame.K_UP] and self.y_pos > WINDOW_HEIGHT / 2 - OBSTACLE_SIZE:
            self.y_pos = self.y_pos - OBSTACLE_SIZE

    def is_ball_going(self):
        return self.going

    def x_pos_dragon(self):
        return self.x_pos - W

    def y_pos_dragon(self):
        return self.y_pos - W


class Field:
    def __init__(self, screen):
        self.screen = screen

    def draw_lines(self):
        for i in range(50, 450, 100):
            pygame.draw.line(self.screen, 'White', (0, i), (WINDOW_WIDTH, i), 2)


def return_list(name_file='one'):
    map1 = list()
    f = open(f"""{name_file}.txt""", encoding="utf8")
    for number, line in enumerate(f):

        line1 = [int(line[0]), int(line[1]), int(line[2])]
        map1.append(line1)

    f.close()
    # вот эта функция по имени текстового файла возвращает функциюд
    return map1


class Obstacle(pygame.sprite.Sprite):
    image = load_image("obst2.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Obstacle.image
        self.rect = self.image.get_rect()
        self.rect.x = OBSTACLE_SIZE * x
        self.rect.y = 50 + y * OBSTACLE_SIZE
        self.x_pos = float(self.rect.x)

    # София
    def update(self, *args):
        self.x_pos -= V / 1000
        self.rect.x = int(self.x_pos)

    def return_x(self):
        return self.rect.x


def main():
    pygame.init()
    pygame.display.set_caption('попытка 1')
    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)

    running = True

    player = Player(screen)
    field = Field(screen)
    clock = pygame.time.Clock()

    dragon = AnimatedSprite(load_image("dragon_sheet8x2.png"), 8, 2)
    all_sprites = pygame.sprite.Group()
    some = return_list()
    for i in range(len(some)):
        for j in range(3):
            if some[i][j] == 1:
                Obstacle(i, j, all_sprites)
    # София
    win = False
    hit = False

    iteration_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not win and not hit:
                    player.change(pygame.key.get_pressed())

        screen.fill((0, 0, 0))

        field.draw_lines()

        all_sprites.draw(screen)
        player.draw()
        if not win:  # обработать победу
            if not hit:  # обработать столкновение
                if not player.going:
                    all_sprites.update()
                else:
                    player.run_start()

        counter = len(all_sprites)
        for sprite in all_sprites.spritedict:
            if (player.y_pos > sprite.rect.y) and (player.y_pos < sprite.rect.y + OBSTACLE_SIZE):
                if player.x_pos + R >= sprite.rect.x and player.x_pos - R <= sprite.rect.x + OBSTACLE_SIZE:
                    hit = True  # обработать столкновение
                    # print('hit')
            if sprite.rect.x + OBSTACLE_SIZE < WINDOW_WIDTH // 2:
                counter -= 1

        if counter == 0:
            win = True  # обработать победу

        iteration_count = (iteration_count + 1) % 80

        dragon_sprites.draw(screen)
        if iteration_count == 5:

            dragon_sprites.update(player.x_pos_dragon(), player.y_pos_dragon())

        pygame.display.flip()
    pygame.quit()


main()