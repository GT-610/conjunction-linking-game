import pygame
import sys

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, small_font
from frontend.commons import Button, button_width, button_height
from frontend.commons import vertical_spacing
from frontend.commons import WHITE

from backend.config import config, load_settings

pygame.init()

# 主菜单
def main_menu():
    settings = load_settings()
    if "username" in settings:
        config.username = settings["username"]
    if "first_play" in settings:
        config.first_play = settings["first_play"]
    del settings

    # 绘制静态元素
    ## 背景
    from frontend.commons import bg0
    bg0.draw(screen)
    del bg0

    ## 文字
    title_surface = font.render("游戏主菜单", True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surface, title_rect)
    del title_surface, title_rect

    text_surface = small_font.render(f"欢迎回来，{config.username}！", True, WHITE)
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # 右上角，留些边距
    screen.blit(text_surface, text_rect)
    del text_surface, text_rect

    # 创建按钮
    buttons = [
        Button(
            "开始游戏",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 - 1.5 * vertical_spacing,
            button_width, button_height,
            lambda: setattr(config, "position", "difficulty_selection")
        ),
        Button(
            "排行榜",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 - 0.5 * vertical_spacing,
            button_width, button_height,
            lambda: setattr(config, "position", "leaderboard")
        ),
        Button(
            "设置",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + 0.5 * vertical_spacing,
            button_width, button_height,
            lambda: setattr(config, "position", "settings")
        ),
        Button(
            "退出游戏",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + 1.5 * vertical_spacing,
            button_width, button_height,
            quit_game
        )
    ]

    # 绘制动态元素
    while True:
        # 检查状态变化
        if config.position != "main_menu":  # 状态改变，退出循环
            return

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

# 退出游戏
def quit_game():
    pygame.quit()
    sys.exit()
