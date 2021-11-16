import geopandas as gpd

import pandas as pd

import matplotlib.pyplot as plt

from shapely.geometry import Polygon, mapping, Point

import numpy as np

import random

import csv

import time

from rdp import rdp
import math

def move_road(roads, road_num, N, up_down):
    print(N)
    if N == 0:
        return
    X, Y = roads["geometry"][road_num].xy

    if not up_down:
        X.reverse()
        Y.reverse()
    
    speed = 1 * 360/40075000
    left = 0
    for i in range(len(X)-1):
        length = math.sqrt((X[i+1]-X[i])**2 + (Y[i+1]-Y[i])**2)
        angle = math.atan2(Y[i+1] - Y[i], X[i+1] - X[i])
        """
        print("road_line", i, left)
        print("len", length/(360/40075000))
        print("X0", X[i], Y[i])
        print("X1", X[i+1], Y[i+1])
        print("Angle", angle)
        """
        
        pos_x = X[i]+math.cos(angle) * left
        pos_y = Y[i]+math.cos(angle) * left
        past = abs(X[i+1]-X[i])/(X[i+1]-X[i])
        while X[i+1]-pos_x != 0  and past == abs(X[i+1]-pos_x)/(X[i+1]-pos_x):
            pos_x += math.cos(angle) * speed
            pos_y += math.sin(angle) * speed
            #print(pos_x, pos_y, X[i+1]-pos_x)
        left = math.sqrt((X[i+1]-pos_x)**2 + (Y[i+1]-pos_y)**2)


    if up_down:
        print("from", roads["UP_FROM_NO"][road_num])
        print("to", roads["UP_TO_NODE"][road_num])
        print(roads["UP_FROM_NO"][roads["UP_FROM_NO"] == roads["UP_TO_NODE"][road_num]])
        if roads["UP_FROM_NO"][roads["UP_FROM_NO"] == roads["UP_TO_NODE"][road_num]].empty:
            move_road(roads, road_num, N-1, not up_down)
        else:
            move_road(roads, roads["UP_FROM_NO"][roads["UP_FROM_NO"] == roads["UP_TO_NODE"][road_num]].index[0], N-1, up_down)
    elif not up_down:
        print("from", roads["DOWN_FROM_"][road_num])
        print("to", roads["DOWN_TO_NO"][road_num])
        print(roads["DOWN_FROM_"][roads["DOWN_FROM_"] == roads["DOWN_TO_NO"][road_num]])
        if roads["DOWN_FROM_"][roads["DOWN_FROM_"] == roads["DOWN_TO_NO"][road_num]].empty:
            move_road(roads, road_num, N-1, not up_down)
        else:
            move_road(roads, roads["DOWN_FROM_"][roads["DOWN_FROM_"] == roads["DOWN_TO_NO"][road_num]].index[0], N-1, up_down)

def cities_and_roads():
    plt.rcParams["figure.figsize"] = (10, 10)
    
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\suwon_union.csv"
    f = open(file, 'r')
    rdr = csv.reader(f)

    suwon_x = []
    suwon_y = []
    suwon_poly = []
    for pos in rdr:
        suwon_poly.append((float(pos[0]), float(pos[1])))

    suwon_poly = suwon_poly[1:]
    suwon_poly = rdp(suwon_poly, epsilon=0.001)

    for x, y in suwon_poly:
        suwon_x.append(x)
        suwon_y.append(y)
    
    print(len(suwon_poly))
    suwon_union = Polygon(suwon_poly)

    
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\roads"

    roads = gpd.read_file(file)
    roads = roads.to_crs(epsg=4326)
    
    move_road(roads, 3, 10, True)

if __name__ == "__main__":
    cities_and_roads()
