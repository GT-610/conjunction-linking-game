# 难度联结词表
DIFFICULTY_CONJUNCTIONS = [
    ["或非", "与", "蕴含"],
    ["与", "或非"],
    ["蕴含"]
]

def AND(a, b):
    return a and b  # 与

def NOR(a, b):
    return not (a or b)  # 或非

def IMP(a, b):
    return not a or b  # 蕴含

# 映射联结词到函数
CONJUNCTIONS = {
    "与": AND,
    "或非": NOR,
    "蕴含": IMP
}
