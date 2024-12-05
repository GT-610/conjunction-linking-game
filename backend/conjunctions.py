# 难度联结词表
DIFFICULTY_CONJUNCTIONS = {
    "easy": ["同或"],
    "advanced": ["异或", "与"],
    "master": ["与"]
}

def AND(a, b):
    return a & b  # 按位与

def XOR(a, b):
    return a ^ b  # 按位异或

def XNOR(a, b): # 同或
    return a == b

# 映射联结词到函数
CONJUNCTIONS = {
    "与": AND,
    "或": OR,
    "异或": XOR,
    "同或": XNOR
}
