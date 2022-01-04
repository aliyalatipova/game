import pygame
from const import *
from loadImage import loadImage


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