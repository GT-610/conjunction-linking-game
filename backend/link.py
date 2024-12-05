from frontend.commons import *

# 是否存在障碍物
def isEmptyInMap(map, point):
    x, y = point
    # 检查是否在边界内，且是否为空
    return 0 <= x < len(map) and 0 <= y < len(map[0]) and map[x][y] == -1

# 直连
def isStraightLink(map, p1, p2):
    if p1[1] == p2[1]:
        start, end = sorted([p1[0], p2[0]])
        for x in range(start + 1, end):
            if map[x][p1[1]] != -1: # 没有障碍物
                return False
    elif p1[0] == p2[0]:
        start, end = sorted([p1[1], p2[1]])
        for y in range(start + 1, end):
            if map[p1[0]][y] != -1:
                return False
    else:
        return False
    return True

# 一个拐点
def isOneCornerLink(map, p1, p2):
    pointCorner = (p1[0], p2[1])  # 假设为水平-垂直拐点
    if (isStraightLink(map, p1, pointCorner) and 
        isStraightLink(map, pointCorner, p2) and 
        isEmptyInMap(map, pointCorner)):
        return pointCorner

    pointCorner = (p2[0], p1[1])  # 假设为垂直-水平拐点
    if (isStraightLink(map, p1, pointCorner) and 
        isStraightLink(map, pointCorner, p2) and 
        isEmptyInMap(map, pointCorner)):
        return pointCorner

    return None

# 两个拐点
def isTwoCornerLink(map, p1, p2):
    rows, cols = len(map), len(map[0])
    
    # 定义四个方向：上、右、下、左
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
    
    # 遍历四个方向，寻找空格（-1）
    for direction in directions:
        # 计算checkP坐标
        checkP = (p1[0] + direction[0], p1[1] + direction[1])
        
        # 确保checkP在地图范围内
        if checkP[0] < 0 or checkP[0] >= rows or checkP[1] < 0 or checkP[1] >= cols:
            continue
        
        # 检查checkP是否是空格
        if map[checkP[0]][checkP[1]] != -1:
            continue
        
        # 检查从p1到checkP，以及从checkP到p2是否能通过单直角连通
        corner1, corner2 = isOneCornerLink(map, p1, checkP), isOneCornerLink(map, checkP, p2)
        
        # 如果找到了有效的拐点，返回
        if corner1 and corner2:
            return [corner1, corner2]  # 返回两个拐点坐标
    
    # 如果四个方向都没有找到合适的checkP
    return None

# 获取两个点连通类型
from backend.conjunctions import CONJUNCTIONS
def getLinkType(map, p1, p2, cur_conj):
    # 获取当前选定的联结词的运算函数
    conj_func = CONJUNCTIONS.get(cur_conj)

    if conj_func(map[p1[0]][p1[1]], map[p2[0]][p2[1]]) != 1:
        print(f"{p1} 和 {p2} 不符合{cur_conj}要求")
        return 0 # 联结词不满足肯定为不连通

    if isStraightLink(map, p1, p2):
        return 1 # 直连
        
    res = isOneCornerLink(map, p1, p2)
    if res:
        return (2, res) # 单拐点连通
        
    res = isTwoCornerLink(map, p1, p2)
    if res:
        return (3, res) # 双拐点连通
        
    return 0 # 无法连通