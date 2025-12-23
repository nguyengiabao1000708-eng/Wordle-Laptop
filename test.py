import json
import os
from datetime import date

class UserManager:
    def __init__(self):
        self.filename = "data_users/users.json"
        self.data = self.load_data()

    def load_data (self):
        if not os.path.exists(self.filename):
            return self.create_default_profile
        
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except(json.JSONDecodeError, IOError):
            return self.create_default_profile()

    def create_default_profile(self):
        return {
            "Player":{
                "username": "Player",
                "stats": {
                    "games_played": 0,
                    "games_won": 0,
                    "current_streak": 0,
                    "max_streak": 0,
                    "guess_distribution": {str(i): 0 for i in range(1, 7)}
                },
                "last_played": None
            }
        }
    def save_data(self):
        with open(self.filename,"w") as f:
            json.dump (self.data, f, indent= 4)

    def update_stats(self, is_win, guess_count):
        stats = self.data["Player"]["stats"]
        stats["games_played"] += 1
        self.data["Player"]["last_played"] = str(date.today())

        if is_win:
            stats["games_won"] += 1
            stats["current_streak"] += 1
            
            if stats["current_streak"] > stats["max_streak"]:
                stats["max_streak"] = stats["current_streak"]
            

            if 1 <= guess_count <= 6:
                stats["guess_distribution"][str(guess_count)] += 1
        else:
            stats["current_streak"] = 0

        self.save_data()

    def get_stats_summary(self):
        """Trả về string thống kê để in ra màn hình."""
        s = self.data["Player"]["stats"]
        win_rate = (s["games_won"] / s["games_played"] * 100) if s["games_played"] > 0 else 0
        
        return (
            f"--- THỐNG KÊ ---\n"
            f"Số trận đã chơi: {s['games_played']}\n"
            f"Tỉ lệ thắng: {win_rate:.1f}%\n"
            f"Chuỗi thắng hiện tại: {s['current_streak']}\n"
            f"Chuỗi thắng dài nhất: {s['max_streak']}"
        )
        