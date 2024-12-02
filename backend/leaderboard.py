import json
import os
from time import time

# 文件路径
LEADERBOARD_FILE = f"saves/leaderboard.json"

# 默认的排行榜结构
DEFAULT_LEADERBOARD = {
    "last_updated": int(time()),  # 最后更新时间
    "records": []                # 记录
}

# 加载
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard(DEFAULT_LEADERBOARD)
    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)

# 保存
def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_record(username, difficulty, play_time, play_date):
    """
    添加新记录到排行榜。
    :param username: 用户名 (str)
    :param difficulty: 难度 (0-2)
    :param play_time: 通关时间 (秒)
    :param play_date: 游玩日期 (UNIX 时间戳)
    """
    leaderboard = load_leaderboard()
    new_record = {
        "username": username,
        "difficulty": difficulty,
        "time": play_time,
        "date": play_date
    }
    leaderboard["records"].append(new_record)
    leaderboard["last_updated"] = int(time())  # 更新最后修改时间
    save_leaderboard(leaderboard)

def get_sorted_leaderboard(sort_key="time", difficulty=None):
    """
    获取排行榜，按指定键排序。
    :param sort_key: 排序字段 (默认按通关时间)
    :param difficulty: 如果指定，则仅返回该难度的记录
    :return: 排序后的记录列表
    """
    leaderboard = load_leaderboard()
    records = leaderboard["records"]
    if difficulty is not None:
        records = [r for r in records if r["difficulty"] == difficulty]
    return sorted(records, key=lambda r: r[sort_key])

def clear_leaderboard():
    # 清空排行榜数据
    save_leaderboard(DEFAULT_LEADERBOARD)
