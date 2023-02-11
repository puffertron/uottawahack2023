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
size = width, height = 320, 240
#warehouse_pos = Vector2(width/2, height/2)

#Map Creation
parcels = create_parcels()
city_map = Map(parcels, "warehouse", random_points(len(parcels) + 1, width, height))

# creating surfaces to draw on, background and dots layer
# (layer for truck is stored in truck class)
screen = pygame.display.set_mode(size)
dots = pygame.Surface.copy(screen)

# global coords variable, this is a primitive list of packages
coords = [Vector2(0,0)]

# coords = cluster_points(5, 5, 10)
coords = random_points(10)

route = sort_by_distance(coords, city_map.warehouse.position)


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