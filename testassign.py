import pygame

import config
from algorithms import *
from algorythms import *
from Structures.Truck import Truck
from Structures.Map import Map

size = width, height = 800, 800
parcel_info = create_parcel_info()  
Map.set_up_state(parcel_info, random_points(len(parcel_info) + 10, width, height))

quadtree = construct_quadtree()
clusters = assign_clusters(Map.parcels,max((config.map_width,config.map_height)),quadtree)
routes = assign_destinations(quadtree, clusters)


pygame.init()
screen = pygame.display.set_mode(size)
dots = pygame.Surface.copy(screen)

num_routes = len(routes)
tkun_list = [Truck() for i in range(num_routes)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "magenta", "brown", "grey", "white"]

    for index, route in enumerate(routes):
        for p in [route.position for route in route]:
            pygame.draw.circle(dots, colors[index % len(colors)], p, 3.0)
        tkun_list[index].drive_route(route, Map.warehouse, colors[index % len(colors)])

    screen.fill("black")
    for tkun in tkun_list:
        screen.blit(tkun.surf, tkun.surf.get_rect(), special_flags=pygame.BLEND_ADD)
    screen.blit(dots, dots.get_rect(), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()