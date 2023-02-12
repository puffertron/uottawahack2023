import pygame
import random
import sys
import math
import time

from pygame import Vector2

from Structures.Map import Map
from config import *

def identify_quadrant(quadtree, parcel):
    box_x = math.floor(parcel.position.x / box_width)
    box_y = math.floor(parcel.position.y / box_height)

    # for case when point on right or bottom edge
    try:
        quadtree[box_x][box_y]
    except IndexError:
        if box_x == granularity:
            box_x -= 1
        if box_y == granularity:
            box_y -= 1
    return box_x, box_y

def construct_quadtree():
    quadtree = [[set() for i in range(granularity)] for i in range(granularity)]

    for parcel in Map.parcels:
        box_x, box_y = identify_quadrant(quadtree, parcel)
        quadtree[box_x][box_y].add(parcel)

    return quadtree

# TODO To make more efficient can try to increase view of quad tree one box at a time, instead of one radius at a time
def assign_destinations(quadtree):
    routes = []
    
    while Map.parcels != []:
        for index, parcel in reversed(list(enumerate(Map.parcels))):
            if parcel.assigned:
                del Map.parcels[index]
                continue

            nearby_parcels = []
            
            depth = 0
            box_x, box_y = identify_quadrant(quadtree, parcel)
            boxes = [(quadtree[box_x][box_y], (box_x, box_y))]

            while True:
                for box in boxes:
                    for quad_parcel in box[0]:
                        nearby_parcels.append((quad_parcel, box[1], Map.find_distance(parcel.position, quad_parcel.position)))
                    boxes.remove(box)
                
                if len(nearby_parcels) >= max_parcel_delivery_size:
                    break

                depth += 1
                if depth > granularity:
                    break

                temp_box_x = box_x - depth
                temp_box_y = box_y - depth

                for i in range(depth * 2):
                    if temp_box_x + i >= 0 and temp_box_x + i < granularity and temp_box_y >= 0 and temp_box_y < granularity:
                        boxes.append((quadtree[temp_box_x + i][temp_box_y], (temp_box_x + i, temp_box_y)))
                    if temp_box_x >= 0 and temp_box_x < granularity and temp_box_y + i >= 0 and temp_box_y + i < granularity:
                        boxes.append((quadtree[temp_box_x][temp_box_y + i], (temp_box_x, temp_box_y + i)))
                    if temp_box_x + depth * 2 >= 0 and temp_box_x + depth * 2 < granularity and temp_box_y + i >= 0 and temp_box_y + i < granularity:
                        boxes.append((quadtree[temp_box_x + depth * 2][temp_box_y + i], (temp_box_x + depth * 2, temp_box_y + i)))
                    if temp_box_x + i >= 0 and temp_box_x + i < granularity and temp_box_y + depth * 2 >= 0 and temp_box_y + depth * 2 < granularity:
                        boxes.append((quadtree[temp_box_x + i][temp_box_y + depth * 2], (temp_box_x + i, temp_box_y + depth * 2)))

            nearby_parcels.sort(key=lambda nearby_parcel: nearby_parcel[2])
            nearby_parcels = nearby_parcels[:max_parcel_delivery_size]

            radius = nearby_parcels[-1][2]
            
            route = []
            for nearby_parcel in nearby_parcels:
                nearby_parcel[0].assigned = True
                quadtree[nearby_parcel[1][0]][nearby_parcel[1][1]].discard(nearby_parcel[0])
                route.append(nearby_parcel[0])
            routes.append(route)

        # REMOVE LATER
        for route in routes:
            print("Route: ")
            for parcel in route:
                print(parcel.position.x, parcel.position.y)
            
    return routes

def generate_deliveries():
    pass

def create_parcels():
    pass
