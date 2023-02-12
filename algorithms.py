import pygame
import random
import sys
import math
import time

from pygame import Vector2

from Structures.Map import Map
from config import *

def construct_quadtree():
    quadtree = [[{} for i in range(granularity)] for i in range(granularity)]

    leftmost_x = map_center_x - map_radius # TODO Make sure coordinates match, is top left (0,0)?
    topmost_y = map_center_y - map_radius

    # TODO replace buildings with parcels
    for parcel in Map.parcels:
        box_x = math.floor((parcel.position.x - leftmost_x) / box_width)
        box_y = math.floor((parcel.position.y - topmost_y) / box_height)
        
        # for case when point on right or bottom edge
        try:
            quadtree[box_x][box_y].add(parcel)
        except IndexError:
            if box_x == map_center_x + map_radius: # TODO Replace map_radius
                box_x -= 1
            if box_y == map_center_y + map_radius:
                box_y -= 1
            quadtree[box_x][box_y].add(parcel)

    return quadtree

def assign_destinations():
    for index, parcel in reversed(list(enumerate(Map.parcels))):
        if parcel.assigned:
            del Map.parcel[index]
        else:
            # continue
            pass

def generate_deliveries():
    pass

def create_parcels():
    pass
