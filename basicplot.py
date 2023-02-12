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
dots = pygame.Surface.copy(screen)

coords_list = []
for parcel in Map.parcels:
    coords_list.append(parcel.position)

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