# 记录已选择的块
selected_block = None

# 处理块的点击事件
def handle_block_click(block, map):
    global selected_block
    
    if selected_block is None:
        # 第一个块被点击
        selected_block = block
        block.toggle_selection()  # 选中第一个块
    elif selected_block != block:
        # 第二个块被点击
        block.toggle_selection()  # 选中第二个块
        p1 = (selected_block.innerX, selected_block.innerY)
        p2 = (block.innerX, block.innerY)
        
        # 检查这两个块是否连通
        if check_and_clear(map, p1, p2):
            draw_link_line(selected_block, block)  # 绘制连线
        else:
            # 如果不连通，取消选中两个块
            selected_block.toggle_selection()
            block.toggle_selection()
        
        # 重置选择状态
        selected_block = None

# 绘制路径连线
def draw_link_line(block1, block2):
    # 计算两个块的中心坐标
    start_pos = block1.outerCenterPoint
    end_pos = block2.outerCenterPoint

    # 绘制一条线连接两个块
    pygame.draw.line(screen, (255, 255, 0), start_pos, end_pos, 5)
