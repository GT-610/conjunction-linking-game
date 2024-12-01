import numpy as np
# 生成地图
def generate_map(mapSize):
    # 块类型只有0和1，所以只需要生成2种块
    total = mapSize ** 2
    map = np.linspace(0, 2, total, endpoint = False, dtype=int)
    np.random.shuffle(map) # 洗牌
    return map.reshape((mapSize, mapSize))
 

# 当前地图中，如果没有可连通路线、进入死局时，将现有的图标进行打散重新洗牌。
def shuffleMap(map, mapSize):
    icons_arr = map.flatten() # 先转化为一维数组，便于操作
    map = np.array([i for i in icons_arr if i >= 0])
    np.random.shuffle(map) # 只洗有效块
    map = np.pad(map, (0, mapSize ** 2 - len(map)), 'constant', constant_values= -1 ) # 补齐剩下地图的值-1
    return map.reshape((mapSize, mapSize))

