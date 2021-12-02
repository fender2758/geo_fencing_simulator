import geopandas as gpd

import pandas as pd

import matplotlib.pyplot as plt

from shapely.geometry import Polygon, LineString, Point

import numpy as np

import random

import csv

import time

from rdp import rdp
import math

from astar import astar_road

import os
from pathlib import Path

ROOT = os.getcwd()
ROOT = Path(__file__).parents[1]

def move_by_node(roads, nodes, initial, initial_f, final, final_f):

    X, Y = roads["geometry"][nodes[1]["index"]].xy

    # Down으로 이동중이면 뒤집기
    if roads["UP_FROM_NO"][nodes[1]["index"]] == nodes[1]["node"]:
        X.reverse()
        Y.reverse()
    init_line = None
    for i in range(len(X) - 1):
        if abs((initial_f[1]-Y[i])/(initial_f[0]-X[i]) - (initial_f[1]-Y[i+1])/(initial_f[0]-X[i+1])) < 0.0000001:
            temp_x = [initial_f[0]]
            temp_y = [initial_f[1]]
            temp_x.extend(X[i+1:])
            temp_y.extend(Y[i+1:])
            init_line = LineString([[temp_x[k], temp_y[k]] for k in range(len(temp_x))])
            break
    line = [LineString([initial, initial_f]), init_line]

    for road in nodes[2:-1]:
        line.append(roads["geometry"][road["index"]])
        X, Y = roads["geometry"][road["index"]].xy

        # Down으로 이동중이면 뒤집기
        if roads["UP_FROM_NO"][road["index"]] == road["node"]:
            X.reverse()
            Y.reverse()

        # 속도는 1m/단위 실행
        speed = 1 * 360 / 40075000

        left = 0
        for i in range(len(X) - 1):
            # 도로의 Linestring을 이동중에 일정 각도로 이동
            angle = math.atan2(Y[i + 1] - Y[i], X[i + 1] - X[i])

            pos_x = X[i] + math.cos(angle) * left
            pos_y = Y[i] + math.cos(angle) * left
            past = abs(X[i + 1] - X[i]) / (X[i + 1] - X[i])
            # Linestring의 단위 직선 이동, 직선을 벗어나면 종료
            while X[i + 1] - pos_x != 0 and past == abs(X[i + 1] - pos_x) / (X[i + 1] - pos_x):
                pos_x += math.cos(angle) * speed
                pos_y += math.sin(angle) * speed
                # 위치 출력문, 후에 cvs로 저장 등 활용 가능
                # print(pos_x, pos_y, X[i+1]-pos_x)
            # 단위 시간당 이동 거리 중 직선 이동 후 남은 거리
            left = math.sqrt((X[i + 1] - pos_x) ** 2 + (Y[i + 1] - pos_y) ** 2)

    X, Y = roads["geometry"][nodes[-1]["index"]].xy

    # Down으로 이동중이면 뒤집기
    if roads["UP_FROM_NO"][nodes[-1]["index"]] == nodes[-1]["node"]:
        X.reverse()
        Y.reverse()

    final_line = None
    for i in range(len(X) - 1):
        if final_f[0] == X[i] or final_f[0] == X[i+1] or abs((final_f[1] - Y[i]) / (final_f[0] - X[i]) - (final_f[1] - Y[i + 1]) / (
                final_f[0] - X[i + 1])) < 0.0000001:
            temp_x = [final_f[0]]
            temp_y = [final_f[1]]
            temp_x.extend(X[:i+1])
            temp_y.extend(Y[:i+1])
            final_line = LineString([[temp_x[k], temp_y[k]] for k in range(len(temp_x))])
            break
    line.append(final_line)
    line.append(LineString([final, final_f]))

    return line


def line_point(p, a, b):
    P = (p[0], p[1])
    A = (a[0], a[1])
    B = (b[0], b[1])

    area = abs((A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0]))
    AB = ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5
    h = (area / AB)
    l1 = ((P[0] - A[0]) ** 2 + (P[1] - A[1]) ** 2) ** 0.5
    l2 = ((P[0] - B[0]) ** 2 + (P[1] - B[1]) ** 2) ** 0.5
    return h, l1, l2


def scan_road(pos, roads, set_range):
    X, Y = pos
    scan_range = set_range * 360 / 40075000
    scan = Polygon(
        (X + math.cos(x) * scan_range, Y + math.sin(x) * scan_range) for x in np.arange(-1 * np.pi, np.pi, np.pi / 4))

    line_roads = roads[roads.intersects(scan)]

    if len(line_roads["geometry"]) == 0:
        line_roads, set_range = scan_road(pos, roads, set_range + 100)

    return line_roads, set_range


def scan_node(pos, roads, scan_range):
    X, Y = pos

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.set_aspect('equal')

    line_roads, scan_range = scan_road(pos, roads, scan_range)
    min_dis = scan_range
    link_id = 0
    up_down = True
    target_pos = (0, 0)

    for i in line_roads['geometry'].index:
        X_l, Y_l = line_roads['geometry'][i].xy
        for j in range(len(X_l) - 1):
            # ax.scatter(X_l[j], Y_l[j], c='blue')
            h, l1, l2 = line_point(pos, (X_l[j], Y_l[j]), (X_l[j + 1], Y_l[j + 1]))
            dis = min((h, l1, l2))
            if dis < min_dis:
                if dis == h:
                    u = np.array([X - X_l[j], Y - Y_l[j]])
                    v = np.array([X_l[j + 1] - X_l[j], Y_l[j + 1] - Y_l[j]])

                    v_norm = np.sqrt(sum(v ** 2))
                    if abs(np.dot(u, v) / v_norm) > v_norm:
                        dis = min((l1, l2))
                        if dis > min_dis:
                            continue
                    else:
                        up_down = l1 < l2
                        proj_of_u_on_v = (np.dot(u, v) / v_norm ** 2) * v + np.array([X_l[j], Y_l[j]])

                        target_pos = tuple(proj_of_u_on_v)

                if dis == l1:
                    up_down = True
                    target_pos = (X_l[j], Y_l[j])

                elif dis == l2:
                    up_down = False
                    target_pos = (X_l[j + 1], Y_l[j + 1])

                min_dis = dis
                link_id = i

    for l in line_roads['geometry']:
        X, Y = l.xy
        # ax.plot(X, Y)

    # ax.scatter([pos[0]], [pos[1]], c='blue')
    # ax.scatter([target_pos[0]], [target_pos[1]], c='red')
    # print(link_id, target_pos, scan_range)

    return link_id, target_pos, up_down


def Astar(roads, initial, final):
    link_id, target_pos, up_down = scan_node(initial, roads, 100)
    link_id_f, target_pos_f, up_down_f = scan_node(final, roads, 100)
    pos = astar_road(roads, target_pos, link_id, target_pos_f, link_id_f)
    
    line = move_by_node(roads, pos, initial, target_pos, final, target_pos_f)

    # 출력
    fig = plt.figure()
    ax = roads.plot(color='purple', edgecolor='w')
    ax.set_aspect('equal')
    for l in line:
        X, Y = l.xy
        ax.plot(X, Y, linewidth=3.0, color='red')

    plt.show()


def suwon_move():
    plt.rcParams["figure.figsize"] = (10, 10)

    # 수원 외곽
    file = os.path.join(ROOT, "suwon\suwon_union.csv")
    f = open(file, 'r')
    rdr = csv.reader(f)

    suwon_poly = []
    for pos in rdr:
        suwon_poly.append((float(pos[0]), float(pos[1])))

    suwon_poly = suwon_poly[1:]
    suwon_poly = rdp(suwon_poly, epsilon=0.001)

    print("Loaded Map...")
    suwon_union = Polygon(suwon_poly)

    # 수원 도로
    file = os.path.join(ROOT, "roads")

    roads = gpd.read_file(file)
    roads = roads.to_crs(epsg=4326)
    print("Loaded Roads...")
    Astar(roads, (126.975, 37.3), (126.985, 37.3))

    plt.show()


if __name__ == "__main__":
    suwon_move()
