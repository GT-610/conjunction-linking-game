import pygame
import sys
import time
pygame.font.init()

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, scale, font, small_font, WHITE, Button, button_width, assets_dir
from backend.leaderboard import load_leaderboard, get_sorted_leaderboard
from backend.config import config, DIFFICULTY_MAPPING

# 排行榜界面
def leaderboard_page():
    # 背景
    from frontend.commons import BgManager
    bg = BgManager(assets_dir/"backgrounds"/"bgLeaderboard.png", 100)
    bg.draw(screen)
    
    # 显示加载中
    loading_text = font.render("加载中...", True, (255, 255, 255))
    screen.blit(loading_text, ((SCREEN_WIDTH - loading_text.get_width()) // 2, (SCREEN_HEIGHT - loading_text.get_height()) // 2))
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
    screen.blit(last_updated_rendered, (SCREEN_WIDTH - last_updated_rendered.get_width() - 20, 10))

    # 获取排行榜记录
    records = leaderboard_data.get("records", [])
    if not records:
        no_records_text = font.render("还没有记录哦", True, WHITE)
        screen.blit(no_records_text, ((SCREEN_WIDTH - no_records_text.get_width()) // 2, (SCREEN_HEIGHT - no_records_text.get_height()) // 2))
        del no_records_text
    else:
        # 表格化数据
        sorted_records = get_sorted_leaderboard()
        y_offset = 80 * scale  # 起始 y 位置
        header_font = small_font
        table_font = pygame.font.Font("assets/fonts/SourceHanSansCN-Regular.otf", int(28 * scale))
        
        # 绘制表头
        headers = ["用户名", "通关状态", "难度", "日期", "分数"]
        header_x_pos = [100, 300, 500, 650, 1050]  # 每列起始 x 坐标
        header_x_pos = [pos * scale for pos in header_x_pos]
        for i, header in enumerate(headers):
            header_text = header_font.render(header, True, WHITE)
            screen.blit(header_text, (header_x_pos[i], y_offset))
        y_offset += 40 * scale  # 表头与内容的间距

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
                screen.blit(record_text, (header_x_pos[i], y_offset))
            y_offset += 35 * scale  # 每条记录之间的垂直间距

    # 绘制返回按钮
    back_button = Button(
        "返回主菜单",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT * 0.8,
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