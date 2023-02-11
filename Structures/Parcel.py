import math
from pygame import Vector2
import pygame

class Parcel:
    def __init__(self, name: str, position: Vector2):
        self.name = name
        self.position = position
        self.cluster_id = None
        self.assigned = False