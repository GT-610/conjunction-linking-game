import json
import os
import time

# 文件路径
LEADERBOARD_FILE = f"saves/leaderboard.json"

# 默认的排行榜结构
DEFAULT_LEADERBOARD = {
    "last_updated": int(time.time()),  # 最后更新时间
    "records": []                # 记录
}

import json
import os
import time
from datetime import datetime, timezone

LEADERBOARD_FILE = "saves/leaderboard.json"
DEFAULT_LEADERBOARD = {"records": [], "last_updated": 0}

# 加载排行榜
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard(DEFAULT_LEADERBOARD)
    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)

# 保存新记录到排行榜
def save_to_leaderboard(username, difficulty, play_time, score):
    """
    username: 用户名 (str)
    difficulty: 难度 (0-2)
    play_time: 通关时间 (秒)
    score: 游戏得分 (int)
    """

    leaderboard = load_leaderboard()

    # 构造新记录
    new_record = {
        "username": username,
        "difficulty": difficulty,
        "time": play_time,
        "date": datetime.now(timezone.utc).isoformat(),  # 使用 ISO 格式保存时间
        "score": score
    }

    # 添加新记录
    leaderboard["records"].append(new_record)
    leaderboard["last_updated"] = int(time.time())

    # 写入文件
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)


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
    save_to_leaderboard(DEFAULT_LEADERBOARD)
