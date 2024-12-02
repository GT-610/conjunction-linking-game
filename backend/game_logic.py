# 处理块的点击事件
def handle_block_click(block, map, blocks):
    # 记录已选择的块
    selected_block = None

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

        link_type = check_and_clear(map, p1, p2)
        # 检查这两个块是否连通
        if link_type:
            draw_link_line(selected_block, block, link_type, blocks)  # 绘制连线

        # 重置选择状态
        selected_block.toggle_selection()
        block.toggle_selection()
        selected_block = None

# 更新块逻辑
def update_blocks(map, blocks):
    for i, row in enumerate(blocks):
        for j, block in enumerate(row):
            block.value = map[i][j]

def timer():
    pass