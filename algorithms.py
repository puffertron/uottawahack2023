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
def assign_destinations(quadtree, clusters):
    quadtree_copy = []
    for x in range(granularity):
        quadtree_copy.append([])
        for y in range(granularity):
            quadtree_copy[x].append(quadtree[x][y].copy())
    
    routes = []
    
    while Map.parcels != []:
        for index, parcel in reversed(list(enumerate(Map.parcels))):
            if parcel.assigned:
                del Map.parcels[index]
            else:
                routes += assign_destinations_route(quadtree_copy, clusters, [], parcel)

        # REMOVE LATER
        for route in routes:
            print("Route: " + str(len(route)))
            for parcel in route:
                print(parcel.position.x, parcel.position.y)
            
    return routes

def unparcel_boxes(boxes, parcel):
    nearby_parcels = []
    for box in boxes:
        for quad_parcel in box[0]:
            if (quad_parcel.cluster_id):
                return False, quad_parcel
            nearby_parcels.append((quad_parcel, box[1], Map.find_distance(parcel.position, quad_parcel.position)))
    return True, nearby_parcels

def assign_destinations_route(quadtree_copy, clusters, nearby_parcels, parcel):
    saved_parcels = []
    routes = []
    
    box_x, box_y = identify_quadrant(quadtree_copy, parcel)
    boxes = [(quadtree_copy[box_x][box_y], (box_x, box_y))]
    depth = 0
    
    while True:
        unboxed, unboxed_parcels = unparcel_boxes(boxes, parcel)
        if unboxed:
            nearby_parcels += unboxed_parcels
        else:
            saved_parcels = nearby_parcels.copy()
            nearby_parcels = []
            
            clustered_parcels = clusters[unboxed_parcels.cluster_id]
            
            for saved_parcel in (saved_parcels + clustered_parcels):
                saved_parcel[0].assigned = True
                quadtree_copy[saved_parcel[1][0]][saved_parcel[1][1]].discard(saved_parcel[0])
            
            routes += assign_destinations_route(quadtree_copy, clusters, clustered_parcels, unboxed_parcels)
            depth -= 1
        boxes = []
        
        if len(saved_parcels) + len(nearby_parcels) >= max_parcel_delivery_size:
            break

        depth += 1
        if depth > granularity * 2:
            break

        temp_box_x = box_x - depth
        temp_box_y = box_y - depth

        for i in range(depth * 2):
            if temp_box_x + i >= 0 and temp_box_x + i < granularity and temp_box_y >= 0 and temp_box_y < granularity:
                boxes.append((quadtree_copy[temp_box_x + i][temp_box_y], (temp_box_x + i, temp_box_y)))
            if temp_box_x >= 0 and temp_box_x < granularity and temp_box_y + i >= 0 and temp_box_y + i < granularity:
                boxes.append((quadtree_copy[temp_box_x][temp_box_y + i], (temp_box_x, temp_box_y + i)))
            if temp_box_x + depth * 2 >= 0 and temp_box_x + depth * 2 < granularity and temp_box_y + i >= 0 and temp_box_y + i < granularity:
                boxes.append((quadtree_copy[temp_box_x + depth * 2][temp_box_y + i], (temp_box_x + depth * 2, temp_box_y + i)))
            if temp_box_x + i >= 0 and temp_box_x + i < granularity and temp_box_y + depth * 2 >= 0 and temp_box_y + depth * 2 < granularity:
                boxes.append((quadtree_copy[temp_box_x + i][temp_box_y + depth * 2], (temp_box_x + i, temp_box_y + depth * 2)))

    expansion_depth = [depth, depth, depth, depth]
    expansion_dist = [
        parcel.position.x - box_x,
        parcel.position.y - box_y,
        box_x + box_width - parcel.position.x,
        box_y + box_height - parcel.position.y
    ]
    
    while True:
        nearby_parcels.sort(key=lambda nearby_parcel: nearby_parcel[2])
        nearby_parcels = nearby_parcels[:(max_parcel_delivery_size - len(saved_parcels))]

        radius = nearby_parcels[-1][2]
        
        if expansion_dist[0] + expansion_depth[0] * box_width > radius:
            expansion_depth[0] += 1
            for i in range(depth * 2):
                if box_x - expansion_depth[0] >= 0 and box_x - expansion_depth[0] < granularity and box_y + i >= 0 and box_y + i < granularity:
                    boxes.append((quadtree_copy[box_x - expansion_depth[0]][box_y + i], (box_x - expansion_depth[0], box_y + i)))
        if expansion_dist[1] + expansion_depth[1] * box_height > radius:
            expansion_depth[1] += 1
            for i in range(depth * 2):
                if box_x + i >= 0 and box_x + i < granularity and box_y - expansion_depth[1] >= 0 and box_y - expansion_depth[1] < granularity:
                    boxes.append((quadtree_copy[box_x + i][box_y - expansion_depth[1]], (box_x + i, box_y - expansion_depth[1])))
        if expansion_dist[2] + expansion_depth[2] * box_width > radius:
            expansion_depth[2] += 1
            for i in range(depth * 2):
                if box_x + expansion_depth[2] >= 0 and box_x + expansion_depth[2] < granularity and box_y + i >= 0 and box_y + i < granularity:
                    boxes.append((quadtree_copy[box_x + expansion_depth[2]][box_y + i], (box_x + expansion_depth[2], box_y + i)))
        if expansion_dist[3] + expansion_depth[3] * box_height > radius:
            expansion_depth[3] += 1
            for i in range(depth * 2):
                if box_x + i >= 0 and box_x + i < granularity and box_y + expansion_depth[3] >= 0 and box_y + expansion_depth[3] < granularity:
                    boxes.append((quadtree_copy[box_x + i][box_y + expansion_depth[3]], (box_x + i, box_y + expansion_depth[3])))

        if boxes == []:
            break
        
        for box in boxes:
            for quad_parcel in box[0]:
                nearby_parcels.append((quad_parcel, box[1], Map.find_distance(parcel.position, quad_parcel.position)))
            boxes.remove(box)
    
    for nearby_parcel in nearby_parcels:
        nearby_parcel[0].assigned = True
        quadtree_copy[nearby_parcel[1][0]][nearby_parcel[1][1]].discard(nearby_parcel[0])

    routes.append([nearby_parcel[0] for nearby_parcel in (nearby_parcels + saved_parcels)])

    return routes

def generate_deliveries():
    pass

def create_parcels():
    pass
