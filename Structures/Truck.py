import pygame
import math

from pygame.math import Vector2

from Structures.Map import Map

class Truck:
    def __init__(self):
        self.color = "purple"
        self.capacity = 5
        self.speed = .01
        self.surf = pygame.Surface(pygame.display.get_window_size())
    
    def drive_route(self, route, start):
        route = self.construct_route([route.position for route in route], start)
        last = start
        for p in route:
            pygame.draw.line(self.surf, self.color, last, p, 2)
            last = p
    
    def construct_route(self, route, start):
        new_route = []
        new_route.append(self.find_greedy_path(route, start))
        while route != []:
            new_route.append(self.find_greedy_path(route, new_route[-1]))
        return new_route
    
    def find_greedy_path(self, route, point):
        smallest_distance = None
        smallest_distance_location = None
        
        for location in route:
            distance = Map.find_distance(point, location)
            if smallest_distance == None or distance < smallest_distance:
                smallest_distance = distance
                smallest_distance_location = location

        route.remove(smallest_distance_location)
        return smallest_distance_location
