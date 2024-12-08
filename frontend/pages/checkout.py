import pygame
import sys
from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, button_font, Button, WHITE, BLACK
from backend.leaderboard import save_leaderboard
from backend.config import config

def checkout_page(final_score, elapsed_time):
    pygame.init()

    # 标题字体
    title_font = pygame.font.Font(None, 64)

    # 按钮：返回主菜单
    return_main_menu_button = Button(
        "返回主菜单",
        SCREEN_WIDTH // 2 - 100,
        SCREEN_HEIGHT - 100,
        200, 50,
        return_to_main_menu
    )

    # # 调用排行榜存储函数（目前留空）
    # save_to_leaderboard(final_score, elapsed_time)

    # 绘制界面
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                return_main_menu_button.check_click()

        # 背景颜色
        screen.fill(BLACK)

        # 标题
        title_text = font.render("游戏结束", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # 分数
        score_text = button_font.render(f"分数: {final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(score_text, score_rect)

        # 时间
        time_text = button_font.render(f"用时: {elapsed_time}秒", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(time_text, time_rect)

        # 按钮
        return_main_menu_button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

def return_to_main_menu():
    from frontend.pages.main_menu import main_menu
    main_menu()
