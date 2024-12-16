import pygame
from backend.config import config

from frontend.pages.checkout import checkout_page
from frontend.pages.difficulty_selection import difficulty_selection_page
from frontend.pages.game import game_page
from frontend.pages.help import help_page
from frontend.pages.main_menu import main_menu
from frontend.pages.leaderboard import leaderboard_page
from frontend.pages.settings import settings_page

# 初始化 pygame
pygame.init()
pygame.display.set_caption("联结词连连看 v0.92-alpha")

# 页面映射
PAGE_MAPPING = {
    "checkout": checkout_page,
    "difficulty_selection": difficulty_selection_page,
    "game":game_page,
    "help":help_page,
    "main_menu": main_menu,
    "leaderboard": leaderboard_page,
    "settings": settings_page,
}

if __name__ == "__main__":
    # 初始页面状态
    config.position = "main_menu"

    # 状态管理主循环
    while True:
        # 根据当前状态调用相应页面
        current_page = config.position
        if current_page in PAGE_MAPPING:
            PAGE_MAPPING[current_page]()
        else:
            print(f"未知页面：{current_page}")
            break
