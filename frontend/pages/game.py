import pygame
import sys
import numpy as np
pygame.init()

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT
from frontend.commons import Button, button_width, button_height, button_font
from frontend.commons import WHITE, BLACK, BLUE, GRAY, YELLOW

from backend.map import generate_map
from backend.block import Block
from backend.config import config
from backend.conj_block import ConjunctionBlock
from backend.conjunctions import DIFFICULTY_CONJUNCTIONS
from backend.link import getLinkType
from backend.timer import Timer
from backend.score import Score
from backend.game_events import update_blocks, handle_block_click

# 初始化计时器
timer = Timer()

# 游戏主界面
def game_page():

    # 初始化计时器并重置计时器和基本参数
    global timer
    timer.reset()
    config.reset()

    conjunctions = DIFFICULTY_CONJUNCTIONS[config.difficulty]
    config.cur_conj = conjunctions[0]

    # 按钮创建
    pause_button = Button(
        "暂停",
        (SCREEN_WIDTH - button_width) // 2 - button_width - 150,
        20,
        button_width, button_height,
        pause_game
    )

    # 重新开始按钮（仅在暂停时显示）
    restart_button = Button(
        "重新开始",
        (SCREEN_WIDTH - button_width) // 2 + button_width + 150,
        20,
        button_width,button_height,
        restart_game
    )

    return_main_menu_button = Button(
        "返回主菜单",
        SCREEN_WIDTH - 200 - 10,
        SCREEN_HEIGHT - button_height - 10,
        200, button_height,
        return_main_menu
    )
    print("已绘制按钮")

    # 生成地图
    map_size = 10
    map = generate_map(map_size)
    print(f"已生成大小为 {map_size} * {map_size} 的地图")

    # 生成一维 blocks 数组并 reshape 为二维
    ## 块的偏移坐标
    offset_x = (SCREEN_WIDTH - map_size * 50) // 2
    offset_y = (SCREEN_HEIGHT - map_size * 50) // 2

    blocks = np.empty((map_size + 2) * (map_size + 2), dtype=object)
    for index in range((map_size + 2) * (map_size + 2)):
        i, j = divmod(index, map_size + 2)
        blocks[index] = Block(map, (i, j), 50, offset_x, offset_y)
    blocks = blocks.reshape((map_size + 2, map_size + 2))
    print("已生成地图块")

    def hint():
        hint_game(map, blocks)

    hint_button = Button(
        "提示",
        (SCREEN_WIDTH - button_width) // 2,
        20,
        button_width, button_height,
        hint
    )

    # 创建联结词块
    conj_blocks = []
    block_size = 100  # 联结词块大小
    start_x, start_y = 50, 150  # 起始位置
    spacing = 20  # 块之间的间隔

    # 初始化联结词块
    ## 联结词块被选中后的回调
    def select_conjunction_block(selected_block):
        config.cur_conj = selected_block.conj_name  # 更新当前联结词

    for i, conj_name in enumerate(conjunctions):
        pos = (start_x, start_y + i * (block_size + spacing))
        conj_block = ConjunctionBlock(conj_name, pos, block_size, select_conjunction_block)
        conj_blocks.append(conj_block)
    print("已生成联结词块")

    # 分数
    score_manager = Score()
    score_font = button_font
    score_text = score_font.render(f"分数: {score_manager.get_score()}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(30, 60))
    print("初始化分数完成")

    # 剩余时间
    time_text = button_font.render("已用时间: 0", True, WHITE)
    time_rect = time_text.get_rect(topleft=(30, 20))

    # 游戏开始时启动计时
    timer.start()
    print("初始化计时器完成")

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
                for block in conj_blocks:
                    block.handle_click(event.pos)
                
                # 游戏未在暂停的时候，检查地图块交互
                if not config.is_paused:
                    for row in blocks:
                        for block in row:
                            if block.rect.collidepoint(event.pos):
                                handle_block_click(block, map, blocks, score_manager, config.cur_conj)
                                update_blocks(map, blocks)
        # 绘制背景
        screen.fill(BLACK)

        # 绘制已用时间（如果未暂停）
        if not config.is_paused:
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
        if config.is_paused:
            restart_button.draw(screen)
        # 绘制返回主菜单按钮
        return_main_menu_button.draw(screen)

        # 绘制每个块
        for block in np.nditer(blocks, flags=['refs_ok']):
            block = block.item()  # 取出 Block 对象
            if block.value != -1:
                block.draw(screen)

        # 绘制联结词块
        for conj_block in conj_blocks:
            conj_block.draw(screen)

        # 游戏结束
        if config.is_game_end == True:
            if np.all(map == -1):
                config.is_cleared = True
            # 计算最终分数和用时
            final_score = score_manager.get_score()
            elapsed_time = timer.get_elapsed_time()

            # 调用结算页面
            from frontend.pages.checkout import checkout_page
            checkout_page(final_score, elapsed_time)
            return

        # 暂停时显示提示
        if config.is_paused:
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
    if config.is_paused:
        timer.resume()  # 恢复计时
    else:
        timer.pause()  # 暂停计时
    config.is_paused = not config.is_paused

# 提示（占位函数）
def hint_game(map, blocks):
    print("激活提示")
    from frontend.commons import GREEN, screen
    # 遍历地图寻找可以连通的一对块
    for x1 in range(10):
        for y1 in range(10):
            for x2 in range(10):
                for y2 in range(10):
                    # 跳过空块或相同位置
                    if (x1, y1) == (x2, y2) or map[x1][y1] == -1 or map[x2][y2] == -1:
                        continue
                    
                    # 检查连通性
                    link_type = getLinkType(map, (x1, y1), (x2, y2))
                    if link_type:
                        # 找到连通块，绘制提示线
                        block1 = blocks[x1][y1]
                        block2 = blocks[x2][y2]

                        draw_link_line(block1, block2, link_type, blocks)
                        pygame.display.update()

                        # 延迟一段时间后清除提示
                        pygame.time.delay(1000)  # 提示线显示 1 秒
                        return

    print("没有可提示的连通块")

# 重新开始
def restart_game():
    game_page()

# 返回主菜单
def return_main_menu():
    config.is_game_end = True