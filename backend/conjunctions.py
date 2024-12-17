# 难度联结词表
DIFFICULTY_CONJUNCTIONS = [
    ["与", "或非", "蕴含"],
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

# 生成真值表
def calculate_truth_table(conjunctions):
    truth_table = [("A", "B") + tuple(conjunctions)]  # 表头
    truth_values = [(True, True), (True, False), (False, True), (False, False)]  # A 和 B 的所有可能值

    for a, b in truth_values:
        row = (str(a), str(b))  # A 和 B 的值
        for conj in conjunctions:
            result = CONJUNCTIONS[conj](a, b)  # 使用对应函数计算结果
            row += (str(result),)
        truth_table.append(row)
    
    return truth_table
