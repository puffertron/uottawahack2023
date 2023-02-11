import math
from pygame import Vector2
import pygame


class Map:
    pass

class Street:
    def get_length(self):
        pass
    

class Building:
    def __init__(self, position: Vector2):
        self.position = position
        self.address = "123 placeholder st"

class Parcel:
    def __init__(self, destination: Vector2, weight: float):
        self.destination = destination
        self.weight = weight

