import pygame
from frontend.commons import screen, WHITE, YELLOW, font, small_font, bg0, SCREEN_WIDTH, SCREEN_HEIGHT, Button
from frontend.pages.game import game_page

from backend.config import config, navigate_with_params, DIFFICULTY_MAPPING
from backend.conjunctions import DIFFICULTY_CONJUNCTIONS, calculate_truth_table

def help_page(in_game=False, game_state=None):
    # 获取当前难度的联结词
    conjunctions = DIFFICULTY_CONJUNCTIONS[config.difficulty]
    # 根据当前难度计算真值表
    truth_table = calculate_truth_table(conjunctions)
    del conjunctions

    # 如果是通过游戏内进入，显示“返回”按钮
    if in_game:            
        return_button = Button(
            text="返回",
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            callback=exit_help_page
        )

        paused_text = small_font.render("游戏暂停中", True, WHITE)
        paused_rect = paused_text.get_rect(topleft=(30, 100))

    # 如果是首次进入，显示“开始游戏”按钮
    else:
        start_game_button = Button(
            text="开始游戏",
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            callback=first_enter_game
        )

    while True:
        if config.position != "help":
            return

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 处理退出事件
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 检测鼠标点击
                if in_game:
                    return_button.check_click()
                else:
                    start_game_button.check_click()

        # 背景
        bg0.draw(screen)

        # 绘制标题
        title = font.render(f"{DIFFICULTY_MAPPING[config.difficulty]}难度游玩说明", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # 绘制真值表
        column_spacing = 150  # 列间距
        table_x_start = SCREEN_WIDTH // 2 - (len(truth_table[0]) - 1) * column_spacing // 2  # 居中起始点

        # 绘制游玩提示
        tip = {
            WHITE: ["按顺序选择正确的两个块和联结词，使其真值为 True。", "以消除所有块为通关目标吧！"],
            YELLOW: ["可以选择不同的联结词配对哦！"]
        }

        row = 0
        for color, messages in tip.items():
            for message in messages:
                tip_text = small_font.render(message, True, color)
                screen.blit(tip_text, (SCREEN_WIDTH // 2 - tip_text.get_width() // 2, 450 + row * 50))
                row += 1
        del row

        for i, row in enumerate(truth_table):
            for j, cell in enumerate(row):
                cell_text = small_font.render(cell, True, WHITE)
                cell_x = table_x_start + j * column_spacing  # 每列增加列间距
                cell_y = 150 + i * 40  # 每行固定高度
                screen.blit(cell_text, (cell_x, cell_y))

        # 绘制按钮
        if in_game:
            return_button.draw(screen)
            screen.blit(paused_text, paused_rect)
        else:
            start_game_button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

def exit_help_page():
    config.position = "game"
    from frontend.pages.game import pause_game
    pause_game()

def first_enter_game():
    config.first_play[config.difficulty] = False
    print("首次游玩设定已改为：", config.first_play[config.difficulty])

    from backend.config import save_settings
    save_settings(config)
    del save_settings
    
    config.position = "game"
