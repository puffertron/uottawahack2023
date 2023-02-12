import pygame

#imports
from algorithms import *
import config
from Structures.Map import Map

from algorythms import * # TEMPORARY

#constants
PRESET_DELIVERIES = create_parcel_info()
OPEN_STREET_MAPS_DATA = random_points(len(PRESET_DELIVERIES) + 10, config.map_width, config.map_height)

#main
initialize_objects(OPEN_STREET_MAPS_DATA, PRESET_DELIVERIES)
quadtree = construct_quadtree()
clusters = assign_clusters(Map.parcels,max((config.map_width,config.map_height)),quadtree)

for parcel in Map.parcels:
    print(parcel.cluster_id)
