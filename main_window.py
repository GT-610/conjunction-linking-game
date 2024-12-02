import pygame
import sys
import time

from frontend.widgets import Button, Slider, TextInputBox
from frontend.commons import *
# 游戏界面
from frontend.game import game_page

from backend.leaderboard import load_leaderboard, save_leaderboard ,get_sorted_leaderboard

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("连连看")

# 字体
font = pygame.font.Font(font_path, 48)  # 标题字体

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

# 退出游戏
def quit_game():
    pygame.quit()
    sys.exit()

# 启动主菜单
if __name__ == "__main__":
    main_menu()
