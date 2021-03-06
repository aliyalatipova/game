from const import *
from loadImage import loadImage
from All_money_counter import *


class Player(pygame.sprite.Sprite):               # писала Алия(1-44)
    image = loadImage("динозавр 4.png", -1)
    last_move_up = False
    last_move_down = False

    # класс героя, пока это динозавр с урока
    def __init__(self, v, screen, columns, rows, *group):
        super().__init__(*group)
        self.v = v
        self.x_pos = 0
        self.screen = screen
        self.y_pos = WINDOW_HEIGHT / 2
        self.going = True
        self.frames = []
        self.cut_sheet(self.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(0, 150)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.rect.x = int(self.x_pos) - W
        self.rect.y = int(self.y_pos) - W
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def run(self):
        if self.x_pos < WINDOW_WIDTH // 2:
            self.x_pos += self.v / 1000
        else:
            self.going = False

    def change(self, *args):                #писала София(46-63)
        keys = args[0]
        if keys[pygame.K_DOWN] and self.y_pos < WINDOW_HEIGHT / 2 + OBSTACLE_SIZE:
            self.y_pos = self.y_pos + OBSTACLE_SIZE
            self.last_move_down = True
        elif keys[pygame.K_UP] and self.y_pos > WINDOW_HEIGHT / 2 - OBSTACLE_SIZE:
            self.y_pos = self.y_pos - OBSTACLE_SIZE
            self.last_move_up = True

    def reset_move_flags(self):
        self.last_move_up = False
        self.last_move_down = False

    def was_last_move_up(self):
        return self.last_move_up

    def was_last_move_down(self):
        return self.last_move_down

    def is_ball_going(self):
        return self.going

    def coins_check(self, all_money_counter, *args): # писала Алия(65-83)
        coins_sprite = args[0]
        if pygame.sprite.spritecollide(self, coins_sprite, False):
            all_money_counter.set_money_in_one_race(all_money_counter.get_money_in_one_race() + len(pygame.sprite.spritecollide(self, coins_sprite, False)))
        pygame.sprite.spritecollide(self, coins_sprite, True)

    def count_money(self, all_money_counter):
        print(all_money_counter.get_money_in_one_race())

    def text_money(self, screen, all_money_counter):
        font = pygame.font.Font(None, 50)
        text = font.render(str(all_money_counter.get_money_in_one_race()), True, 'White')
        screen.blit(text, (700, 10))

    def return_number_money_in_one_race(self, all_money_counter):
        return all_money_counter.get_money_in_one_race()
