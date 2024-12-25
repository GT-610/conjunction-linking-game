import numpy as np
import random

from backend.conjunctions import DIFFICULTY_CONJUNCTIONS, CONJUNCTIONS

def generate_valid_values(map_size, difficulty):
    valid_values = []
    for conj in DIFFICULTY_CONJUNCTIONS[difficulty]:
        for a in [0, 1]:
            for b in [0, 1]:
                if CONJUNCTIONS[conj](a, b):  # 如果逻辑值满足消除条件
                    valid_values.append(1)  # 满足条件为1
                else:
                    valid_values.append(0)  # 不满足条件为0

    # 确保生成的逻辑值有足够数量
    total_values = map_size ** 2
    values = random.choices(valid_values, k=total_values)
    return values

def generate_map(difficulty, map_size):
    while True:
        values = generate_valid_values(map_size, difficulty)

        # 将生成的值随机打乱并转换为 NumPy 矩阵
        np_values = np.array(values, dtype=np.int8)
        np.random.shuffle(np_values)  # 随机打乱逻辑值
        reshaped_map = np_values.reshape((map_size, map_size))  # 转换为二维矩阵
        
        if test_map_solution(reshaped_map):  # 验证是否有解
            print("已验证有解")
            break

    # 添加边界填充，pad 使用值 -1
    padded_map = np.pad(reshaped_map, pad_width=1, mode='constant', constant_values=-1)
    return padded_map

def test_map_solution(map):
    # 验证是否至少存在一对可消除的块
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


# # 生成地图
# def generate_map(mapSize):
#     # 块类型只有0和1，所以只需要生成2种块
#     total = mapSize ** 2
#     map = np.linspace(0, 2, total, endpoint = False, dtype=np.int8)
#     np.random.shuffle(map) # 洗牌
#     return np.pad(map.reshape((mapSize, mapSize)), pad_width=1, mode='constant', constant_values=-1)
 

# 洗牌
def shuffle_map(map, mapSize):
    inner_map = map[1:-1, 1:-1].flatten() # 去除边界
    map = np.array([i for i in icons_arr if i >= 0])
    np.random.shuffle(map) # 只洗有效块
    map = np.pad(map, (0, mapSize ** 2 - len(map)), 'constant', constant_values= -1 ) # 补齐剩下地图的值-1
    map[1:-1, 1:-1] = map.reshape((map.shape[0] - 2, map.shape[1] - 2))

    return map
