import pygame
import random
import sys
import math
import time

from pygame import Vector2

from Structures.Map import Map

def spiral_deliver(points: list[Vector2], origin: Vector2) -> list[Vector2]:
    sortedpoints = sort_by_distance(points)
    far = sortedpoints[-1]

    a = origin.angle_to(far)
    last = far

    for p in points:
        t = last.angle_to(p)
        if t < 180:
            pass

def sort_by_distance(points: list[Vector2], origin: Vector2) -> list[Vector2]:
    """sort em by distance, birds eye view"""
    distances = []
    for p in points:
        d = origin.distance_to(p)
        distances.append(d)
    
    print(points)
    print (distances)

    zipped = list(zip(distances, points))
    zipped.sort()
    
    distances, sortedpoints, = zip(*zipped)
    print(sortedpoints)
    print (distances)

    return sortedpoints

def construct_quadtree():
    leftmost_x = rightmost_x = Map.buildings[0].position.x
    topmost_y = bottommost_y = Map.buildings[0].position.y

    for building in Map.buildings:
        if building.position.x < leftmost_x:
            leftmost_x = building.position.x
        elif building.position.x > rightmost_x:
            rightmost_x = building.position.x
        elif building.position.y < topmost_y:
            topmost_y = building.position.y
        elif building.position.y > bottommost_y:
            bottommost_y = building.position.y

    box_width = (rightmost_x - leftmost_x) / 10     # use constant from config.py
    box_height = (bottommost_y - topmost_y) / 10    # use constant from config.py

    quadtree = [[[] for i in range(10)] for i in range(10)]     # use constant from config.py

    # will error for rightmost_x and bottommost_y
    for building in Map.buildings:
        x = math.floor((building.position.x - leftmost_x) / box_width)
        y = math.floor((building.position.y - topmost_y) / box_height)
        quadtree[x][y].append(building)

    return leftmost_x, topmost_y, box_width, box_height, quadtree

def assign_destinations():
    for building in Map.buildings[::-1]:
        if building.assigned:
            # delete building from Map.buildings (maybe iterate by index instead of by value)
            pass
        else:
            pass
