import pygame
import random
import sys
import math
import time

from pygame import Vector2

from Structures.Truck import Truck
from Structures.StreetMap import StreetMap

from algorythms import *


import Structures


## PYGAME WINDOW CREATION
pygame.init()
size = width, height = 320, 240
middle = Vector2(width/2, height/2)

# creating surfaces to draw on, background and dots layer
# (layer for truck is stored in truck class)
screen = pygame.display.set_mode(size)
dots = pygame.Surface.copy(screen)

# global coords variable, this is a primitive list of packages
coords = [Vector2(0,0)]

def random_points(amt) -> list[Vector2]:
    """generate x number of points randomly distributed, returns a list of Vec2"""
    points = []
    for i in range(1, amt):
        vec = Vector2(random.randint(0, width), random.randint(0, height))
        points.append(vec)
    
    return points

def cluster_points(density, c_amt, c_rad) -> list[Vector2]:
    """generate y number of clusters, containing x number of points within z radius, returns a list of Vec2"""
    clusters = []
    points = []
    for i in range(1, c_amt):
        vec = Vector2(random.randint(0, width), random.randint(0, height))
        clusters.append(vec)
    
    for c in clusters:
        for i in range(density):
            vec = Vector2(random.randint(c.x-c_rad, c.x-c_rad), random.randint(c.y-c_rad, c.y-c_rad))
            points.append(vec)
    
    return points

# coords = cluster_points(5, 5, 10)
coords = random_points(10)

route = sort_by_distance(coords, middle)


tkun = Truck()
tkun.drive_route(route, (width/2, height/2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for p in coords:
        pygame.draw.circle(dots, "white", p, 3.0)

    pygame.draw.circle(dots, "green", (width/2, height/2), 4.0)

    screen.fill("black")
    screen.blit(tkun.surf, tkun.surf.get_rect())
    screen.blit(dots, dots.get_rect(), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()