import pygame
import math


class Truck:
    def __init__(self):
        self.color = "purple"
        self.capacity = 5
        self.speed = .01
        self.surf = pygame.Surface(pygame.display.get_window_size())
    
    def drive_route(self, route, start):
        last = start
        for p in route:
            pygame.draw.line(self.surf, self.color, last, p, 2)
            last = p