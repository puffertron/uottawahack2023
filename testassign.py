import pygame

from algorithms import *
from algorythms import *

size = width, height = 800, 800
parcel_info = create_parcel_info()  
Map.open_street_map_processor(parcel_info, random_points(len(parcel_info) + 10, width, height))

quadtree = construct_quadtree()
routes = assign_destinations(quadtree, {})

pygame.init()
screen = pygame.display.set_mode(size)
dots = pygame.Surface.copy(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "magenta", "brown", "grey", "white"]

    for index, route in enumerate(routes):
        for p in [route.position for route in route]:
            pygame.draw.circle(dots, colors[index % len(colors)], p, 3.0)

    screen.fill("black")
    screen.blit(dots, dots.get_rect(), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()