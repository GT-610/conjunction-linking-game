import pygame
pygame.init()

from frontend.commons import *

class Block:
    def __init__(self, map, point, block_size, offset_x, offset_y):
        self.innerX, self.innerY = point  # 块的位置 (map的坐标)
        self.value = map[self.innerX][self.innerY]  # 块的值 (0 或 1)

        # 块的基本信息
        self.outerWidth = block_size # 外部尺寸
        self.outerX = offset_x + self.innerY * block_size  # 每列的 x 坐标
        self.outerY = offset_y + self.innerX * block_size  # 每行的 y 坐标
        self.outerCenterPoint = (self.outerX + int(self.outerWidth / 2), self.outerY + int(self.outerWidth / 2))
        self.rect = pygame.Rect(self.outerX, self.outerY, self.outerWidth, self.outerWidth)
        
        # 块内字体，显示0或1
        self.font = pygame.font.Font(font_path, 36)  

        # 选中状态
        self.selected = False

    def draw(self, screen):
        # 根据块的值 (0 或 1) 选择颜色
        color = WHITE if self.value == 0 else BLUE
        pygame.draw.rect(screen, color, (self.outerX, self.outerY, self.outerWidth, self.outerWidth))
        pygame.draw.rect(screen, BLACK, (self.outerX, self.outerY, self.outerWidth, self.outerWidth), 2)

        # 如果块被选中，绘制黄色边框
        if self.selected:
            pygame.draw.rect(screen, YELLOW, (self.outerX, self.outerY, self.outerWidth, self.outerWidth), 4)  # 黄色边框

        # 绘制块的边界
        pygame.draw.rect(screen, BLACK, (self.outerX, self.outerY, self.outerWidth, self.outerWidth), 2)

        # 渲染块的值（0 或 1）
        value_text = self.font.render(str(self.value), True, BLACK)  # 使用黑色字体渲染值
        value_rect = value_text.get_rect(center=(self.outerX + self.outerWidth // 2, self.outerY + self.outerWidth // 2))  # 计算中心坐标
        screen.blit(value_text, value_rect)  # 绘制文本

    def is_clicked(self, pos):
        """检测鼠标点击的位置是否在块的范围内"""
        return self.rect.collidepoint(pos)

    # 切换选中状态
    def toggle_selection(self):
        self.selected = not self.selected

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


# 两个拐点检查
def isTwoCornerLink(map, p1, p2):
    rows, cols = len(map), len(map[0])
    
    # 遍历所有可能的水平、垂直线
    for x in range(rows):  # x 遍历所有行，包括边界
        for y in range(cols):  # y 遍历所有列，包括边界
            # 构建两个拐点
            pointCorner1 = (p1[0], y)  # 水平拐点
            pointCorner2 = (x, p2[1])  # 垂直拐点

            # 排除 p1 与 p2 自身两个点
            if pointCorner1 == p1 or pointCorner2 == p2:
                continue

            # 检查路径连通性
            # 对边界点：无需检查是否为空
            if (map[p1[0]][y] == -1 or map[x][p2[1]] == -1):
                if isStraightLink(map, p1, pointCorner1) and isStraightLink(map, pointCorner2, p2):
                    return [pointCorner1, pointCorner2]

            # 对普通点：检查路径连通性，且拐点应为空
            elif (isStraightLink(map, p1, pointCorner1) and
                  isStraightLink(map, pointCorner1, pointCorner2) and
                  isStraightLink(map, pointCorner2, p2) and
                  isEmptyInMap(map, pointCorner1) and
                  isEmptyInMap(map, pointCorner2)):
                return [pointCorner1, pointCorner2]

    return None






# 获取两个点连通类型
def getLinkType(map, p1, p2):
    if map[p1[0]][p1[1]] != map[p2[0]][p2[1]]:
        return 0 # 相同块无法连通

    if isStraightLink(map, p1, p2):
        return 1 # 直连
        
    res = isOneCornerLink(map, p1, p2)
    if res:
        return (2, res) # 单拐点连通
        
    res = isTwoCornerLink(map, p1, p2)
    if res:
        return (3, res) # 双拐点连通
        
    return 0 # 无法连通

# 判断两个块是否连通并清除
def check_and_clear(map, p1, p2):
    link_type = getLinkType(map, p1, p2)
    
    print(f"连通类型：{link_type}")

    # 如果返回值是 0，说明不连通，直接返回
    if link_type == 0:
        return False
    
    # 如果连通（返回值为1，2，或3），执行清除操作
    ClearLinkedBlocks(map, p1, p2)
    return link_type


# 消除连通的两个块
def ClearLinkedBlocks(map, p1, p2):
    map[p1[0]][p1[1]] = -1
    map[p2[0]][p2[1]] = -1
    print("已消除")
    # 清除绘制
    # 保存 p1[0], p1[1], p2[0], p2[1], p1的值, p2的值

# 游戏结束
def isGameEnd(map):
    return np.all(map == -1)
 