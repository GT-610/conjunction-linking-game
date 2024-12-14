import pygame
from frontend.commons import screen, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

def help_page():
    # 绘制帮助页面内容
    font = pygame.font.Font(None, 36)
    title = font.render("联结词真值表", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    # 这里是展示真值表的部分
    truth_table = [
        ("A", "B", "A AND B"),
        ("True", "True", "True"),
        ("True", "False", "False"),
        ("False", "True", "False"),
        ("False", "False", "False")
    ]

    # 打印真值表
    for i, row in enumerate(truth_table):
        row_text = font.render(f"{row[0]}  {row[1]}  {row[2]}", True, WHITE)
        screen.blit(row_text, (SCREEN_WIDTH // 2 - row_text.get_width() // 2, 150 + i * 40))

    # 绘制“开始游戏”按钮
    start_game_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, WHITE, start_game_button)
    button_text = font.render("开始游戏", True, BLACK)
    screen.blit(button_text, (start_game_button.centerx - button_text.get_width() // 2,
                             start_game_button.centery - button_text.get_height() // 2))

    # 更新显示
    pygame.display.flip()

    return start_game_button
