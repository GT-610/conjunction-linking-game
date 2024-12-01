# “点”使用元组存储，(x,y)

# 比较两个点是否相等
def is_equal(p1, p2):
    return p1 == p2

# 判断一个点是否可用
def is_usable(point):
    return point[0] >= 0 and point[1] >= 0

# 克隆一个点
def clone_point(point):
    return tuple(point)  # 元组本身是不可变的，直接返回副本

# 改变一个点的值（需要注意：元组是不可变的，不能直接修改）
def change_point(point, new_point):
    return new_point

# 打印点信息
def point_repr(point):
    return f"x={point[0]}, y={point[1]}"
