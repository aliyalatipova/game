import pygame
from player import Player
from obstacle import Obstacle
from field import Field
from levelLoader import LevelLoader
from const import *
from loadImage import loadImage
import sys


class Coins(pygame.sprite.Sprite):
    image = loadImage("m4.png")

    def __init__(self, v, x1, x2, y1, y2, *group):
        super().__init__(*group)
        self.v = v
        self.image = Coins.image
        self.rect = self.image.get_rect()
        self.rect.x = OBSTACLE_SIZE * x1 + COIN_SIZE * x2
        self.rect.y = (50 + y1 * OBSTACLE_SIZE) + (OBSTACLE_SIZE // 2 - 1.5 * COIN_SIZE) + COIN_SIZE * y2
        self.x_pos = float(self.rect.x)

    def update(self, *args):
        self.x_pos -= self.v / 1000
        self.rect.x = int(self.x_pos)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["GO FAST", "",
                  "Чтобы управлять игроком, необходимо,",
                  "использовать клавиши 'вверх', 'вниз'.",
                  "Нажмите [1], [2] или [3] для выбора уровня,",
                  "либо нажмите любую кнопку для начала игры."]

    fon = pygame.transform.scale(loadImage('fon.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and (pygame.key.get_pressed()[pygame.K_1]
                                                   or pygame.key.get_pressed()[pygame.K_KP1]):
                return 1
            elif event.type == pygame.KEYDOWN and (pygame.key.get_pressed()[pygame.K_2]
                                                   or pygame.key.get_pressed()[pygame.K_KP2]):
                return 2
            elif event.type == pygame.KEYDOWN and (pygame.key.get_pressed()[pygame.K_3]
                                                   or pygame.key.get_pressed()[pygame.K_KP3]):
                return 3
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 1  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def level_start_screen(screen, level):
    intro_text = ["Уровень " + str(level) + ".",
                  "Нажмите любую кнопку для начала."]
    fon = pygame.transform.scale(loadImage('fon.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (1, 0))
    font = pygame.font.Font(None, 45)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def lose_screen(screen):
    # Когда сделаем жизни, здесь надо будет менять текст
    intro_text = ["Вы проиграли.", "",
                  "Нажмите любую кнопку,",
                  "чтобы начать заново."]
    fon = pygame.transform.scale(loadImage('win_lose.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 75)
    text_coord = 65
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def win_screen(screen):
    intro_text = ["Вы выиграли!", "",
                  "Нажмите любую кнопку", "чтобы закончить."]
    fon = pygame.transform.scale(loadImage('win_lose.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 75)
    text_coord = 75
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def main():
    pygame.init()
    size = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    level = start_screen(screen)

    # здесь надо показать стартовое окно с выбором уровня (переменная level)

    hit = False
    money_count = 0
    while level <= LEVEL_COUNT and not hit:
        level_start_screen(screen, level)

        pygame.display.set_caption('Уровень ' + str(level))
        running = True

        dragon_sprite = pygame.sprite.Group()
        player = Player(V + V_delta * (level - 1), screen, 8, 2, dragon_sprite)
        field = Field(screen)

        obst_sprites = pygame.sprite.Group()
        coins_sprites = pygame.sprite.Group()

        level_loader = LevelLoader(level)
        some = level_loader.load()
        # обработка списка уровня
        if level == 1:  # так как в новом формате прописан только 1 уровень
            for i in range(len(some)):
                for j in range(3):
                    if some[i][j] == '#':
                        Obstacle(V + V_delta * (level - 1), i, j, obst_sprites)
                    if some[i][j] == '1':
                        for n in range(OBSTACLE_SIZE // COIN_SIZE):
                            Coins(V + V_delta * (level - 1), i, n, j, 1, coins_sprites)
                    if some[i][j] == '2':
                        for n in range(OBSTACLE_SIZE // COIN_SIZE):
                            Coins(V + V_delta * (level - 1), i, n, j, 0, coins_sprites)
                        for n in range(OBSTACLE_SIZE // COIN_SIZE):
                            Coins(V + V_delta * (level - 1), i, n, j, 1, coins_sprites)
                    if some[i][j] == '3':
                        for n in range(OBSTACLE_SIZE // COIN_SIZE):
                            Coins(V + V_delta * (level - 1), i, n, j, 0, coins_sprites)
                        for n in range(OBSTACLE_SIZE // COIN_SIZE):
                            Coins(V + V_delta * (level - 1), i, n, j, 1, coins_sprites)
                        for n in range(OBSTACLE_SIZE // COIN_SIZE):
                            Coins(V + V_delta * (level - 1), i, n, j, 2, coins_sprites)

        else:
            for i in range(len(some)):
                for j in range(3):
                    if some[i][j] == '1':
                        Obstacle(V + V_delta * (level - 1), i, j, obst_sprites)

        win = False
        iteration_count = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    player.change(pygame.key.get_pressed())

            screen.fill((0, 0, 0))

            field.draw_lines()

            obst_sprites.draw(screen)
            coins_sprites.draw(screen)
            dragon_sprite.draw(screen)
 
            iteration_count = (iteration_count + 1) % 80
            if iteration_count == 5:
                dragon_sprite.update()


            player.coins_check(coins_sprites)

            if not win:  # обработать победу
                if not hit:  # обработать столкновение
                    if not player.going:
                        obst_sprites.update()
                        coins_sprites.update()
                    else:
                        player.run()

            counter = len(obst_sprites)
            for sprite in obst_sprites.spritedict:
                if (player.y_pos > sprite.rect.y) and (player.y_pos < sprite.rect.y + OBSTACLE_SIZE):
                    if player.x_pos + R >= sprite.rect.x and player.x_pos - R <= sprite.rect.x + OBSTACLE_SIZE:
                        hit = True  # обработать столкновение
                        running = False
                if sprite.rect.x + OBSTACLE_SIZE < WINDOW_WIDTH // 2:
                    counter -= 1

            if counter == 0:
                win = True  # обработать победу
                running = False

            pygame.display.flip()

        if hit is True:
            lose_screen(screen)
            level = start_screen(screen)
            hit = False
        else:
            level += 1

    # здесь надо показать финальное окно
    win_screen(screen)
    pygame.quit()


main()
