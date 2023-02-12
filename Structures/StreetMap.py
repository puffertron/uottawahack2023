import math
from pygame import Vector2
import pygame
import overpy

from Structures.Street import Street

class StreetMap:
    def __init__(self) -> None:
        self.streets = []
    
    def generate_map(density):

