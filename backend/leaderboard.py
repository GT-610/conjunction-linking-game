import json
import os
from time import time

# 文件路径
LEADERBOARD_FILE = "saves/leaderboard.json"

# 默认的排行榜结构
DEFAULT_LEADERBOARD = {
    "last_updated": int(time()),  # 最后更新时间
    "records": []                # 记录
}

from datetime import datetime, timezone

# 加载排行榜
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_to_leaderboard(DEFAULT_LEADERBOARD)
    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)

# 保存新记录到排行榜
def save_to_leaderboard(username, difficulty, play_time, overall_score, is_cleared):
    """
    username: 用户名 (str)
    difficulty: 难度 (0-2)
    play_time: 通关时间 (秒)
    oscore: 综合得分
    is_cleared: 是否通关 (bool)
    """

    leaderboard = load_leaderboard()

    # 构造新记录
    new_record = {
        "username": username,
        "difficulty": difficulty,
        "date": int(time()),  # 使用 UNIX 时间戳
        "is_cleared": is_cleared,
        "oscore": overall_score
    }

    # 添加新记录
    leaderboard["records"].append(new_record)
    leaderboard["last_updated"] = int(time())

    # 写入文件
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)

# 获取排行榜
def get_sorted_leaderboard():
    leaderboard = load_leaderboard()
    records = leaderboard["records"]
    # 按通关优先、综合得分降序、游玩时间降序排序
    sorted_records = sorted(
        records,
        key=lambda x: (not x["is_cleared"], -x["oscore"], -x["date"])  # 未通关排后，分数降序
    )
    return sorted_records

def clear_leaderboard():
    # 清空排行榜数据
    save_to_leaderboard(DEFAULT_LEADERBOARD)
