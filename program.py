import pygame
from player import Player
from obstacle import Obstacle
from field import Field
from levelLoader import LevelLoader
from const import *


def main():         # писала Алия(92-102)
    pygame.init()
    pygame.display.set_caption('попытка 1')
    size = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)

    running = True

    dragon_sprite = pygame.sprite.Group()
    player = Player(screen, 8, 2, dragon_sprite)
    field = Field(screen)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()         # писала София(104-150)
    level = LevelLoader(1)
    some = level.load()
    for i in range(len(some)):
        for j in range(3):
            if some[i][j] == 1:
                Obstacle(i, j, all_sprites)

    win = False
    hit = False
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

        pygame.display.flip()
    pygame.quit()


main()
