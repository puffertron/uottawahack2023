#imports
import basicplot
from algorithms import *
import config

#constants
PRESET_DELIVERIES = False
OPEN_STREET_MAPS_DATA = None

#main
parcels = initialize_objects(OPEN_STREET_MAPS_DATA, PRESET_DELIVERIES)
assign_clusters(parcels,config.size) #todo fix config name 