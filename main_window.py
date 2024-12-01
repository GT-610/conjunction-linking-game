import pygame
import sys
import time

from frontend.widgets import Button, Slider, TextInputBox
from frontend.leaderboard import load_leaderboard, save_leaderboard ,get_sorted_leaderboard
from frontend.commons import *

from backend.map import generate_map
from backend.block import Block, check_and_clear


# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("连连看")



# 字体
font = pygame.font.Font(font_path, 48)  # 标题字体
button_font = pygame.font.Font(font_path, 36)  # 按钮字体

# 主菜单
def main_menu():
    button_width = 200  # 按钮宽度
    button_height = 50  # 按钮高度
    vertical_spacing = 80  # 按钮之间的间距

    # 创建按钮
    buttons = [
        Button(
            "开始游戏",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 - 1.5 * vertical_spacing,
            button_width, button_height,
            difficulty_selection_page
        ),
        Button("排行榜",
        (SCREEN_WIDTH - button_width) // 2,
        SCREEN_HEIGHT // 2 - 0.5 * vertical_spacing,
        button_width, button_height,
        leaderboard_page
        ),
        Button(
            "设置",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + 0.5 * vertical_spacing,
            button_width, button_height,
            settings_page
        ),
        Button(
            "退出游戏",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + 1.5 * vertical_spacing,
            button_width, button_height,
            quit_game
        )
    ]
    
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                for button in buttons:
                    button.check_click()

        # 绘制界面
        screen.fill(BLACK)
        title_surface = font.render("游戏主菜单", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 绘制按钮
        for button in buttons:
            button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

# 设置界面
def settings_page():
    # 滑块实例
    bgm_slider = Slider(300, 200, 200, initial_value=50)
    sfx_slider = Slider(300, 300, 200, initial_value=50)
    name_input = TextInputBox(300, 400, 200, 40, text="玩家")

    # 返回按钮
    back_button = Button("返回主菜单", 300, 500, 200, 50, callback=main_menu)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 滑块事件处理
            bgm_slider.handle_event(event)
            sfx_slider.handle_event(event)
            # 文本框事件处理
            name_input.handle_event(event)
            # 按钮点击处理
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                back_button.check_click()

        # 绘制设置界面
        screen.fill(BLACK)

        # 绘制标题
        title_surface = font.render("设置", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 绘制滑块和文本框
        bgm_slider.draw(screen)
        sfx_slider.draw(screen)
        name_input.draw(screen)

        # 显示音量和玩家名称
        bgm_text = button_font.render(f"背景音乐音量: {int(bgm_slider.value)}", True, WHITE)
        screen.blit(bgm_text, (300, 140))
        sfx_text = button_font.render(f"音效音量: {int(sfx_slider.value)}", True, WHITE)
        screen.blit(sfx_text, (300, 240))

        name_text = button_font.render("玩家名称:", True, WHITE)
        screen.blit(name_text, (300, 340))

        # 绘制返回按钮
        back_button.draw(screen)

        # 更新显示
        pygame.display.flip()

# 排行榜界面
def leaderboard_page():
    # 清空屏幕
    screen.fill((0, 0, 0))
    
    # 显示加载中
    loading_text = font.render("加载中...", True, (255, 255, 255))
    screen.blit(loading_text, (screen.get_width() // 2 - loading_text.get_width() // 2, screen.get_height() // 2))
    pygame.display.update()

    # 加载排行榜数据
    leaderboard_data = load_leaderboard()

    # 清空加载中的文字
    screen.fill(BLACK)
    pygame.display.update()

    # 显示更新时间
    last_updated_time = leaderboard_data.get("last_updated", 0)
    last_updated_text = font.render(f"更新时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_updated_time))}", True, WHITE)
    screen.blit(last_updated_text, (20, 20))

    # 获取排行榜记录
    records = leaderboard_data.get("records", [])
    if not records:
        no_records_text = font.render("还没有记录哦", True, WHITE)
        no_records_rect = no_records_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(no_records_text, no_records_rect)
    else:
        sorted_records = get_sorted_leaderboard()
        y_offset = 100  # 起始y位置
        for record in sorted_records:
            record_text = font.render(
                f"{record['username']} - 难度: {record['difficulty']} - 时间: {record['time']}秒 - 日期: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record['date']))}",
                True, WHITE
            )
            screen.blit(record_text, (20, y_offset))
            y_offset += 50  # 每条记录之间的垂直间距

    # 绘制返回按钮
    back_button = Button(
        "返回主菜单",
        300,
        500,
        200, 50,
        callback=main_menu
    )
    back_button.draw(screen)
    pygame.display.flip()

    # 事件处理，保持窗口响应
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)  # 限制帧率
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                back_button.check_click()  # 点击返回按钮

# 选择难度界面
def difficulty_selection_page():
    # 按钮参数
    button_width = 200
    button_height = 50
    vertical_spacing = 80

    # 按钮回调函数
    def choose_easy():
        game_page()

    def choose_medium():
        print("高级难度功能待实现")

    def choose_hard():
        print("大师难度功能待实现")

    # 创建按钮
    buttons = [
        Button(
            "初级",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 - vertical_spacing,
            button_width, button_height,
            callback=choose_easy,
            hover_color=(0, 255, 0)  # 绿色
        ),  
        Button(
            "高级",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2,
            200, 50,
            callback=choose_medium,
            hover_color=(255, 0, 0)  # 红色
            ),
        Button(
            "大师",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + vertical_spacing,
            200, 50,
            callback=choose_hard,
            hover_color=(128, 0, 128)  # 紫色
            ),
        Button("返回主菜单", 300, 440, 200, 50, callback=main_menu)  # 默认按钮颜色
    ]

    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                for button in buttons:
                    button.check_click()

        # 绘制界面
        screen.fill(BLACK)

        # 绘制标题
        title_surface = font.render("选择难度", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 绘制按钮
        for button in buttons:
            button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

# 主要游戏部分
# 游戏主界面
# 游戏主界面
def game_page():
    button_width = 150
    button_height = 50
    vertical_spacing = 80

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
    for i in range(map_size):
        row = []
        for j in range(map_size):
            block = Block(map, (i, j), block_size, offset_x, offset_y)
            row.append(block)
        blocks.append(row)

    # 剩余时间文本
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

# 退出游戏
def quit_game():
    pygame.quit()
    sys.exit()

# 启动主菜单
if __name__ == "__main__":
    main_menu()
