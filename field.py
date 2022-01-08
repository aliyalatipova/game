import pygame
from const import *


class Field:            # писала Алия (1-11)
    def __init__(self, screen):
        self.screen = screen

    def draw_lines(self):
        for i in range(50, 450, 100):
            pygame.draw.line(self.screen, 'White', (0, i), (WINDOW_WIDTH, i), 2)
