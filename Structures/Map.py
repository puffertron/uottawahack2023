import math
from pygame import Vector2
import pygame
from operator import itemgetter

from Structures.Parcel import Parcel

import random


class Map:
    def __init__(self, parcel_info: list[tuple[str,]], points: list[Vector2]):
        self.available_points = points
        self.warehouse = self.name_to_location()

        self.create_parcels(parcel_info)
    
    def name_to_location(self): #real map will use map data to determine this instead of randomizing
        i = random.randint(0,len(self.available_points) - 1)
        return self.available_points.pop(i)
    
    def create_parcels(self, parcel_info: list[tuple[str,]]):
        self.parcels = [] 
        for entry in parcel_info:
            parcel = Parcel(entry[0], self.name_to_location())
            distance = self.find_distance(parcel.position,self.warehouse)
            self.parcels.append((parcel,distance))
        self.parcels = sorted(self.parcels, key=itemgetter(1))

    def find_distance(self, target: Vector2, source: Vector2):
        return (target - source).magnitude()
    

