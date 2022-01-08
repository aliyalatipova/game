import pygame
from const import *
from loadImage import loadImage


class Obstacle(pygame.sprite.Sprite):       # писала Алия, исправила София(1-16)
    image = loadImage("obst2.png")

    def __init__(self, v, x, y, *group):
        super().__init__(*group)
        self.v = v
        self.image = Obstacle.image
        self.rect = self.image.get_rect()
        self.rect.x = OBSTACLE_SIZE * x
        self.rect.y = 50 + y * OBSTACLE_SIZE
        self.x_pos = float(self.rect.x)

    def update(self, *args):            #писала София(18-21)
        self.x_pos -= self.v / 1000
        self.rect.x = int(self.x_pos)
