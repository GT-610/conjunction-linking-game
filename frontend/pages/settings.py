import pygame
import sys

from frontend.commons import screen, SCREEN_WIDTH, scale, font
from frontend.commons import Button, small_font, Slider, TextInputBox
from frontend.commons import WHITE, assets_dir, BgManager

from backend.config import config, save_settings

# 设置界面
def settings_page():
    # 滑块实例
    sfx_slider = Slider(SCREEN_WIDTH // 2, 260 * scale, 300 * scale, initial_value=config.sfx_vol)
    name_input = TextInputBox(SCREEN_WIDTH // 2, 380 * scale, 200 * scale, 40 * scale, text=config.username)

    # 返回按钮
    back_button = Button(
        "返回主菜单",
        SCREEN_WIDTH // 2, 500 * scale,
        callback=lambda: setattr(config, "position", "main_menu"))

    # 背景
    bg = BgManager(assets_dir/"backgrounds"/"bgSettings.png", 100)

    while True:
        if config.position != "settings":
            config.sfx_vol = int(sfx_slider.value)
            config.username = name_input.text
            save_settings(config)
            print("已保存设置")
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 滑块事件处理
            sfx_slider.handle_event(event)
            # 文本框事件处理
            name_input.handle_event(event)
            # 按钮点击处理
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                back_button.check_click()

        # 绘制背景
        bg.draw(screen)

        # 绘制标题
        title_surface = font.render("设置", True, WHITE)
        screen.blit(title_surface, ((SCREEN_WIDTH - title_surface.get_width()) // 2, 100 * scale))
        del title_surface

        # 绘制滑块和文本框
        sfx_slider.draw(screen)
        name_input.draw(screen)

        # 绘制音量和玩家名称
        sfx_text = small_font.render(f"音效音量: {int(sfx_slider.value)}", True, WHITE)
        screen.blit(sfx_text, ((SCREEN_WIDTH - sfx_text.get_width()) // 2, 190 * scale))

        name_text = small_font.render("玩家名称", True, WHITE)
        screen.blit(name_text, ((SCREEN_WIDTH - name_text.get_width()) // 2, 300 * scale))

        # 绘制返回按钮
        back_button.draw(screen)

        # 更新显示
        pygame.display.flip()