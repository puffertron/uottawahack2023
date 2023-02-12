import math
from pygame import Vector2
import pygame
from operator import itemgetter

from Structures.Parcel import Parcel
from StreetMap import Road

import random

#This is a class that no instances should be made. This is a class to hold make the info of the map and hold the map data.
class Map:

    # The state of the class, just initialized in 'Algorithm'
    available_points:list[Vector2] = []
    warehouse:Vector2 = Vector2(0,0)
    parcels:list[Parcel] = [] # order closest to warehouse to farthest
    
    
    
    def __init__(parcel_info: list[tuple[str,]], points: list[Vector2]):
        pass
    
    @staticmethod
    def set_up_state(parcel_info: list[tuple[str,]], points: list[Vector2]):
        #This takes in raw data from open street maps and the parcels to be delivered and sorts it into the state of Map. TODO - make it actually take Open Street Map data and parse it (instead of taking in pre-generated points)
        Map.available_points = points
        Map.warehouse = Map.name_to_location()
        
        Map.create_parcels(parcel_info)
    
    @staticmethod
    def name_to_location(): #real map will use map data to determine this instead of randomizing
        i = random.randint(0,len(Map.available_points) - 1)
        return Map.available_points.pop(i)
    
    @staticmethod
    def create_parcels(parcel_info: list[tuple[str,]]):
        parcel_dist_pairs = []
        for entry in parcel_info:
            parcel = Parcel(entry[0], Map.name_to_location())
            distance = Map.find_distance(parcel.position,Map.warehouse)
            parcel_dist_pairs.append((parcel,distance))
        Map.parcels = [parcel_dist_pair[0] for parcel_dist_pair in sorted(parcel_dist_pairs, key=itemgetter(1))]

    @staticmethod
    def find_distance(target: Vector2, source: Vector2): #TODO - this function isn't written yet, need to turn sudo code into actual code
        travel_attempts:list[tuple[list[Road]], Road, float] = [] #First element is roads taken, second is current road, third is distance until end of road
        output = tuple[float, list[Road]] = (0,[])

        running = True
        distance_since_last_iter:int = 0
        splitting_point:Vector2 = Vector2(0,0)

        #Set travel_attempts to all roads with edge at source

        while running:
            #find next closest junction
            #splitting_point = 

            #if reached end, set output to winner(fix output) and set running = False

            #distance_since_last_iter = splitting_point... stuff

            #iterate through travel_attempts and update distances
            #Check if distance is less than 0, if yes throw an error (TODO - make this work, but rare case so shouldn't be an issue)

            #Deal with splitting point by adding new travel attempts to travel_attempts
            #iterate through junctions at splitting point (road. start or end connections)
            #for each junction, add current road to it's list, change road and float, add to travel_attempts
            #after for loop, remove splitting point travel attempt



        return output
