#imports
# import basicplot
from algorithms import *
import config

from algorythms import * # TEMPORARY

#constants
PRESET_DELIVERIES = False
OPEN_STREET_MAPS_DATA = None

#main

# TEMPORARY
# size = width, height = 800, 800
# parcel_info = create_parcel_info()  
# Map.open_street_map_processor(parcel_info, random_points(len(parcel_info) + 10, width, height))
# quadtree = construct_quadtree()
# assign_destinations(quadtree)
# TEMPORARY

parcels = initialize_objects(OPEN_STREET_MAPS_DATA, PRESET_DELIVERIES)
clusters = assign_clusters(parcels,config.map_radius)
