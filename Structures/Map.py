import math
from pygame import Vector2
import pygame

from Structures.Parcel import Parcel

import random


class Map:
    def __init__(self, parcel_info: list[tuple[str,]], warehouse_name: str, size: tuple[int,int], points: list[Vector2]):
        self.warehouse = self.name_to_location(warehouse_name)
        self.size = self.width, self.height = size
        self.available_points = points

        self.create_parcels(self, parcel_info)
    
    def name_to_location(self, name: str): #real map will use map data to determine this instead of randomizing
        i = random.randint(0,len(self.available_points) - 1)
        return self.available_points.pop(i)
    
    def create_parcels(self, parcel_info: list[tuple[str,]]):
        self.parcels = []
        for entry in parcel_info:
            parcel = Parcel(entry[0], self.name_to_location(entry[0]))
            distance = self.find_distance(parcel.position,self.warehouse)
            self.parcels.append((parcel,distance))

    def find_distance(target: Vector2, source: Vector2):
        return (target - source).magnitude
    

