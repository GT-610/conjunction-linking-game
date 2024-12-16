import pygame
import sys
pygame.init()

from frontend.commons import screen, SCREEN_WIDTH, font
from frontend.commons import Button, small_font, Slider, TextInputBox
from frontend.commons import WHITE, bg

from backend.config import config, save_settings

# 设置界面
def settings_page():
    # 滑块实例
    bgm_slider = Slider(SCREEN_WIDTH // 2 - 100, 200, 200, initial_value=50)
    sfx_slider = Slider(SCREEN_WIDTH // 2 - 100, 300, 200, initial_value=50)
    name_input = TextInputBox(SCREEN_WIDTH // 2 - 100, 400, 200, 40, text=config.username)

    # 返回按钮
    from frontend.pages.main_menu import main_menu
    def back_button_callback():
        save_settings(config)
        main_menu()
    back_button = Button("返回主菜单", SCREEN_WIDTH // 2 - 100, 500, 200, 50, callback=back_button_callback)

    # 确认按钮
    def confirm_button_callback():
        config.username = name_input.text # 传递修改内容给配置实例
        print(f"用户名已更改为：{config.username}")
    confirm_button = Button("确认", 750, 395, 100, 50, callback=confirm_button_callback)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 滑块事件处理
            bgm_slider.handle_event(event)
            sfx_slider.handle_event(event)
            # 文本框事件处理
            name_input.handle_event(event)
            # 按钮点击处理
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                back_button.check_click()
                confirm_button.check_click()

        # 背景
        bg.draw(screen)

        # 绘制标题
        title_surface = font.render("设置", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 绘制滑块和文本框
        bgm_slider.draw(screen)
        sfx_slider.draw(screen)
        name_input.draw(screen)

        # 显示音量和玩家名称
        bgm_text = small_font.render(f"背景音乐音量: {int(bgm_slider.value)}", True, WHITE)
        screen.blit(bgm_text, (SCREEN_WIDTH // 2 - 150, 140))
        sfx_text = small_font.render(f"音效音量: {int(sfx_slider.value)}", True, WHITE)
        screen.blit(sfx_text, (SCREEN_WIDTH // 2 - 150, 240))

        name_text = small_font.render("玩家名称（修改后点击确认才能保存）:", True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 300, 340))

        # 绘制返回按钮
        back_button.draw(screen)
        # 绘制确认按钮
        confirm_button.draw(screen)  # 假设你有一个 confirm_button 对象

        # 更新显示
        pygame.display.flip()
