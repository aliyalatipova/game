import pygame
from player import Player
from obstacle import Obstacle
from field import Field
from levelLoader import LevelLoader
from const import *
from loadImage import loadImage
import sys


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["GO FAST", "",
                  "Чтобы управлять игроком, необходимо,",
                  "использовать клавиши 'вверх', 'вниз'"]

    fon = pygame.transform.scale(loadImage('fon.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def main():         # писала Алия(92-102)
    pygame.init()
    level = 1
    level_count = 3
    size = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    start_screen(screen)

    # здесь надо показать стартовое окно с выбором уровня (переменная level)

    hit = False
    while level <= level_count and hit == False:
        # здесь надо показать стартовое окно уровня
        pygame.display.set_caption('Уровень ' + str(level))
        running = True

        dragon_sprite = pygame.sprite.Group()
        player = Player(V + V_delta * (level - 1), screen, 8, 2, dragon_sprite)
        field = Field(screen)

        all_sprites = pygame.sprite.Group()         # писала София(104-150)
        level_loader = LevelLoader(level)
        some = level_loader.load()
        for i in range(len(some)):
            for j in range(3):
                if some[i][j] == 1:
                    Obstacle(V + V_delta * (level - 1), i, j, all_sprites)

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

            all_sprites.draw(screen)
            dragon_sprite.draw(screen)
            iteration_count = (iteration_count + 1) % 80
            if iteration_count == 5:
                dragon_sprite.update()

            if not win:  # обработать победу
                if not hit:  # обработать столкновение
                    if not player.going:
                        all_sprites.update()
                    else:
                        player.run()

            counter = len(all_sprites)
            for sprite in all_sprites.spritedict:
                if player.y_pos > sprite.rect.y and player.y_pos < sprite.rect.y + OBSTACLE_SIZE:
                    if player.x_pos + R >= sprite.rect.x and player.x_pos - R <= sprite.rect.x + OBSTACLE_SIZE:
                        hit = True  # обработать столкновение
                        # print('hit')
                if sprite.rect.x + OBSTACLE_SIZE < WINDOW_WIDTH // 2:
                    counter -= 1

            if counter == 0:
                win = True  # обработать победу
                running = False

            pygame.display.flip()
        level += 1

    # здесь надо показать финальное окно
    pygame.quit()


main()
