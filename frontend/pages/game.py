import pygame
import sys
import numpy as np

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, scale
from frontend.commons import Button, button_width, button_height, small_font, bg0
from frontend.commons import WHITE, YELLOW

from backend.map import generate_map
from backend.block import Block
from backend.config import config, navigate_with_params
from backend.conj_block import ConjunctionBlock
from backend.conjunctions import DIFFICULTY_CONJUNCTIONS
from backend.timer import timer
from backend.game_events import update_blocks, handle_block_click

# 游戏主界面
def game_page():
    # 加载联结词
    from frontend.loading import display_loading_message
    display_loading_message(screen, "初始化基本参数...", small_font)

    # 重置参数
    timer.reset()
    config.reset()
    conjunctions = DIFFICULTY_CONJUNCTIONS[config.difficulty]
    config.cur_conj = conjunctions[0]

    # 生成地图
    display_loading_message(screen, "生成地图...", small_font)
    map_size = 10
    map = generate_map(map_size)
    print(f"已生成大小为 {map_size} * {map_size} 的地图")

    # 生成一维 blocks 数组并 reshape 为二维
    display_loading_message(screen, "生成地图块...", small_font)
    block_size = 50 * scale

    # 计算居中的偏移量
    offset_x = (SCREEN_WIDTH - block_size * (map_size + 2)) // 2
    offset_y = (SCREEN_HEIGHT - block_size * (map_size + 2)) // 2

    # 生成所有块的索引 (i, j) 的坐标
    indices = np.array(np.meshgrid(range(map_size + 2), range(map_size + 2)), dtype=np.int16).T.reshape(-1, 2)

    # 创建 Block 对象
    blocks = np.array([
        Block(map, (i, j), block_size, offset_x, offset_y)
        for i, j in indices
    ], dtype=object)
        
    blocks = blocks.reshape((map_size + 2, map_size + 2))
    del offset_x, offset_y, indices, map_size

    # 创建联结词块
    display_loading_message(screen, "初始化联结词块...", small_font)
    conj_blocks = []
    block_size = 100 * scale  # 联结词块大小
    start_x, start_y = 50 * scale, 150 * scale  # 起始位置
    spacing = 20 * scale  # 块之间的间隔

    # 初始化联结词块
    ## 联结词块被选中后，更新当前联结词
    def select_conjunction_block(selected_block):
        config.cur_conj = selected_block.conj_name

    for i, conj_name in enumerate(conjunctions):
        pos = (start_x, start_y + i * (block_size + spacing))
        conj_block = ConjunctionBlock(conj_name, pos, block_size, select_conjunction_block)
        conj_blocks.append(conj_block)

    display_loading_message(screen, "加载其他组件...", small_font)


    # 剩余时间
    time_text = small_font.render("已用时间: 0", True, WHITE)
    time_pos = (30 * scale, 10 * scale)
    print("初始化计时器完成")

    # 完成度
    cr_text = small_font.render(f"完成度: 0%", True, WHITE)
    cr_pos = (30 * scale, 50 * scale)
    print("初始化完成度完成")

    del display_loading_message

    # 按钮创建
    pause_button = Button(
        "暂停",
        SCREEN_WIDTH // 2 - 160 * scale,
        SCREEN_HEIGHT * 0.05,
        pause_game
    )

    # 重新开始按钮（仅在暂停时显示）
    restart_button = Button(
        "重新开始",
        SCREEN_WIDTH // 2 + 160 * scale,
        SCREEN_HEIGHT * 0.05,
        lambda: setattr(config, "restart", True)
    )

    # 返回主菜单按钮
    return_main_menu_button = Button(
        "返回主菜单",
        SCREEN_WIDTH  - 100 * scale,
        SCREEN_HEIGHT * 0.925,
        lambda: setattr(config, "is_game_end", True)
    )

    help_button = Button(
        "帮助",
        SCREEN_WIDTH - 100 * scale,  # 地图右侧
        150 * scale,                 # y 坐标
        callback=show_help_page
    )

    from backend.hint import hint_game
    def hint():
        hint_game(map, blocks, config.sfx_vol)

    hint_button = Button(
        "提示",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT * 0.05,
        hint
    )

    print("已绘制按钮")

    # 开始计时
    pygame.init()
    timer.start()

    # 绘制游戏界面
    while True:
        if config.position != "game" or config.restart:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 处理按钮点击事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                pause_button.check_click()
                hint_button.check_click()
                help_button.check_click()
                restart_button.check_click()
                return_main_menu_button.check_click()
                
                # 游戏未在暂停的时候，检查交互
                if not config.is_paused:
                    for row in blocks:
                        for block in row:
                            if block.rect.collidepoint(event.pos):
                                handle_block_click(block, map, blocks, config.cur_conj)
                                update_blocks(map, blocks)
                    for block in conj_blocks:
                        block.handle_click(event.pos)
        # 绘制背景
        bg0.draw(screen)

        # 绘制已用时间（如果未暂停）
        if not config.is_paused:
            elapsed_time = timer.get_elapsed_time()
        time_text = small_font.render(f"已用时间: {elapsed_time}", True, WHITE)
        screen.blit(time_text, time_pos)

        # 绘制分数显示
        cr_text = small_font.render(f"完成度: {int(config.clear_rate * 100)}%", True, WHITE)
        screen.blit(cr_text, cr_pos)

        # 绘制按钮
        pause_button.draw(screen)
        hint_button.draw(screen)
        help_button.draw(screen)
        if config.is_paused:
            restart_button.draw(screen)
        return_main_menu_button.draw(screen)

        # 绘制每个块
        for block in np.nditer(blocks, flags=['refs_ok']):
            block = block.item()
            if block.value != -1:
                block.draw(screen)

        # 绘制联结词块
        for conj_block in conj_blocks:
            conj_block.draw(screen)

        # 通关判定
        if np.all(map == -1):
            config.is_cleared = True
            config.is_game_end = True

        # 游戏结束
        if config.is_game_end == True:
            elapsed_time = timer.get_elapsed_time()
            # 调用结算页面
            navigate_with_params("checkout", elapsed_time=elapsed_time)
            return

        # 暂停时显示暂停文字
        if config.is_paused:
            paused_text = small_font.render("游戏暂停中", True, WHITE)
            screen.blit(paused_text, (30 * scale, 90 * scale))

        # 更新屏幕
        pygame.display.flip()

# 绘制路径连线
def draw_link_line(block1, block2, link_type, blocks, color=YELLOW, delay_time=250):
    # 计算两个块的中心坐标
    start_pos = block1.outerCenterPoint
    end_pos = block2.outerCenterPoint

    if link_type == 1:
        # 绘制一条线连接两个块
        pygame.draw.line(screen, color, start_pos, end_pos, 5)
        print("绘制直连线")

    elif link_type[0] == 2:
        blockCorner = blocks[link_type[1][0]][link_type[1][1]].outerCenterPoint
        pygame.draw.line(screen, color, start_pos, blockCorner, 5)
        pygame.draw.line(screen, color, blockCorner, end_pos, 5)
        print("绘制单拐点线")
    
    elif link_type[0] == 3:
        blockCorner1 = blocks[link_type[1][0][0]][link_type[1][0][1]].outerCenterPoint
        blockCorner2 = blocks[link_type[1][1][0]][link_type[1][1][1]].outerCenterPoint
        pygame.draw.line(screen, color, start_pos, blockCorner1 , 5)
        pygame.draw.line(screen, color, blockCorner1, blockCorner2, 5)
        pygame.draw.line(screen, color, blockCorner2, end_pos, 5)
        print("绘制双拐点线")

    # 更新屏幕
    pygame.display.update()

    # 延迟清屏
    pygame.time.delay(delay_time)
    print("已绘制连线")

# 暂停操作
def pause_game():
    if config.is_paused:
        timer.resume()  # 恢复计时
    else:
        timer.pause()  # 暂停计时
    config.is_paused = not config.is_paused

def show_help_page():
    pause_game()
    config.position = "help"
    from frontend.pages.help import help_page
    help_page(in_game=True)