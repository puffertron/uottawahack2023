import math
from pygame import Vector2
import pygame
from operator import itemgetter

from Structures.Parcel import Parcel

import random

#This is a class that no instances should be made. This is a class to hold make the info of the map and hold the map data.
class Map:
    # The state of the class, just initialized in 'Algorithm'
    available_points:list[Vector2] = []
    warehouse:Vector2 = Vector2(0,0)
    
    
    
    def __init__(parcel_info: list[tuple[str,]], points: list[Vector2]):
        pass
    
    @staticmethod
    def open_street_map_processor(parcel_info: list[tuple[str,]], points: list[Vector2]):
        #This takes in raw data from open street maps and the parcels to be delivered and sorts it into the state of Map. TODO - make it actually take Open Street Map data and parse it (instead of taking in pre-generated points)
        available_points = points
        warehouse = Map.name_to_location()
        
        Map.create_parcels(parcel_info)
    
    @staticmethod
    def name_to_location(): #real map will use map data to determine this instead of randomizing
        i = random.randint(0,len(Map.available_points) - 1)
        return Map.available_points.pop(i)
    
    @staticmethod
    def create_parcels(parcel_info: list[tuple[str,]]):
        parcels = [] 
        for entry in parcel_info:
            parcel = Parcel(entry[0], Map.name_to_location())
            distance = Map.find_distance(parcel.position,Map.warehouse)
            Map.parcels.append((parcel,distance))
        Map.parcels = sorted(parcels, key=itemgetter(1))

    @staticmethod
    def find_distance(target: Vector2, source: Vector2):
        return (target - source).magnitude()
    

