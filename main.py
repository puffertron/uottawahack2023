import pygame

#imports
from algorithms import *
import config
from Structures.Map import Map
from Structures.StreetMap import StreetMap

from algorythms import * # TEMPORARY

#constants
PRESET_DELIVERIES = create_parcel_info()
OPEN_STREET_MAPS_DATA = random_points(len(PRESET_DELIVERIES) + 10, config.map_width, config.map_height)

#main
initialize_objects(OPEN_STREET_MAPS_DATA, PRESET_DELIVERIES)
quadtree = construct_quadtree()
clusters = assign_clusters(Map.parcels,max((config.map_width,config.map_height)),quadtree)

stmap = StreetMap()
s,x = stmap.initialise_road_segments()
roads = stmap.merge_segments(s, x)
stmap.populate_linked_list_network(roads)

for parcel in Map.parcels:
    print(parcel.cluster_id)
