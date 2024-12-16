from backend.link import getLinkType
from backend.config import config

# 更新块逻辑
def update_blocks(map, blocks):
    for i, row in enumerate(blocks):
        for j, block in enumerate(row):
            block.value = map[i][j]

# 记录已选择的块
selected_block = None

# 处理块的点击事件
def handle_block_click(block, map, blocks, cur_conj):
    global selected_block

    if block.value == -1:
        return

    if selected_block is None:
        # 第一个块被点击
        selected_block = block
        block.toggle_selection()  # 选中第一个块
        print(f"已选中块：({selected_block.innerX}, {selected_block.innerY})")
    elif selected_block == block:
        # 再次点击同一个块，取消选中
        block.toggle_selection()  # 取消选中状态
        selected_block = None  # 重置选择状态
    else:
        # 第二个块被点击
        block.toggle_selection()  # 选中第二个块
        p1 = (selected_block.innerX, selected_block.innerY)
        p2 = (block.innerX, block.innerY)

        print("已选中块", p2)

        # 判断连通性和联结词条件
        link_type = check_and_clear(map, p1, p2)

        # 检查这两个块是否连通
        if link_type:
            from frontend.pages.game import draw_link_line
            draw_link_line(selected_block, block, link_type, blocks)  # 绘制连线
            # 更新完成度
            config.clear_rate += 0.02

        # 重置选择状态
        selected_block.toggle_selection()
        block.toggle_selection()
        selected_block = None


# 检查两个块是否可以消除
def check_and_clear(map, p1, p2):
    # 获取两个块是否连通
    link_type = getLinkType(map, p1, p2)
    
    print(f"连通类型：{link_type}")

    # 如果返回值是 0，说明不连通，直接返回
    if link_type == 0:
        return False

    # 联结词运算的判断
    block1_value = map[p1[0]][p1[1]]
    block2_value = map[p2[0]][p2[1]]

    # 如果连通并且满足运算条件，执行清除操作
    ClearLinkedBlocks(map, p1, p2)
    return link_type

# 消除连通的两个块
def ClearLinkedBlocks(map, p1, p2):
    map[p1[0]][p1[1]] = -1
    map[p2[0]][p2[1]] = -1
    print("已消除")

# 保存当前游戏状态
def save_game_state(map, blocks, conj_blocks):
    return {
        "map": map,
        "blocks": blocks,
        "conj_blocks": conj_blocks
    }

# 恢复游戏状态
def load_game_state(game_state):
    map = game_state["map"]
    blocks = game_state["blocks"]
    conj_blocks = game_state["conj_blocks"]
    return map, blocks, conj_blocks