import pygame
import sys
from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, small_font, Button, WHITE, BLACK
from backend.leaderboard import save_to_leaderboard
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

    # 保存排行榜数据
    save_to_leaderboard(config.username, config.difficulty, config.elapsed_time, config.final_score, config.is_cleared)

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

        # 通关状态
        cleared_text = "通关" if config.is_cleared else "未通关"
        cleared_color = (0, 255, 0) if config.is_cleared else (255, 0, 0)  # 成功为绿色，失败为红色
        cleared_text_rendered = font.render(cleared_text, True, cleared_color)
        cleared_rect = cleared_text_rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(cleared_text_rendered, cleared_rect)

        # 分数
        score_text = small_font.render(f"分数: {final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(score_text, score_rect)

        # 时间
        time_text = small_font.render(f"用时: {elapsed_time}秒", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(time_text, time_rect)

        # 按钮
        return_main_menu_button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

def return_to_main_menu():
    from frontend.pages.main_menu import main_menu
    main_menu()
