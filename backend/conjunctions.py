def AND(a, b):
    return a & b  # 按位与

def OR(a, b):
    return a | b  # 按位或

def XOR(a, b):
    return a ^ b  # 按位异或

# 映射联结词到函数
CONJUNCTIONS = {
    "与": AND,
    "或": OR,
    "异或": XOR
}
