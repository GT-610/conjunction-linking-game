import pygame
pygame.init()
import sys

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, font_path
from frontend.commons import Button, button_width, button_height, button_font
from frontend.commons import WHITE, BLACK, BLUE, GRAY, YELLOW

from backend.map import generate_map

from backend.block import Block, block_size
from backend.link import getLinkType
from backend.game_logic import check_and_clear

# 主要游戏部分
# 游戏主界面
# 游戏主界面
def game_page():

    # 是否处于暂停状态
    global is_paused
    is_paused = False

    # 按钮创建
    pause_button = Button(
        "暂停",
        (SCREEN_WIDTH - button_width) // 2 - button_width - 150,
        20,
        button_width, button_height,
        pause_game
    )
    hint_button = Button(
        "提示",
        (SCREEN_WIDTH - button_width) // 2,
        20,
        button_width, button_height,
        hint_game
    )
    # 重新开始按钮（仅在暂停时显示）
    restart_button = Button(
        "重新开始",
        (SCREEN_WIDTH - button_width) // 2 + button_width + 150,
        20,
        button_width,button_height,
        restart_game
    )
    # 返回主菜单按钮
    return_main_menu_button = Button(
        "返回主菜单",
        SCREEN_WIDTH - button_width - 10,
        SCREEN_HEIGHT - button_height - 10,
        button_width, button_height,
        return_main_menu
    )

    # 块
    ## 游戏地图大小 10x10
    map_size = 10
    offset_x = (SCREEN_WIDTH - map_size * block_size) // 2  # 使地图居中
    offset_y = (SCREEN_HEIGHT - map_size * block_size) // 2

    # 在游戏开始时生成地图
    map_size = 10
    map = generate_map(map_size)  # 生成10x10的地图

    ## 生成块对象
    blocks = []
    for i in range(map_size + 2):
        row = []
        for j in range(map_size + 2):
            block = Block(map, (i, j), block_size, offset_x, offset_y)
            row.append(block)
        blocks.append(row)

    # 剩余时间文本
    time_start = pygame.time.get_ticks()  # 记录开始时间（毫秒）
    time_text = button_font.render("已用时间: 0", True, WHITE)
    time_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 10, 20))

    # 绘制游戏界面
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 处理按钮点击事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                pause_button.check_click()
                hint_button.check_click()
                restart_button.check_click()
                return_main_menu_button.check_click()
                # 检测哪个块被点击
                for row in blocks:
                    for block in row:
                        if block.rect.collidepoint(event.pos):
                            handle_block_click(block, map, blocks)
                            update_blocks(map, blocks)  # 更新块

        # 绘制背景
        screen.fill(BLACK)

        # 绘制已用时间
        elapsed_time = (pygame.time.get_ticks() - time_start) // 1000  # 获取已经过去的秒数
        time_text = button_font.render(f"已用时间: {elapsed_time}", True, WHITE)
        screen.blit(time_text, time_rect)

        # 绘制顶部区域
        screen.blit(time_text, time_rect)

        # 绘制按钮
        pause_button.draw(screen)
        hint_button.draw(screen)
        ## 如果暂停，则显示“重新开始”按钮
        if is_paused:
            restart_button.draw(screen)
        # 绘制返回主菜单按钮
        return_main_menu_button.draw(screen)

        # 画中央区域的地图框架（留空）
        # 居中绘制
        map_width, map_height = 750, 750
        map_x = (SCREEN_WIDTH - map_width) // 2
        map_y = (SCREEN_HEIGHT - map_height) // 2 + 20
        pygame.draw.rect(screen, WHITE, (map_x, map_y, map_width, map_height), 2)  # 绘制地图框架

        # 绘制每个块
        for row in blocks:
            for block in row:
                if block.value != -1:
                    block.draw(screen)

        # 更新屏幕
        pygame.display.flip()

# 记录已选择的块
selected_block = None

# 处理块的点击事件
def handle_block_click(block, map, blocks):
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

# 绘制路径连线
def draw_link_line(block1, block2, link_type, blocks):
    # 计算两个块的中心坐标
    start_pos = block1.outerCenterPoint
    end_pos = block2.outerCenterPoint

    if link_type == 1:
        # 绘制一条线连接两个块
        pygame.draw.line(screen, YELLOW, start_pos, end_pos, 5)
        print("绘制直连线")

    elif link_type[0] == 2:
        blockCorner = blocks[link_type[1][0]][link_type[1][1]].outerCenterPoint

        pygame.draw.line(screen, YELLOW, start_pos, blockCorner, 5)
        pygame.draw.line(screen, YELLOW, blockCorner, end_pos, 5)
        print("绘制单拐点线")
    
    elif link_type[0] == 3:
        blockCorner1 = blocks[link_type[1][0][0]][link_type[1][0][1]].outerCenterPoint
        blockCorner2 = blocks[link_type[1][1][0]][link_type[1][1][1]].outerCenterPoint
        pygame.draw.line(screen, YELLOW, start_pos, blockCorner1 , 5)
        pygame.draw.line(screen, YELLOW, blockCorner1, blockCorner2, 5)
        pygame.draw.line(screen, YELLOW, blockCorner2, end_pos, 5)
        print("绘制双拐点线")

    # 更新屏幕，确保连线可见
    pygame.display.update()

    # 延迟清屏
    pygame.time.delay(250)
    print("已绘制连线")


# 暂停游戏（占位函数）
def pause_game():
    global is_paused
    is_paused = not is_paused  # 更改暂停状态
    if is_paused == True:
        print("暂停功能待实现")
    else:
        print("已取消暂停")

# 提示（占位函数）
def hint_game():
    print("提示功能待实现")

# 重新开始
def restart_game():
    print("重新开始游戏功能待实现")
    global is_paused
    is_paused = False  # 重新开始游戏，恢复游戏状态

# 返回主菜单
def return_main_menu():
    print("返回主菜单功能待实现")
    difficulty_selection_page()