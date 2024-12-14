import pygame
import sys

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font
from frontend.commons import Button, button_width, button_height
from frontend.commons import vertical_spacing
from frontend.commons import BLACK, GRAY, WHITE

# 导入其他页面
from frontend.pages.difficulty_selection import difficulty_selection_page
from frontend.pages.settings import settings_page
from frontend.pages.leaderboard import leaderboard_page

from backend.config import config, load_settings

# 初始化 pygame
pygame.init()
pygame.display.set_caption("连连看")

# 主菜单
def main_menu():

    settings = load_settings()
    if "username" in settings:
        config.username = settings["username"]  # 如果配置文件中有用户名，加载它
    del settings

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


# 退出游戏
def quit_game():
    pygame.quit()
    sys.exit()
