import pygame
from const import *
from loadImage import loadImage


class Player(pygame.sprite.Sprite):               # писала Алия(26-35)
    image = loadImage("dragon_sheet8x2.png")

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

    def change(self, *args):
        keys = args[0]
        if keys[pygame.K_DOWN] and self.y_pos < WINDOW_HEIGHT / 2 + OBSTACLE_SIZE:
            self.y_pos = self.y_pos + OBSTACLE_SIZE
        elif keys[pygame.K_UP] and self.y_pos > WINDOW_HEIGHT / 2 - OBSTACLE_SIZE:
            self.y_pos = self.y_pos - OBSTACLE_SIZE

    def is_ball_going(self):
        return self.going
