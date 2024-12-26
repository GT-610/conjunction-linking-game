import pygame
import sys

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, scale, font, small_font
from frontend.commons import Button, button_width, vertical_spacing
from frontend.commons import WHITE

from backend.config import ver, minver, config, load_settings

# 主菜单
def main_menu():
    settings = load_settings()
    config.username = settings["username"]
    config.sfx_vol = settings["sfx_vol"]
    config.first_play = settings["first_play"]
    del settings

    # 绘制静态元素
    ## 背景
    from frontend.commons import bg0
    bg0.draw(screen)
    del bg0

    ## 文字
    title= font.render("联结词连连看", True, WHITE)
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, (125 - title.get_height()) * scale))
    del title

    welcome_text = small_font.render(f"欢迎回来，{config.username}！", True, WHITE)
    screen.blit(welcome_text, (SCREEN_WIDTH * 0.65, 15 * scale))
    del welcome_text

    if minver:
        ver_text = small_font.render(f"Ver. {ver}-{minver}", True, WHITE)
    else:
        ver_text = small_font.render(f"Ver. {ver}", True, WHITE)
    screen.blit(ver_text, (SCREEN_WIDTH - (20 + 1.5 * ver_text.get_width()) * scale, SCREEN_HEIGHT - (20 + 1.5 * ver_text.get_height()) * scale))
    del ver_text

    # 创建按钮
    buttons = [
        Button(
            "开始游戏",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 1.5 * vertical_spacing,
            lambda: setattr(config, "position", "difficulty_selection")
        ),
        Button(
            "排行榜",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 0.5 * vertical_spacing,
            lambda: setattr(config, "position", "leaderboard")
        ),
        Button(
            "设置",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 0.5 * vertical_spacing,
            lambda: setattr(config, "position", "settings")
        ),
        Button(
            "退出游戏",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 1.5 * vertical_spacing,
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
