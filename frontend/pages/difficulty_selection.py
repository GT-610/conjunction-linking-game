import pygame
import sys
pygame.init()

from frontend.commons import screen, SCREEN_WIDTH, SCREEN_HEIGHT, Button, font, BLACK, WHITE, GRAY

difficulty = None

# 选择难度界面
def difficulty_selection_page():
    # 按钮参数
    button_width = 200
    button_height = 50
    vertical_spacing = 80

    from frontend.pages.game import game_page
    global difficulty
    # 按钮回调函数
    def choose_easy():
        difficulty = "easy"
        game_page(difficulty)
        print("已选择简单难度")

    def choose_advanced():
        difficulty = "advanced"
        game_page(difficulty)
        print("已选择高级难度")

    def choose_master():
        difficulty = "master"
        game_page(difficulty)
        print("已选择大师难度")

    # 创建按钮
    buttons = [
        Button(
            "初级",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 - vertical_spacing,
            button_width, button_height,
            callback=choose_easy,
            hover_color=(0, 255, 0)  # 绿色
        ),  
        Button(
            "高级",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2,
            200, 50,
            callback=choose_advanced,
            hover_color=(255, 0, 0)  # 红色
            ),
        Button(
            "大师",
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + vertical_spacing,
            200, 50,
            callback=choose_master,
            hover_color=(128, 0, 128)  # 紫色
            )]
    
    from frontend.pages.main_menu import main_menu
    buttons.append(Button("返回主菜单", 300, 440, 200, 50, callback=main_menu))

    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                for button in buttons:
                    button.check_click()

        # 绘制界面
        screen.fill(BLACK)

        # 绘制标题
        title_surface = font.render("选择难度", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 绘制按钮
        for button in buttons:
            button.draw(screen)

        # 更新屏幕
        pygame.display.flip()
