import pygame
from const import *
from loadImage import loadImage


class Coins2(pygame.sprite.Sprite):
    image = loadImage("coins11.png", -1)

    def __init__(self, v, x1, x2, y1, y2, columns=10, rows=1, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(self.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = OBSTACLE_SIZE * x1 + COIN_SIZE * x2
        self.rect.y = (50 + y1 * OBSTACLE_SIZE) + (OBSTACLE_SIZE // 2 - 1.5 * COIN_SIZE) + COIN_SIZE * y2
        self.x_pos = float(self.rect.x)
        self.v = v
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, should_go=True):
        if should_go:
            self.coins_run()
        self.whirl()

    def whirl(self):
        self.counter = (self.counter + 1) % 200
        if self.counter == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def coins_run(self):
        self.x_pos -= self.v / 1000
        self.rect.x = int(self.x_pos)
