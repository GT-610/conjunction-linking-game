import pygame
pygame.init()

from backend.link import getLinkType
from frontend.commons import screen, GREEN, BLACK, RED

# 提示（占位函数）
def hint_game(map, blocks):
    print("激活提示")
    from frontend.pages.game import draw_link_line
    # 遍历地图寻找可以连通的一对块
    for x1 in range(10):
        for y1 in range(10):
            for x2 in range(10):
                for y2 in range(10):
                    # 跳过空块或相同位置
                    if (x1, y1) == (x2, y2) or map[x1][y1] == -1 or map[x2][y2] == -1:
                        continue
                    
                    # 检查连通性
                    link_type = getLinkType(map, (x1, y1), (x2, y2))
                    if link_type:
                        # 找到连通块，绘制提示线
                        block1 = blocks[x1][y1]
                        block2 = blocks[x2][y2]

                        draw_link_line(block1, block2, link_type, blocks, RED)
                        pygame.display.update()

                        # 延迟一段时间后清除提示
                        pygame.time.delay(1000)  # 提示线显示 1 秒
                        return

    print("没有可提示的连通块")