import numpy as np

# 生成地图
def generate_map(mapSize):
    # 块类型只有0和1，所以只需要生成2种块
    total = mapSize ** 2
    map = np.linspace(0, 2, total, endpoint = False, dtype=int)
    np.random.shuffle(map) # 洗牌
    return np.pad(map.reshape((mapSize, mapSize)), pad_width=1, mode='constant', constant_values=-1)
 

# 当前地图中，如果没有可连通路线、进入死局时，将现有的图标进行打散重新洗牌。
def shuffle_map(map, mapSize):
    inner_map = map[1:-1, 1:-1].flatten() # 去除边界
    map = np.array([i for i in icons_arr if i >= 0])
    np.random.shuffle(map) # 只洗有效块
    map = np.pad(map, (0, mapSize ** 2 - len(map)), 'constant', constant_values= -1 ) # 补齐剩下地图的值-1
    map[1:-1, 1:-1] = map.reshape((map.shape[0] - 2, map.shape[1] - 2))

    return map
