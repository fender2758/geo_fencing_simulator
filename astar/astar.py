from shapely.geometry import Polygon, mapping, Point
from shapely.geometry import LineString

# Time complexityity는 H에 따라 다르다.
# O(b^d), where d = depth, b = 각 노드의 하위 요소 수
# heapque를 이용하면 길을 출력할 때 reverse를 안해도 됨
from PIL import Image
import numpy as np
import turtle
import pandas as pd
import time
import sys


class Node:
    def __init__(self, parent=None, position=None, road_node=None, road_index=None):
        self.parent = parent
        self.position = position
        self.road_node = road_node
        self.road_index = road_index

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        # if self.position == other.position
        return self.position == other.position


def heuristic(node, goal, D=1, D2=2 ** 0.5):  # Diagonal Distance
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def get_pos(blocks, road_index):
    pnt_arr = mapping(blocks["geometry"][road_index])
    pnt_arr = pnt_arr['coordinates']
    return pnt_arr[0], pnt_arr[-1]


def get_target_roads(roads, node, road_index):
    if node == 0:
        return pd.array([])
    up_ser = roads["UP_FROM_NO"][roads["UP_FROM_NO"] == node]
    down_ser = roads["UP_TO_NODE"][roads["UP_TO_NODE"] == node]

    if True in up_ser.index.isin([road_index]):
        del up_ser[road_index]
    if True in down_ser.index.isin([road_index]):
        del down_ser[road_index]
    target_roads = np.concatenate((np.array(up_ser.index), np.array(down_ser.index)), axis=None)
    return target_roads


def astar_road(blocks, start, road_index, end, end_index):
    # startNode와 endNode 초기화
    startNode = Node(None, start, None, road_index)
    endNode = Node(None, end, blocks["UP_FROM_NO"][end_index], end_index)
    # openList, closedList 초기화
    openList = []
    closedList = []

    # openList에 시작 노드 추가
    road_pos = get_pos(blocks, road_index)
    temp = Node(startNode, road_pos[0], blocks["UP_FROM_NO"][road_index], road_index)
    temp.f = np.sqrt(((road_pos[0][0] - start[0]) **
                      2) + ((road_pos[0][1] - start[1]) ** 2))
    openList.append(temp)
    temp = Node(startNode, road_pos[1], blocks["UP_TO_NODE"][road_index], road_index)
    temp.f = np.sqrt(((road_pos[1][0] - start[0]) **
                      2) + ((road_pos[1][1] - start[1]) ** 2))
    openList.append(temp)

    # endNode를 찾을 때까지 실행
    while openList:
        # 현재 노드 지정
        currentNode = openList[0]
        currentIdx = 0

        # 이미 같은 노드가 openList에 있고, f 값이 더 크면
        # currentNode를 openList안에 있는 값으로 교체
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIdx = index

        #print("curr", currentNode.road_index, currentNode.road_node)
        # openList에서 제거하고 closedList에 추가
        openList.pop(currentIdx)
        closedList.append(currentNode)

        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode == endNode:
            print("end")
            path = []
            current = currentNode
            while current is not None:
                # maze 길을 표시하려면 주석 해제
                # x, y = current.position
                # maze[x][y] = 7 
                path.append({"index": current.road_index, "node": current.road_node})
                current = current.parent
            return path[::-1]  # reverse

        children = []
        # 인접한 블럭
        target_roads = get_target_roads(blocks, currentNode.road_node, currentNode.road_index)

        for tar_road in target_roads:
            tar_pos = get_pos(blocks, tar_road)
            if currentNode.road_node == blocks["UP_FROM_NO"][tar_road]:
                newNode = Node(currentNode, tar_pos[1], blocks["UP_TO_NODE"][tar_road], tar_road)
            elif currentNode.road_node == blocks["UP_TO_NODE"][tar_road]:
                newNode = Node(currentNode, tar_pos[0], blocks["UP_FROM_NO"][tar_road], tar_road)
            children.append(newNode)

        # 자식들 모두 loop
        for child in children:
            # 자식이 closedList에 있으면 continue
            if child in closedList:
                continue

            # f, g, h값 업데이트

            child.g = currentNode.g + blocks["LENGTH"][child.road_index] * 360 / 40075000
            child.h = np.sqrt(((child.position[0] - endNode.position[0]) **
                               2) + ((child.position[1] - endNode.position[1]) ** 2))
            # child.h = heuristic(child, endNode) 다른 휴리스틱
            # print("position:", child.position) 거리 추정 값 보기
            # print("from child to goal:", child.h)

            child.f = child.g + child.h

            # 자식이 openList에 있으고, g값이 더 크면 continue
            if len([openNode for openNode in openList
                    if child == openNode and child.g > openNode.g]) > 0:
                continue

            openList.append(child)
