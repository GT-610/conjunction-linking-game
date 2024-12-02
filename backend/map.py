import numpy as np
# 生成地图
# 生成地图
def generate_map(map_size):
    # 块类型只有0和1，所以只需要生成两种块
    total = map_size ** 2
    map = np.linspace(0, 2, total, endpoint=False, dtype=int)
    np.random.shuffle(map)  # 洗牌
    map = map.reshape((map_size, map_size))

    # 在地图四周添加一圈值为-1的边界
    return np.pad(map, pad_width=1, mode='constant', constant_values=-1)


# 当前地图中，如果没有可连通路线、进入死局时，将现有的图标进行打散重新洗牌。
def shuffle_map(map):
    # 提取内部有效块（去除边界的部分）
    inner_map = map[1:-1, 1:-1].flatten()  # 去掉边界并展平为一维数组
    inner_map = np.array([i for i in inner_map if i >= 0])  # 仅保留非负值的有效块

    # 洗牌有效块
    np.random.shuffle(inner_map)

    # 将洗牌后的块重新填回内部区域
    reshaped_inner_map = np.pad(inner_map, 
                                (0, (map.shape[0] - 2)**2 - len(inner_map)), 
                                'constant', constant_values=-1)  # 补齐为-1
    reshaped_inner_map = reshaped_inner_map.reshape(map.shape[0] - 2, map.shape[1] - 2)

    # 构造完整的地图，保留边界
    map[1:-1, 1:-1] = reshaped_inner_map

    return map

