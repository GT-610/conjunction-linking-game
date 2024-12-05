import pygame
import sys
import numpy as np
pygame.init()

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, font_path
from frontend.commons import Button, button_width, button_height, button_font
from frontend.commons import WHITE, BLACK, BLUE, GRAY, YELLOW

from backend.map import generate_map
from backend.block import Block
from backend.conj_block import ConjunctionBlock
from backend.conjunctions import CONJUNCTIONS
from backend.timer import Timer
from backend.score import Score
from backend.link import getLinkType
from backend.game_events import update_blocks, handle_block_click, check_and_clear

# 初始化计时器
timer = Timer()

# 主要游戏部分
# 游戏主界面
# 游戏主界面
def game_page():

    # 是否处于暂停状态
    global is_paused, timer, isGameEnd
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
    offset_x = (SCREEN_WIDTH - map_size * 50) // 2  # 使地图居中
    offset_y = (SCREEN_HEIGHT - map_size * 50) // 2

    # 在游戏开始时生成地图
    map_size = 10
    map = generate_map(map_size)  # 生成10x10的地图

    ## 生成块对象
    blocks = np.empty((map_size + 2, map_size + 2), dtype=object)  # 创建一个空的二维数组用于存储 Block 对象

    # 生成一维 blocks 数组并 reshape
    blocks = np.empty((map_size + 2) * (map_size + 2), dtype=object)
    for index in range((map_size + 2) * (map_size + 2)):
        i, j = divmod(index, map_size + 2)
        blocks[index] = Block(map, (i, j), 50, offset_x, offset_y)
    blocks = blocks.reshape((map_size + 2, map_size + 2))

    # 创建联结词块
    conjunction_blocks = []
    block_size = 100  # 联结词块大小
    start_x, start_y = 50, 150  # 起始位置
    spacing = 20  # 块之间的间隔

    def select_conjunction_block(selected_block):
        """联结词块被选中后的回调"""
        global cur_conj
        cur_conj = selected_block.conj_name  # 更新当前联结词
        for block in conjunction_blocks:
            block.set_selected(block == selected_block)  # 更新其他块状态

    # 当前选中的联结词（全局变量）
    cur_conj = "与"  # 默认值
    # 初始化联结词块
    for i, conj_name in enumerate(CONJUNCTIONS.keys()):
        pos = (start_x, start_y + i * (block_size + spacing))
        conj_block = ConjunctionBlock(conj_name, pos, block_size, select_conjunction_block)
        conjunction_blocks.append(conj_block)

    # 初始化分数对象
    score_manager = Score()
    score_font = button_font  # 假设已有的字体资源

    # 分数文本
    score_text = score_font.render(f"分数: {score_manager.get_score()}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(30, 60))

    # 剩余时间文本
    # 游戏开始时启动计时
    timer.start()
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

                # 检查联结词块交互
                for block in conjunction_blocks:
                    block.handle_click(event.pos)
                
                # 游戏未在暂停的时候，检查地图块交互
                if not is_paused:
                    for row in blocks:
                        for block in row:
                            if block.rect.collidepoint(event.pos):
                                handle_block_click(block, map, blocks, score_manager)
                                update_blocks(map, blocks)
        # 绘制背景
        screen.fill(BLACK)

        # 绘制已用时间（如果未暂停）
        if not is_paused:
            elapsed_time = timer.get_elapsed_time()
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

        # 绘制每个块
        for block in np.nditer(blocks, flags=['refs_ok']):
            block = block.item()  # 取出 Block 对象
            if block.value != -1:
                block.draw(screen)

        # 绘制联结词块
        for conj_block in conjunction_blocks:
            conj_block.draw(screen)

        # 游戏结束
        if np.all(map == -1) or isGameEnd == 1:
            # 计算最终分数和用时
            final_score = score_manager.get_score()
            elapsed_time = timer.get_elapsed_time()

            # 调用结算页面
            from frontend.pages.checkout import checkout_page
            checkout_page(final_score, elapsed_time)
            return

        # 暂停时显示提示
        if is_paused:
            paused_text = button_font.render("游戏暂停中", True, WHITE)
            paused_rect = paused_text.get_rect(topleft=(30, 100))
            screen.blit(paused_text, paused_rect)
            pygame.display.flip()  # 更新屏幕

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

# 暂停操作
def pause_game():
    global is_paused
    if is_paused:
        timer.resume()  # 恢复计时
    else:
        timer.pause()  # 暂停计时
    is_paused = not is_paused


# 假设 isGameEnd 被其他地方设置为 1 来表示游戏结束
isGameEnd = 0  # 游戏未结束

# 游戏结束时调用的函数
def end_game():
    global isGameEnd
    isGameEnd = 1  # 设置游戏结束标志

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