import numpy as np
import random

from backend.conjunctions import DIFFICULTY_CONJUNCTIONS, CONJUNCTIONS
# 按联结词可能性生成块
def generate_valid_map(map_size, difficulty, balance_range=(0.45, 0.55)):
    valid_blocks = []
    for conj in DIFFICULTY_CONJUNCTIONS[difficulty]:
        for a in [0, 1]:
            for b in [0, 1]:
                if CONJUNCTIONS[conj](a, b):  # 逻辑为真
                    valid_blocks.append((a, b))

    total_blocks = map_size ** 2
    target_ones = int(total_blocks * random.uniform(*balance_range))
    target_zeros = total_blocks - target_ones
    blocks = []

    ones_count = 0
    zeros_count = 0

    while len(blocks) < total_blocks:
        block = random.choice(valid_blocks)
        a, b = block[0], block[1]

        # 确保生成的 1 和 0 数量符合比例
        if ones_count < target_ones and (a + b) > 0:
            blocks.append(a)
            blocks.append(b)
            ones_count += a + b
        elif zeros_count < target_zeros and (1 - a + 1 - b) > 0:
            blocks.append(a)
            blocks.append(b)
            zeros_count += (1 - a) + (1 - b)

        # 如果达到目标比例，填充剩余空位
        if len(blocks) >= total_blocks:
            break

    random.shuffle(blocks)  # 打乱
    return np.array(blocks, dtype=np.int8).reshape((map_size, map_size))

# 验证是否有解
def test_map_solution(map):
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == -1:
                continue
            for di, dj in [(0, 1), (1, 0)]:  # 检查右方和下方的块
                ni, nj = i + di, j + dj
                if ni < map.shape[0] and nj < map.shape[1]:
                    if map[ni, nj] == map[i, j]:
                        return True  # 找到一对可消除的块
    return False

def generate_map(difficulty, map_size):
    while True:
        map = generate_valid_map(map_size, difficulty)
        if test_map_solution(map):
            print("已确认地图有解")
            break

    # 添加边界填充
    padded_map = np.pad(map, pad_width=1, mode='constant', constant_values=-1)
    return padded_map

# 洗牌
def shuffle_map(map, mapSize):
    inner_map = map[1:-1, 1:-1].flatten() # 去除边界
    map = np.array([i for i in icons_arr if i >= 0]) # 去除空块
    np.random.shuffle(map)
    map = np.pad(map, (0, mapSize ** 2 - len(map)), 'constant', constant_values= -1 ) # 补齐剩下地图的值-1
    map[1:-1, 1:-1] = map.reshape((map.shape[0] - 2, map.shape[1] - 2))

    return map
