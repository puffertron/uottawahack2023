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
city_map = Map.open_street_map_processor(parcel_info, random_points(len(parcel_info) + 10, width, height))

# creating surfaces to draw on, background and dots layer
# (layer for truck is stored in truck class)
screen = pygame.display.set_mode(size)
dots = pygame.Surface.copy(screen)

coords_list = []
for entry in city_map.parcels:
    parcel = entry[0]
    coords_list.append(parcel.position)

route = sort_by_distance(coords_list, city_map.warehouse)

tkun = Truck()
tkun.drive_route(route, city_map.warehouse)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for p in coords_list:
        pygame.draw.circle(dots, "white", p, 3.0)

    pygame.draw.circle(dots, "green", city_map.warehouse, 4.0)

    screen.fill("black")
    screen.blit(tkun.surf, tkun.surf.get_rect())
    screen.blit(dots, dots.get_rect(), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()