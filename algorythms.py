import pygame
import random
import sys
import math
import time

from pygame import Vector2

def create_parcel_info() -> list[str]:
    amount = random.randint(100,500)
    parcels = []
    for i in range(amount):
        letter = chr(random.randint(32,126))
        if i > 0:
            name = parcels[i-1][0]
        else:
            name = ""
        name += letter
        parcels.append((name,))
    return parcels

def random_points(amt,width,height) -> list[Vector2]:
    """generate x number of points randomly distributed, returns a list of Vec2"""
    points = []
    for i in range(1, amt):
        vec = Vector2(random.randint(0, width), random.randint(0, height))
        points.append(vec)
    
    return points

def cluster_points(density, c_amt, c_rad, width, height) -> list[Vector2]:
    """generate y number of clusters, containing x number of points within z radius, returns a list of Vec2"""
    clusters = []
    points = []
    for i in range(1, c_amt):
        vec = Vector2(random.randint(0, width), random.randint(0, height))
        clusters.append(vec)
    
    for c in clusters:
        for i in range(density):
            vec = Vector2(random.randint(c.x-c_rad, c.x-c_rad), random.randint(c.y-c_rad, c.y-c_rad))
            points.append(vec)
    
    return points

def spiral_deliver(points: list[Vector2], origin: Vector2) -> list[Vector2]:
    sortedpoints = sort_by_distance(points)
    far = sortedpoints[-1]

    a = origin.angle_to(far)
    last = far

    for p in points:
        t = last.angle_to(p)
        if t < 180:
            pass

def sort_by_distance(points: list[Vector2], origin: Vector2) -> list[Vector2]:
    """sort em by distance, birds eye view"""
    distances = []
    for p in points:
        d = origin.distance_to(p)
        distances.append(d)
    
    #print(points)
    #print (distances)

    zipped = list(zip(distances, points))
    zipped.sort()
    
    distances, sortedpoints, = zip(*zipped)
    #print(sortedpoints)
    #print (distances)

    return sortedpoints
