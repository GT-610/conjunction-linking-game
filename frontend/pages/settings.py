import pygame
pygame.init()

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font
from frontend.commons import Button, button_font, Slider, TextInputBox
from frontend.commons import WHITE, BLACK

# 设置界面
def settings_page():
    # 滑块实例
    bgm_slider = Slider(300, 200, 200, initial_value=50)
    sfx_slider = Slider(300, 300, 200, initial_value=50)
    name_input = TextInputBox(300, 400, 200, 40, text="玩家")

    # 返回按钮
    from frontend.pages.main_menu import main_menu
    back_button = Button("返回主菜单", 300, 500, 200, 50, callback=main_menu)

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

        # 绘制设置界面
        screen.fill(BLACK)

        # 绘制标题
        title_surface = font.render("设置", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 绘制滑块和文本框
        bgm_slider.draw(screen)
        sfx_slider.draw(screen)
        name_input.draw(screen)

        # 显示音量和玩家名称
        bgm_text = button_font.render(f"背景音乐音量: {int(bgm_slider.value)}", True, WHITE)
        screen.blit(bgm_text, (300, 140))
        sfx_text = button_font.render(f"音效音量: {int(sfx_slider.value)}", True, WHITE)
        screen.blit(sfx_text, (300, 240))

        name_text = button_font.render("玩家名称:", True, WHITE)
        screen.blit(name_text, (300, 340))

        # 绘制返回按钮
        back_button.draw(screen)

        # 更新显示
        pygame.display.flip()