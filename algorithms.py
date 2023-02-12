import pygame
import random
import sys
import math
import time

from pygame import Vector2

from Structures.Map import Map
from Structures.Parcel import Parcel
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

# Initialization
def initialize_objects(raw_data, preset_deliveries: bool | list[str]) -> list[Parcel]:
    deliveries = generate_deliveries(preset_deliveries)
    parcels: list[Parcel] = Map.set_up_state(deliveries, raw_data) #todo make this correct
    return parcels

def generate_deliveries(preset_deliveries: bool | list[str]) -> list[str]:
    if not preset_deliveries:
        pass #todo randomly generate deliveries
    else:
        return preset_deliveries
    

# Cluster Assignment
def assign_clusters(parcels: list[Parcel], size: int) -> dict[str, list[Parcel]]:
    cluster_radius = get_cluster_radius(size)
    clusters: dict[str, list[Parcel]] = {}

    parcels_to_check = set(parcels)
    for origin in parcels_to_check:
        cluster = {origin.name: [origin]}
        for source in cluster[origin.name]:
            near_parcels = get_parcel_neighbourhood(source) #note: near_parcels should be sorted closest to farthest!
            for (target, distance) in near_parcels:
                if (distance <= cluster_radius) and (target not in cluster[origin.name]):
                  target.cluster_id = origin.name
                  cluster[origin.name].append(target)
                  parcels_to_check.remove(target)
                else:
                  break
        if len(cluster[origin.name]) > 1:
            clusters.update(cluster)
        parcels_to_check.remove(origin)

    return clusters

def get_cluster_radius(distance: float) -> float:
    pass #todo some operation to decide

def get_parcel_neighbourhood(parcel: Parcel) -> list[tuple[Parcel, float]]: #note: near_parcels should be sorted closest to farthest!
    #todo use quadtrees to give a short list of parcels to check along with associated distance using Map.find_distance() function
    #also sort the list by proximity to source parcel
    pass 