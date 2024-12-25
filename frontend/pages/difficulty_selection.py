import pygame
import sys

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, scale
from frontend.commons import Button, button_width, button_height, vertical_spacing
from frontend.commons import font, WHITE, assets_dir
from backend.config import config, DIFFICULTY_MAPPING

# 选择难度界面
def difficulty_selection_page():
    
    ## 绘制静态元素
    ## 背景
    from frontend.commons import BgManager
    bg = BgManager(assets_dir/"backgrounds"/"bgDifficulty.png", 100)
    bg.draw(screen)
    del bg, BgManager

    ## 标题
    title = font.render("选择难度", True, WHITE)
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 100 * scale))
    del title

    # 按钮回调函数
    def choose_easy():
        config.difficulty = 0
        enter_game()
        print("已选择基本难度")

    def choose_advanced():
        config.difficulty = 1
        enter_game()
        print("已选择高级难度")

    def choose_expert():
        config.difficulty = 2
        enter_game()
        print("已选择专家难度")

    def choose_master():
        config.difficulty = 3
        enter_game()
        print("已选择大师难度")

    # 创建按钮
    buttons = [
        Button(
            DIFFICULTY_MAPPING[0],
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 1.5 * vertical_spacing,
            choose_easy,
            hover_color=(0, 255, 0)  # 绿色
        ),  
        Button(
            DIFFICULTY_MAPPING[1],
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 0.5 * vertical_spacing,
            choose_advanced,
            hover_color= (255, 204, 0) # 黄色
        ),
        Button(
            DIFFICULTY_MAPPING[2],
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 0.5 * vertical_spacing,
            choose_expert,
            hover_color=(255, 0, 0)  # 红色
            ),
        Button(
            DIFFICULTY_MAPPING[3],
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 1.5 * vertical_spacing,
            choose_master,
            hover_color=(128, 0, 128)  # 紫色
            )]

    buttons.append(
        Button(
            "返回主菜单",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.8,
            lambda: setattr(config, "position", "main_menu")
        )
    )

    # 绘制动态元素
    while True:
        # 检查状态变化
        if config.position != "difficulty_selection":
            return

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                for button in buttons:
                    button.check_click()

        # 绘制按钮
        for button in buttons:
            button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

def enter_game():
    print("是否首次游玩：", config.first_play[config.difficulty])
    if config.first_play[config.difficulty]:
        config.position = "help"
    else:
        config.position = "game"