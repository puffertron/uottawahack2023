#imports
# import basicplot
from algorithms import *

from algorythms import * # TEMPORARY

#constants
RANDOM_DELIVERIES = True
PRESET_DELIVERIES = ["Put house names here"]

#main
# parcels = create_parcels()

# TEMPORARY
size = width, height = 800, 800
parcel_info = create_parcel_info()  
Map.open_street_map_processor(parcel_info, random_points(len(parcel_info) + 10, width, height))
# TEMPORARY

quadtree = construct_quadtree()

assign_destinations(quadtree)