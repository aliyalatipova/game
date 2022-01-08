import pygame
from particle import Particle
from player import Player
from obstacle import Obstacle
from field import Field
from levelLoader import LevelLoader
from const import *
from loadImage import loadImage
from Coins2 import Coins2
from All_money_counter import AllMoneyCounter
import sys
import random


def terminate():            # писала софия(1-143)
    pygame.quit()
    sys.exit()


def start_screen(screen):
    all_money_counter = AllMoneyCounter()
    all_money_counter.load_from_txt()
    coins = str(all_money_counter.money_at_start_of_race)
    intro_text = ["GO FAST                                                    Монет заработано: " + coins,
                  "",
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


def level_start_screen(screen, level, last_level_coins):
    intro_text = ["Уровень " + str(level) + ".",
                  "Нажмите любую кнопку для начала.", ""]

    if last_level_coins > 0:
        intro_text.append("В прошлом уровне вы заработали " + str(last_level_coins) + " монет!")

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


def lose_screen(screen, all_money_counter):
    # Когда сделаем жизни, здесь надо будет менять текст
    intro_text = ["Вы проиграли.", "",
                  "Нажмите любую кнопку, чтобы начать заново."]
    if all_money_counter.get_all_money() > LIFE_PRICE:
        intro_text.append("Либо нажмите [D], чтобы купить жизнь за " + str(LIFE_PRICE) + " монет.")
    fon = pygame.transform.scale(loadImage('lose.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font(None, 45)

    while True:
        screen.blit(fon, (0, 0))
        text_coord = 65
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            delta = random.randrange(3) - 1
            intro_rect.top += delta
            intro_rect.x = 10
            delta = random.randrange(3) - 1
            intro_rect.x += delta
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_d]:
                if all_money_counter.get_all_money() > LIFE_PRICE:
                    all_money_counter.set_money_at_start_of_race(all_money_counter.get_all_money() - LIFE_PRICE)
                    all_money_counter.load_to_txt()
                    return True
                else:
                    return False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return False
        pygame.display.flip()
        clock.tick(fps)


def create_particles(position, all_sprites):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), all_sprites)


def win_screen(screen):
    intro_text = ["Вы выиграли!", "",
                  "Нажмите любую кнопку,", "чтобы закончить."]
    font = pygame.font.Font(None, 75)
    fon = pygame.transform.scale(loadImage('win_lose.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    fire = 0
    while True:
        screen.blit(fon, (0, 0))
        text_coord = 75
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        if fire == 0:
            create_particles((int(WINDOW_WIDTH * random.random()), int(WINDOW_HEIGHT * random.random())), all_sprites)
        fire += 1
        if fire == FIRE_DELAY:
            fire = 0

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


# обработка списка уровня, писала алия
def list_processing(level, some, obst_sprites, coins_sprites):  # писала алия
    if level == 1 or level == 2 or level == 3:
        for i in range(len(some)):
            for j in range(3):
                if some[i][j] == '#':
                    Obstacle(V + V_delta * (level - 1), i, j, obst_sprites)
                if some[i][j] == '1':
                    for n in range(OBSTACLE_SIZE // COIN_SIZE):
                        Coins2(V + V_delta * (level - 1), i, n, j, 1, 10, 1, coins_sprites)
                if some[i][j] == '2':
                    for n in range(OBSTACLE_SIZE // COIN_SIZE):
                        Coins2(V + V_delta * (level - 1), i, n, j, 0, 10, 1, coins_sprites)
                    for n in range(OBSTACLE_SIZE // COIN_SIZE):
                        Coins2(V + V_delta * (level - 1), i, n, j, 1, 10, 1, coins_sprites)
                if some[i][j] == '3':
                    for n in range(OBSTACLE_SIZE // COIN_SIZE):
                        Coins2(V + V_delta * (level - 1), i, n, j, 0, 10, 1, coins_sprites)
                    for n in range(OBSTACLE_SIZE // COIN_SIZE):
                        Coins2(V + V_delta * (level - 1), i, n, j, 1, 10, 1, coins_sprites)
                    for n in range(OBSTACLE_SIZE // COIN_SIZE):
                        Coins2(V + V_delta * (level - 1), i, n, j, 2, 10, 1, coins_sprites)


# функции, которые должны выполнятся каждую итерацию, писала алия
def functions_for_each_iteration(screen, field, obst_sprites, coins_sprites, dragon_sprite, player, all_money_counter):
    screen.fill((0, 0, 0))
    field.draw_lines()
    obst_sprites.draw(screen)
    coins_sprites.draw(screen)
    dragon_sprite.draw(screen)
    player.coins_check(all_money_counter, coins_sprites)
    player.text_money(screen, all_money_counter)
    all_money_counter.print_all_money(screen)


def end_of_one_race(player, all_money_counter):
    player.count_money(all_money_counter)
    all_money_counter.load_to_txt()


def main():
    pygame.init()
    size = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    level = start_screen(screen)

    hit = False
    last_level_coins = 0  # монеты, заработанные в прошлом уровне
    while level <= LEVEL_COUNT and not hit:
        level_start_screen(screen, level, last_level_coins)
        last_level_coins = 0

        pygame.display.set_caption('Уровень ' + str(level))
        running = True

        # cоздание групп спрайтов и объектов
        dragon_sprite = pygame.sprite.Group()
        player = Player(V + V_delta * (level - 1), screen, 8, 2, dragon_sprite)
        field = Field(screen)
        obst_sprites = pygame.sprite.Group()
        coins_sprites = pygame.sprite.Group()

        all_money_counter = AllMoneyCounter()
        all_money_counter.load_from_txt()
        level_loader = LevelLoader(level)
        some = level_loader.load()

        # обработка списка уровня
        list_processing(level, some, obst_sprites, coins_sprites)

        win = False
        iteration_count = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYDOWN:
                    player.change(pygame.key.get_pressed())

            functions_for_each_iteration(screen, field, obst_sprites, coins_sprites, dragon_sprite, player,
                                         all_money_counter)
 
            iteration_count = (iteration_count + 1) % 80
            if iteration_count == 5:
                dragon_sprite.update()
                # coins_sprites.update()

            if not win:  # обработать победу
                if not hit:  # обработать столкновение
                    if not player.going:
                        obst_sprites.update()
                        coins_sprites.update()
                    else:
                        coins_sprites.update(False)
                        player.run()

            counter = len(obst_sprites)
            for sprite in obst_sprites.spritedict:
                if (player.y_pos > sprite.rect.y) and (player.y_pos < sprite.rect.y + OBSTACLE_SIZE):
                    if player.x_pos + R >= sprite.rect.x and player.x_pos - R <= sprite.rect.x + OBSTACLE_SIZE:
                        hit = True  # обработать столкновение
                        running = False
                        end_of_one_race(player, all_money_counter)
                        if lose_screen(screen, all_money_counter):
                            hit = False
                            running = True
                            player.x_pos -= 80
                if sprite.rect.x + OBSTACLE_SIZE < WINDOW_WIDTH // 2:
                    counter -= 1

            if counter == 0:
                win = True  # обработать победу
                last_level_coins = all_money_counter.get_money_in_one_race()
                end_of_one_race(player, all_money_counter)
                running = False

            pygame.display.flip()

        if hit is True:
            end_of_one_race(player, all_money_counter)
            level = start_screen(screen)
            hit = False
        else:
            level += 1

    # здесь надо показать финальное окно
    win_screen(screen)
    pygame.quit()


main()
