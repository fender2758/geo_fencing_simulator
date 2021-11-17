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
    #도로 정보, 현재 도로 인덱스, 남은 도로 개수, 위/아래 이동 여부
    print(road_num)
    #종료
    if N == 0:
        return []
    
    #현재 도로의 LineString
    line = [roads["geometry"][road_num]]

    
    X, Y = roads["geometry"][road_num].xy
    
    #Down으로 이동중이면 뒤집기
    if not up_down:
        X.reverse()
        Y.reverse()
        
    #속도는 1m/단위 실행
    speed = 1 * 360/40075000
    
    left = 0
    for i in range(len(X)-1):
        # 도로의 Linestring을 이동중에 일정 각도로 이동
        angle = math.atan2(Y[i+1] - Y[i], X[i+1] - X[i])
        
        pos_x = X[i]+math.cos(angle) * left
        pos_y = Y[i]+math.cos(angle) * left
        past = abs(X[i+1]-X[i])/(X[i+1]-X[i])
        #Linestring의 단위 직선 이동, 직선을 벗어나면 종료
        while X[i+1]-pos_x != 0  and past == abs(X[i+1]-pos_x)/(X[i+1]-pos_x):
            pos_x += math.cos(angle) * speed
            pos_y += math.sin(angle) * speed
            #위치 출력문, 후에 cvs로 저장 등 활용 가능
            #print(pos_x, pos_y, X[i+1]-pos_x)
        #단위 시간당 이동 거리 중 직선 이동 후 남은 거리
        left = math.sqrt((X[i+1]-pos_x)**2 + (Y[i+1]-pos_y)**2)

    #도로 정보에서 인덱스 기준으로 도로의 시작/끝 노드를 up/down 기준으로 알 수 있음
    if up_down:
        print("from", roads["UP_FROM_NO"][road_num], end = "")
        print("to", roads["UP_TO_NODE"][road_num])
        start_n = roads["UP_FROM_NO"][road_num]
        end_n = roads["UP_TO_NODE"][road_num]
    else:
        print("from", roads["DOWN_FROM_"][road_num], end = "")
        print("to", roads["DOWN_TO_NO"][road_num])
        start_n = roads["DOWN_FROM_"][road_num]
        end_n = roads["DOWN_TO_NO"][road_num]

    #끝 노드를 시작점으로 잡는 도로의 인덱스를 지정, 자기 자신 제외
    up_ser = roads["UP_FROM_NO"][roads["UP_FROM_NO"] == end_n]
    down_ser = roads["DOWN_FROM_"][roads["DOWN_FROM_"] == end_n]
    
    if True in up_ser.index.isin([road_num]):
        del up_ser[road_num]
    if True in down_ser.index.isin([road_num]):
        del down_ser[road_num]
            
    #우선 up 방향을 우선적으로 이동
    if not up_ser.empty:
        line.extend(move_road(roads, up_ser.index[0], N-1, True))
    
    if not down_ser.empty:
        line.extend(move_road(roads, down_ser.index[0], N-1, False))
        
    #다음 진행 도로가 없으면 회귀
    else:
        print("GO BACK")
        if up_down:
            line.extend(move_road(roads, road_num, N-1, not up_down))
        else:
            line.extend(move_road(roads, road_num, N-1, not up_down))

            
    return line

def suwon_move():
    plt.rcParams["figure.figsize"] = (10, 10)

    #수원 외곽
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\suwon_union.csv"
    f = open(file, 'r')
    rdr = csv.reader(f)

    suwon_poly = []
    for pos in rdr:
        suwon_poly.append((float(pos[0]), float(pos[1])))

    suwon_poly = suwon_poly[1:]
    suwon_poly = rdp(suwon_poly, epsilon=0.001)
    
    print(len(suwon_poly))
    suwon_union = Polygon(suwon_poly)

    #수원 도로
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\roads"

    roads = gpd.read_file(file)
    roads = roads.to_crs(epsg=4326)


    #0번 인덱스의 도로에서 5번 up 방향으로 이동
    line = move_road(roads, 0, 5, True)
    
    #출력
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    for l in line:
        X, Y = l.xy
        ax.plot(X, Y)
    plt.show()
    

if __name__ == "__main__":
    suwon_move()
