from backend.link import getLinkType

# 更新块逻辑
def update_blocks(map, blocks):
    for i, row in enumerate(blocks):
        for j, block in enumerate(row):
            block.value = map[i][j]

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

def timer():
    pass