import geopandas as gpd

import pandas as pd

import matplotlib.pyplot as plt

from shapely.geometry import Polygon, mapping, Point

import numpy as np

import random

import csv

def roads():
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["figure.figsize"] = (10, 10)
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\Z_KAIS_TL_SPBD_EQB_경기"

    roads = gpd.read_file(file)

    ax = roads.convex_hull.plot(color='purple', edgecolor='w')
    ax.set_title('test')
    ax.set_axis_off()
    plt.show()


def cities():
    plt.rcParams["figure.figsize"] = (10, 10)
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MA-BA 행정경계(2019년 기준)_세계\\2020-TM-GR-MA-BA 행정경계(2019년기준_세계좌표)"

    cities = gpd.read_file(file)
    cities = cities.to_crs(epsg=4326)
    suwon = cities.loc[cities.DISTRICT_N.str.contains('수원시'), 'geometry']
    suwon_union = suwon.unary_union


    block = mapping(suwon_union)
    pos = block['coordinates'][0][:-1]
    
    df = pd.DataFrame(pos) ## 데이터프래임 생성
    df.to_csv('suwon_union.csv',index=False)


    #ax = suwon.convex_hull.plot(color='purple', edgecolor='w')

    ax = gpd.GeoSeries(suwon.unary_union).plot(color='purple', edgecolor='w')

    ax.set_title('test')

    plt.show()
    return suwon

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

    for x, y in suwon_poly:
        suwon_x.append(x)
        suwon_y.append(y)
    
    print(len(suwon_poly))
    suwon_union = Polygon(suwon_poly)

    """
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MA-BA 행정경계(2019년 기준)_세계\\2020-TM-GR-MA-BA 행정경계(2019년기준_세계좌표)"

    cities = gpd.read_file(file)
    cities = cities.to_crs(epsg=4326)
    suwon = cities.loc[cities.DISTRICT_N.str.contains('수원시'), 'geometry']
    suwon_union = suwon.unary_union
    """

    
    """
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MR-LLV2 도로망(2019년 기준)_세계\\2020-TM-GR-MR-LLV2 도로망(2019년 기준)\\02. 링크"
    roads = gpd.read_file(file)
    roads = roads.to_crs(epsg=4326)
    roads_suwon = roads[roads.within(suwon_union)]
    roads_suwon.to_file('C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\roads_suwon.shp', driver='ESRI Shapefile')

    """


    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\roads"

    roads = gpd.read_file(file)
    roads_suwon = roads.to_crs(epsg=4326)
    
    file_node = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MR-LLV2 도로망(2019년 기준)_세계\\2020-TM-GR-MR-LLV2 도로망(2019년 기준)\\01. 노드"
    file_rotatate = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MR-LLV2 도로망(2019년 기준)_세계\\2020-TM-GR-MR-LLV2 도로망(2019년 기준)\\03. 회전정보"


    roads_node = gpd.read_file(file_node)
    roads_node = roads_node.to_crs(epsg=4326)
    roads_node_suwon = roads_node[roads_node.within(suwon_union)]
    roads_node_suwon.to_file('C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\nodes\\roads_node_suwon.shp', driver='ESRI Shapefile')
    print(file_node)
    roads_rotatate = gpd.read_file(file_rotatate)
    roads_rotatate = roads_rotatate.to_crs(epsg=4326)
    roads_rotatate_suwon = roads_rotatate[roads_rotatate.within(suwon_union)]
    roads_rotatate_suwon.to_file('C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\mapview\\rotates\\roads_rotatate_suwon.shp', driver='ESRI Shapefile')
    print(file_rotatate)


    block = mapping(suwon_union)
    pos = block['coordinates'][0][:-1]
    
    df = pd.DataFrame(pos) ## 데이터프래임 생성
    df.to_csv('suwon_union.csv',index=False)

    """
    ax = plt.subplot(1, 2, 1)
    x, y = suwon.exterior.xy
    plt.plot(x, y, color='purple', ax=ax)
    ax.set_title('suwon')
    ax.set_axis_off()
    """
    """
    ax = plt.subplot(1, 2, 1)
    roads_suwon.plot(color='purple', edgecolor='w', ax=ax)
    """

    
    
    ax = roads_suwon.plot(color='purple', edgecolor='w')
    ax.set_title('roads')
    ax.set_axis_off()

    ay = roads_node_suwon.plot(color='purple', edgecolor='w')
    ay.set_title('nodes')
    ay.set_axis_off()

    az = roads_rotatate_suwon.plot(color='purple', edgecolor='w')
    az.set_title('rotate')
    az.set_axis_off()


    
    plt.show()
    return roads_suwon

if __name__ == "__main__":
    cities_and_roads()
