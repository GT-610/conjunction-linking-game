import pygame
import sys
import time
pygame.font.init()

from frontend.commons import screen, SCREEN_WIDTH, font, small_font, WHITE, Button
from backend.leaderboard import load_leaderboard, get_sorted_leaderboard
from backend.config import config, DIFFICULTY_MAPPING

# 排行榜界面
def leaderboard_page():
    # 背景
    from frontend.commons import BgManager
    bg = BgManager("assets/backgrounds/bgLeaderboard.png", 100)
    bg.draw(screen)
    
    # 显示加载中
    loading_text = font.render("加载中...", True, (255, 255, 255))
    screen.blit(loading_text, (screen.get_width() // 2 - loading_text.get_width() // 2, screen.get_height() // 2))
    pygame.display.update()

    bg.draw(screen)
    del bg, BgManager

    # 加载排行榜数据
    leaderboard_data = load_leaderboard()

    # 显示更新时间
    last_updated_time = leaderboard_data.get("last_updated", 0)
    if last_updated_time:
        last_updated_text = f"更新时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_updated_time))}"
    else:
        last_updated_text = "尚未更新过排行榜"
    last_updated_rendered = small_font.render(last_updated_text, True, WHITE)
    screen.blit(last_updated_rendered, (screen.get_width() - last_updated_rendered.get_width() - 20, 10))

    # 获取排行榜记录
    records = leaderboard_data.get("records", [])
    if not records:
        no_records_text = font.render("还没有记录哦", True, WHITE)
        no_records_rect = no_records_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(no_records_text, no_records_rect)
    else:
        # 表格化数据
        sorted_records = get_sorted_leaderboard()
        y_offset = 80  # 起始 y 位置
        header_font = pygame.font.Font("assets/fonts/SourceHanSansCN-Regular.otf", 36)
        table_font = pygame.font.Font("assets/fonts/SourceHanSansCN-Regular.otf", 28)
        
        # 绘制表头
        headers = ["用户名", "通关", "难度", "日期", "分数"]
        header_x_positions = [100, 300, 500, 650, 1050]  # 每列起始 x 坐标
        for i, header in enumerate(headers):
            header_text = header_font.render(header, True, WHITE)
            screen.blit(header_text, (header_x_positions[i], y_offset))
        y_offset += 40  # 表头与内容的间距

        # 绘制记录
        for record in sorted_records[:11]:
            local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record['date']))
            cleared_text = "通关" if record["is_cleared"] else "未通关"
            difficulty_text = DIFFICULTY_MAPPING[record["difficulty"]]  # 根据整数获取难度文字
            row_data = [
                record['username'],
                cleared_text,
                difficulty_text,  # 替换为对应的难度文字
                local_time,
                str(record['oscore'])
            ]
            for i, data in enumerate(row_data):
                record_text = table_font.render(data, True, WHITE)
                screen.blit(record_text, (header_x_positions[i], y_offset))
            y_offset += 35  # 每条记录之间的垂直间距

    # 绘制返回按钮
    back_button = Button(
        "返回主菜单",
        SCREEN_WIDTH // 2 - 100,
        500,
        200, 50,
        callback=lambda: setattr(config, "position", "main_menu")
    )

    while True:
        if config.position != "leaderboard":
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                back_button.check_click()  # 点击返回按钮

        # 绘制返回按钮
        back_button.draw(screen)

        pygame.display.flip()