import pygame
import sys
from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, scale, font, small_font, Button, WHITE
from backend.leaderboard import save_to_leaderboard
from backend.config import config

def checkout_page(elapsed_time):
    # 保存排行榜数据
    overall_score = calc_overall_score(config.clear_rate, config.difficulty, elapsed_time)
    save_to_leaderboard(config.username, config.difficulty, elapsed_time, overall_score, config.is_cleared)

    # 绘制静态元素
    ## 背景
    from frontend.commons import bg0
    bg0.draw(screen)
    del bg0

    ## 通关状态
    cleared_text = "通关" if config.is_cleared else "未通关"
    cleared_color = (0, 255, 0) if config.is_cleared else (255, 0, 0)  # 成功为绿色，失败为红色
    cleared_text_rendered = font.render(cleared_text, True, cleared_color)
    screen.blit(cleared_text_rendered, ((SCREEN_WIDTH - cleared_text_rendered.get_width()) // 2, (SCREEN_HEIGHT - cleared_text_rendered.get_height()) // 4))
    del cleared_text, cleared_color, cleared_text_rendered

    ## 完成度
    cr_text = small_font.render(f"完成度: {int(config.clear_rate * 100)}%", True, WHITE)
    screen.blit(cr_text, ((SCREEN_WIDTH - cr_text.get_width()) // 2, (SCREEN_HEIGHT - cr_text.get_height()) // 2 - 60 * scale))
    del cr_text

    ## 时间
    time_text = small_font.render(f"用时: {elapsed_time}秒", True, WHITE)
    screen.blit(time_text, ((SCREEN_WIDTH - time_text.get_width()) // 2, (SCREEN_HEIGHT - time_text.get_height()) // 2))
    del time_text

    ## 综合得分
    oscore_text = small_font.render(f"综合得分: {overall_score}", True, WHITE)
    screen.blit(oscore_text, ((SCREEN_WIDTH - oscore_text.get_width()) // 2, (SCREEN_HEIGHT - oscore_text.get_height()) // 2 + 60))
    del oscore_text, overall_score

    # 按钮
    return_main_menu_button = Button(
        "返回主菜单",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 100 * scale,
        lambda: setattr(config, "position", "main_menu")
    )

    # 通关音效
    if config.is_cleared:
        from frontend.commons import success_sound
        success_sound.set_volume(config.sfx_vol / 100)
        success_sound.play()
        del success_sound
    else:
        from frontend.commons import failure_sound
        failure_sound.set_volume(config.sfx_vol / 100)
        failure_sound.play()
        del failure_sound

    # 绘制动态元素
    while True:
        # 检查状态变化
        if config.position != "checkout":
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                return_main_menu_button.check_click()

        # 按钮
        return_main_menu_button.draw(screen)

        # 更新屏幕
        pygame.display.flip()


def calc_overall_score(clear_rate, difficulty, elapsed_time):
    import math
    # 难度影响参数调整
    x0 = 200 + 100 * difficulty  # 时间中点，难度越高衰减越慢
    k = 0.01 / (difficulty + 1)  # Sigmoid 曲线陡峭度，难度越高越平缓

    # 计算时间权重
    sigmoid = 1 / (1 + math.exp(-k * (elapsed_time - x0)))
    time_weight = 1 - sigmoid  # 反向处理，时间越大，权重越小

    # 清除率权重，平方放大高达成率
    clear_weight = clear_rate ** 2

    # 综合得分公式
    overall_score = (difficulty + 1) * clear_weight * time_weight * 1000

    # 保证最低得分为0
    return max(0, int(overall_score))