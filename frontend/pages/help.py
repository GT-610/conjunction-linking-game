import pygame
from frontend.commons import screen, scale, config, WHITE, YELLOW, font, small_font, bg0, SCREEN_WIDTH, SCREEN_HEIGHT, Button

from backend.config import config, DIFFICULTY_MAPPING
from backend.conjunctions import DIFFICULTY_CONJUNCTIONS, calculate_truth_table

def help_page(in_game=False):
    # 获取当前难度的联结词
    conjunctions = DIFFICULTY_CONJUNCTIONS[config.difficulty]
    # 根据当前难度计算真值表
    truth_table = calculate_truth_table(conjunctions)
    del conjunctions

    # 背景
    bg0.draw(screen)

    # 绘制标题
    title = font.render(f"{DIFFICULTY_MAPPING[config.difficulty]}难度游玩说明", True, WHITE)
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 50 * scale))

    # 绘制游玩提示
    tip = {
        WHITE: ["按顺序选择正确的两个块和联结词，使其真值为 1。", "以消除所有块为通关目标吧！"],
        YELLOW: ["可以选择不同的联结词配对哦！"]
    }
    row = 0
    for color, messages in tip.items():
        for message in messages:
            tip_text = small_font.render(message, True, color)
            screen.blit(tip_text, ((SCREEN_WIDTH - tip_text.get_width()) // 2, (440 + row * 50) * scale))
            row += 1
    del row

    # 绘制真值表
    column_widths = []
        ## 计算每列的最大宽度
    for j in range(len(truth_table[0]) - 1):
        max_width = max(small_font.render(row[j], True, WHITE).get_width() for row in truth_table)
        column_widths.append((max_width + 50) * scale)  # 将最大宽度乘以缩放系数
    ## 计算表格总宽度
    table_width = sum(column_widths)
    ## 计算居中起始点
    table_x_start = (SCREEN_WIDTH - table_width) // 2
    ## 绘制表格内容
    for i, row in enumerate(truth_table):
        for j, cell in enumerate(row):
            if i == 0:
                cell_text = cell
            else:
                cell_text = '1' if cell == "True" else '0'
            cell_text_rendered = small_font.render(cell_text, True, WHITE)
            # 动态计算每个单元格的 x 坐标
            cell_x = table_x_start + sum(column_widths[:j])  # 计算当前列的起始 x 坐标
            cell_y = (150 + i * 40) * scale  # 每行固定高度
            screen.blit(cell_text_rendered, (cell_x, cell_y))
    del column_widths, table_width, table_x_start

    # 如果是通过游戏内进入，显示“返回”按钮
    if in_game:            
        return_button = Button(
            "返回",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100 * scale,
            exit_help_page
        )

        paused_text = small_font.render("游戏暂停中", True, WHITE)
        screen.blit(paused_text, (30 * scale, 90 * scale))

    # 如果是首次进入，显示“开始游戏”按钮
    else:
        start_game_button = Button(
            "开始游戏",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100 * scale,
            first_enter_game
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

        # 绘制按钮
        if in_game:
            return_button.draw(screen)
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
