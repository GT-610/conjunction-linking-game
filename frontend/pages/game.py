import pygame
pygame.init()
import sys

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, font_path
from frontend.commons import Button, button_width, button_height, button_font
from frontend.commons import WHITE, BLACK, BLUE, GRAY, YELLOW

from backend.map import generate_map

from backend.block import Block, block_size
from backend.score import Score
from backend.link import getLinkType
from backend.game_events import update_blocks, handle_block_click, check_and_clear

# 主要游戏部分
# 游戏主界面
# 游戏主界面
def game_page():

    # 是否处于暂停状态
    global is_paused, isGameEnd
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

    # 初始化分数对象
    score_manager = Score()
    score_font = button_font  # 假设已有的字体资源

    # 分数文本
    score_text = score_font.render(f"分数: {score_manager.get_score()}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(30, 60))

    # 剩余时间文本
    time_start = pygame.time.get_ticks()  # 记录开始时间（毫秒）
    time_text = button_font.render("已用时间: 0", True, WHITE)
    time_rect = time_text.get_rect(topleft=(30, 20))

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
                            handle_block_click(block, map, blocks, score_manager)
                            update_blocks(map, blocks)  # 更新块

        # 绘制背景
        screen.fill(BLACK)

        # 绘制已用时间
        elapsed_time = (pygame.time.get_ticks() - time_start) // 1000  # 获取已经过去的秒数
        time_text = button_font.render(f"已用时间: {elapsed_time}", True, WHITE)
        screen.blit(time_text, time_rect)

        # 绘制分数显示
        score_text = score_font.render(f"分数: {score_manager.get_score()}", True, WHITE)
        screen.blit(score_text, score_rect)

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

        # 画中央区域的地图框架
        map_width, map_height = 650, 650
        map_x = (SCREEN_WIDTH - map_width) // 2
        map_y = (SCREEN_HEIGHT - map_height) // 2 + 20
        pygame.draw.rect(screen, WHITE, (map_x, map_y, map_width, map_height), 2)  # 绘制地图框架

        # 绘制每个块
        for row in blocks:
            for block in row:
                if block.value != -1:
                    block.draw(screen)

        # 如果游戏结束，显示结束时间
        if isGameEnd == 1:
            end_time = (pygame.time.get_ticks() - time_start) // 1000  # 游戏结束时的时间
            end_time_text = button_font.render(f"游戏结束！总时间: {end_time}秒", True, WHITE)
            screen.blit(end_time_text, (SCREEN_WIDTH // 2 - end_time_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.time.delay(2000)

        # 更新屏幕
        pygame.display.flip()

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

# 假设 isGameEnd 被其他地方设置为 1 来表示游戏结束
isGameEnd = 0  # 游戏未结束

# 游戏结束时调用的函数
def end_game():
    global isGameEnd
    isGameEnd = 1  # 设置游戏结束标志

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
    global isGameEnd
    isGameEnd = 1
    print("返回主菜单功能待实现")