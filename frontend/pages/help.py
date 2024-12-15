import pygame
from frontend.commons import screen, BLACK, WHITE, YELLOW, font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT, Button

from backend.config import config, DIFFICULTY_MAPPING
from backend.conjunctions import DIFFICULTY_CONJUNCTIONS, calculate_truth_table

def help_page():
    # 获取当前难度的联结词
    conjunctions = DIFFICULTY_CONJUNCTIONS[config.difficulty]
    # 根据当前难度计算真值表
    truth_table = calculate_truth_table(conjunctions)
    del conjunctions

    # 创建按钮实例
    start_game_button = Button(
        text="开始游戏",
        x=SCREEN_WIDTH // 2 - 100,
        y=SCREEN_HEIGHT - 100,
        width=200,
        height=50,
        callback=first_enter_game
    )

    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 处理退出事件
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 检测鼠标点击
                start_game_button.check_click()

        # 绘制帮助页面内容
        screen.fill((0, 0, 0))  # 清屏为黑色背景

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
        start_game_button.draw(screen)

        # 更新屏幕
        pygame.display.flip()

def first_enter_game():
    config.first_play[config.difficulty] = False
    print("首次游玩设定已改为：", config.first_play[config.difficulty])

    from backend.config import save_settings
    save_settings(config)
    del save_settings
    
    from frontend.pages.game import game_page
    game_page()
