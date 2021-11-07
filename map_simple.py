import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, mapping, Point
import numpy as np
import random
import csv
import time
from rdp import rdp
#ramer-douglas-peucker

def cities_and_roads(agent_nums = 1000):
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

        
    minx = min(suwon_x)
    maxx = max(suwon_x)
    miny = min(suwon_y)
    maxy = max(suwon_y)
    print(minx, maxx, miny, maxy)

    people = []

    i = 0
    X=[]
    Y=[]
    X_app = X.append
    Y_app = Y.append
    rand_float = random.uniform
    s_con = suwon_union.contains
    t_1 = 0
    t_2 = 0
    t_3 = 0
    t3 = time.time()
    c = 0
    while i<agent_nums:
        t1 = time.time()
        if i%10000 == 0:
            print(i/5000, t_1, t_2, t_3)
            t_1 = 0
            t_2 = 0
            t_3 = 0
        x = rand_float(minx, maxx)
        y = rand_float(miny, maxy)
        p = Point((x, y))
        t2 = time.time()
        
        t_1+=t2-t1
        
        if s_con(p):
            c = 0
            t_3+=time.time()-t3
            t3 = time.time()
            t_2+=t3-t2
            
            i+=1
            X_app(x)
            Y_app(y)
    
    plt.figure()
    plt.plot(*suwon_union.exterior.xy)
    plt.scatter(X, Y)

    
    
    ax = roads.plot(color='purple', edgecolor='w')
    ax.set_title('roads')
    ax.scatter(X, Y)
    ax.set_axis_off()


    
    plt.show()
    return suwon_union, roads, (X, Y)

if __name__ == "__main__":
    cities_and_roads(1000)
