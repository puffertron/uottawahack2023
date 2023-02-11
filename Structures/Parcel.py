import math
from pygame import Vector2
import pygame

class Parcel:
    def __init__(self, destination: Vector2, weight: float):
        self.destination = destination
        self.weight = weight

