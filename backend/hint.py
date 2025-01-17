from backend.link import getLinkType
from frontend.commons import RED, hint_sound

# 提示函数
def hint_game(map, blocks, sfx_vol):
    print("激活提示")

    hint_sound.set_volume(sfx_vol / 100)
    # 收集所有非空块的坐标
    non_empty_blocks = [(x, y) for x in range(len(map)) for y in range(len(map[x])) if map[x][y] != -1]

    # 遍历非空块的所有可能配对
    for i, (x1, y1) in enumerate(non_empty_blocks):
        for x2, y2 in non_empty_blocks[i + 1:]:
            # 检查连通性
            link_type = getLinkType(map, (x1, y1), (x2, y2))
            if link_type:
                # 找到连通块，绘制提示线
                block1 = blocks[x1][y1]
                block2 = blocks[x2][y2]

                hint_sound.play()
                from frontend.pages.game import draw_link_line
                draw_link_line(block1, block2, link_type, blocks, RED, 1000)

                return

    print("没有可提示的连通块")
