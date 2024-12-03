import pygame
import sys
import time
pygame.init()

from frontend.commons import screen, font, BLACK, WHITE, GRAY, Button
from backend.leaderboard import load_leaderboard, save_leaderboard, get_sorted_leaderboard

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
    from frontend.pages.main_menu import main_menu
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
