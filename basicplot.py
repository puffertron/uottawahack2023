import pygame
import random
import sys
import math
import time

from pygame import Vector2

from Structures.Truck import Truck
from Structures.StreetMap import StreetMap
from Structures.Map import Map

from algorythms import * 

import Structures

## PYGAME WINDOW CREATION
pygame.init()
size = width, height = 800, 800

#Map Creation
parcel_info = create_parcel_info()
#TODO - This next line should take random map data
Map.open_street_map_processor(parcel_info, random_points(len(parcel_info) + 10, width, height))

# creating surfaces to draw on, background and dots layer
# (layer for truck is stored in truck class)
screen = pygame.display.set_mode(size)
streetmap = pygame.surface.copy(screen)
dots = pygame.Surface.copy(screen)

<<<<<<< HEAD
coords_list = []
for parcel in Map.parcels:
    coords_list.append(parcel.position)
=======

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
>>>>>>> dc4af6f46460f6d7b29c115eff37f581775dfa52

route = sort_by_distance(coords_list, Map.warehouse)

tkun = Truck()
tkun.drive_route(route, Map.warehouse)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for p in coords_list:
        pygame.draw.circle(dots, "white", p, 3.0)

    pygame.draw.circle(dots, "green", Map.warehouse, 4.0)

    screen.fill("black")
    screen.blit(tkun.surf, tkun.surf.get_rect())
    screen.blit(dots, dots.get_rect(), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()