import json
import os
from datetime import date

class UserManager:
    def __init__(self):
        self.filename = "data_users/users.json"
        self.data = self.load_data()

    def load_data(self):
        # Nếu chưa có file hoặc lỗi -> Trả về kho rỗng
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, "r", encoding='utf-8') as f:
                content = f.read()
                return json.loads(content) if content else {}
        except:
            return {}

    def create_default_profile(self, username):
        # CHỈ TẠO NỘI DUNG (VALUE)
        return {
            "username": username,
            "stats": {
                "games_played": 0,
                "games_won": 0,
                "current_streak": 0,
                "max_streak": 0,
                "guess_distribution": {str(i): 0 for i in range(1, 7)}
            },
            "last_played": None
        }

    def save_data(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "w", encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_user_data(self, username):
        """Hàm này chịu trách nhiệm GÁN username vào Dictionary tổng"""
        if username not in self.data:
            # Key = username, Value = Profile mặc định
            self.data[username] = self.create_default_profile(username)
            self.save_data()
        return self.data[username]

    def update_stats(self, username, is_win, guess_count):
        # Lấy đúng profile của người đó ra sửa
        profile = self.get_user_data(username)
        stats = profile["stats"]

        stats["games_played"] += 1
        profile["last_played"] = str(date.today())

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

    def get_stats_summary(self, username):
        if username not in self.data:
            return "User mới (chưa có dữ liệu)"
            
        s = self.data[username]["stats"]
        win_rate = (s["games_won"] / s["games_played"] * 100) if s["games_played"] > 0 else 0
        
        return (
            f"\n--- THỐNG KÊ ({username}) ---\n"
            f"Trận: {s['games_played']} | Thắng: {s['games_won']} ({win_rate:.1f}%) | Streak: {s['current_streak']}"
        )