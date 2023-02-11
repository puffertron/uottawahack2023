import pygame
import random
import sys
import math
import time

from pygame import Vector2

def spiral_deliver(points: list[Vector2], origin: Vector2):
    sortedpoints = sort_by_distance(points)
    far = sortedpoints[-1]

    a = origin.angle_to(far)
    last = far

    for p in points:
        t = last.angle_to(p)
        if t < 180:
            


def sort_by_distance(points: list[Vector2], origin: Vector2):
    distances = []
    for p in points:
        d = origin.distance_to(p)
        distances.append(d)
    
    print(points)
    print (distances)

    zipped = list(zip(distances, points))
    zipped.sort()
    
    distances, sortedpoints, = zip(*zipped)
    print(sortedpoints)
    print (distances)

    return sortedpoints