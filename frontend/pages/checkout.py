import pygame
import sys
from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font, small_font, Button, WHITE, BLACK
from backend.leaderboard import save_to_leaderboard
from backend.config import config

def checkout_page(elapsed_time):
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

    # 综合得分 (EXPERIMENTAL)
    overall_score = 5000 * config.clear_rate + 500 * (config.difficulty + 1) + 1800 - elapsed_time
    # 保存排行榜数据
    save_to_leaderboard(config.username, config.difficulty, elapsed_time, overall_score, config.is_cleared)

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

        # 完成度
        cr_text = small_font.render(f"完成度: {int(config.clear_rate * 100)}%", True, WHITE)
        cr_rect = cr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(cr_text, cr_rect)

        # 时间
        time_text = small_font.render(f"用时: {elapsed_time}秒", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(time_text, time_rect)

        # 综合得分
        oscore_text = small_font.render(f"综合得分: {overall_score}", True, WHITE)
        oscore_rect = oscore_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(oscore_text, oscore_rect)

        # 按钮
        return_main_menu_button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

def calc_overall_score(clear_rate, difficulty, elapsed_time):
    pass

def return_to_main_menu():
    from frontend.pages.main_menu import main_menu
    main_menu()
