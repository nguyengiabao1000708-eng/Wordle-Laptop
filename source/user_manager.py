import os
from datetime import date

class UserNode:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.games_played = 0
        self.total_wins = 0
        self.cur_streak = 0
        self.best_streak = 0
        self.win_easy = 0
        self.win_normal = 0
        self.win_hard = 0
        self.last_played = "1970-01-01"
        self.resume_mode = 0
        self.resume_diff = 0
        self.resume_target = ""
        self.resume_attempts = ""
        self.next = None

class UserManager:
    def __init__(self):
        self.head = None
        self.file_path = "source/data/users_data/users.bin"
        self.name_size = 10
        self.password_size = 10
        self.last_played_size = 10
        self.int_size = 4
        self.resume = 80
        self.record_size = 142 # 10 + 10 + 4*7 + 10 + 80 (1 + 1 + 13 + (13 * 5 +4))


# HÀM TẢI VÀ LƯU DỮ LIỆU NGƯỜI CHƠI (NHỊ PHÂN)
    def save_data(self):
        """Lưu dữ liệu người chơi vào file nhị phân."""
            
        with open(self.file_path, "wb") as f:
            current = self.head
            while current:
                buffer = bytearray(self.record_size)

                name_bytes = current.username.encode('utf-8')[:self.name_size]
                buffer[0:len(name_bytes)] = name_bytes 
                
                password_bytes = current.password.encode('utf-8')[:self.password_size]
                buffer[10:len(password_bytes) + 10] = password_bytes

                buffer[20:24] = current.games_played.to_bytes(self.int_size, 'little')
                buffer[24:28] = current.total_wins.to_bytes(self.int_size, 'little')
                buffer[28:32] = current.cur_streak.to_bytes(self.int_size, 'little')
                buffer[32:36] = current.best_streak.to_bytes(self.int_size, 'little')
                buffer[36:40] = current.win_easy.to_bytes(self.int_size, 'little')
                buffer[40:44] = current.win_normal.to_bytes(self.int_size, 'little')
                buffer[44:48] = current.win_hard.to_bytes(self.int_size, 'little')
                
                last_date_str = str(current.last_played)
                date_bytes = last_date_str.encode('utf-8')[:10] 
                buffer[48:48+len(date_bytes)] = date_bytes
 
                buffer[58:59] = int(current.resume_mode).to_bytes(1, 'little')
                buffer[59:60] = int(current.resume_diff).to_bytes(1, 'little')

                target_bytes = current.resume_target.encode('utf-8')[:13]
                buffer[60 : 60 + len(target_bytes)] = target_bytes

                attempts_bytes = current.resume_attempts.encode('utf-8')[:69]
                buffer[73 : 73 + len(attempts_bytes)] = attempts_bytes

                f.write(buffer)
                current = current.next

    def load_data(self):
        """Tải dữ liệu người chơi từ file nhị phân."""
        if not os.path.exists(self.file_path):
            return

        self.head = None
        with open(self.file_path, "rb") as f:
            while True:
                data = f.read(self.record_size)
                if len(data) < self.record_size:
                    break
                
                username = data[0:10].decode('utf-8', errors='ignore').rstrip('\x00')
                password = data[10:20].decode('utf-8', errors='ignore').rstrip('\x00')

                user_node = self.insert_at_beginning(username, password)

                user_node.games_played = int.from_bytes(data[20:24], 'little')
                user_node.total_wins   = int.from_bytes(data[24:28], 'little')
                user_node.cur_streak   = int.from_bytes(data[28:32], 'little')
                user_node.best_streak  = int.from_bytes(data[32:36], 'little')
                user_node.win_easy     = int.from_bytes(data[36:40], 'little')
                user_node.win_normal   = int.from_bytes(data[40:44], 'little')
                user_node.win_hard     = int.from_bytes(data[44:48], 'little')

                user_node.last_played  = data[48:58].decode('utf-8', errors='ignore').rstrip('\x00')
                user_node.resume_mode     = int.from_bytes(data[58:59], 'little')
                user_node.resume_diff     = int.from_bytes(data[59:60], 'little')

                user_node.resume_target   = data[60:73].decode('utf-8', errors='ignore').rstrip('\x00')
                user_node.resume_attempts = data[73:142].decode('utf-8', errors='ignore').rstrip('\x00')


# HÀM RESUME NGƯỜI CHƠI
    def have_resume(self, username):
        """Kiểm tra người chơi có resume hay không."""
        user = self.get_player(username)
        if len(user.resume_attempts) == 0 or len(user.resume_attempts) == 6:
            return False
        return True

    def get_resume(self, username):
        """Lấy resume của người chơi."""
        user = self.get_player(username)
        if user.resume_mode == 1:
            mode = "easy"
        elif user.resume_mode == 2: 
            mode = "normal"
        else:   
            mode = "hard"
        if user.resume_diff == 1:
            diff = "vietnamese"
        elif user.resume_diff == 2:
            diff = "english"
        else:   
            diff = "math"
        target = user.resume_target
        attempts = user.resume_attempts.split(",") if user.resume_attempts else []
        return mode, diff, target, attempts

    def update_resume (self, mode, diff, target, attempts, username):
        """Cập nhật resume của người chơi."""
        user = self.get_player(username)

        if mode == "easy":
            user.resume_mode = 1
        elif mode == "normal":
            user.resume_mode = 2
        else:
            user.resume_mode = 3

        if diff == "vietnamese":
            user.resume_diff = 1
        elif diff == "english": 
            user.resume_diff = 2
        else:
            user.resume_diff = 3
        user.resume_target = target
        user.resume_attempts = ",".join(attempts)
        self.save_data()

    def clear_resume(self, username):
        """Xóa resume của người chơi."""
        user = self.get_player(username)
        user.resume_mode = 0
        user.resume_diff = 0
        user.resume_target = ""
        user.resume_attempts = ""
        self.save_data()


# HÀM LIÊN QUAN ĐẾN KIỂM SOÁT LƯỢT CHƠI TRONG NGÀY
    def check_can_play(self, username):
        """Kiểm tra xem người chơi có thể chơi trong ngày hôm nay hay không."""
        user = self.get_player(username)
        if user.last_played == str(date.today()):
            return False
        return True

    def mark_played_today(self, username):
        """Đánh dấu người chơi đã chơi trong ngày hôm nay."""
        user = self.get_player(username)
        user.last_played = str(date.today())
        self.save_data()


# HÀM THAO TÁC LINKEDLIST NGƯỜI CHƠI
    def is_empty(self):
        """Kiểm tra xem danh sách người chơi có rỗng hay không."""
        return self.head == None

    def insert_at_beginning(self, username, password):
        """Chèn một người chơi mới vào đầu danh sách liên kết."""
        new_node = UserNode(username, password)
        new_node.next = self.head
        self.head = new_node
        return new_node

    def get_player(self, username):
        """Lấy thông tin người chơi dựa trên tên đăng nhập."""
        # if self.is_empty():
        #     user = self.create_new_player(username, password)
        # elif self.player_is_exist(username) == False:
        #     user = self.create_new_player(username, password)
        # else:
        user = self.player_is_exist(username)
        return user

    def create_new_player(self, username, password):
        """Tạo một người chơi mới và thêm vào danh sách."""
        new_user = self.insert_at_beginning(username, password)
        return new_user

    def player_is_exist(self,username):
        """Kiểm tra xem người chơi có tồn tại trong danh sách hay không."""
        if self.is_empty():
            print("not exist")
            return
        itr = self.head
        while itr:
            if itr.username == username:
                return itr
            itr = itr.next
        return False
    
    def delete_player(self, username):
        """Xóa người chơi khỏi danh sách dựa trên tên đăng nhập."""
        cur = self.head
        if self.head.username == username:
            self.head = self.head.next
            return
        while cur.next:
            if cur.next.username == username:
                cur.next = cur.next.next
                return
            cur = cur.next    
    
    def update_data(self, username, is_win, which_diff):
        """Cập nhật dữ liệu người chơi sau mỗi trận chơi."""
        user = self.get_player(username)
        user.games_played +=1
        if is_win == True:
            user.total_wins +=1
            if which_diff == "easy":
                user.win_easy += 1
            elif which_diff == "normal":
                user.win_normal += 1
            else:
                user.win_hard += 1
            user.cur_streak +=1
            if user.cur_streak > user.best_streak:
                user.best_streak = user.cur_streak
        else:
            user.cur_streak = 0


# HÀM LIÊN QUAN ĐẾN XẾP HẠNG NGƯỜI CHƠI
    def ranking_total_games(self):
            """Lấy bảng xếp hạng người chơi dựa trên số trận đã chơi."""
            if self.is_empty():
                print("No player")
                return
            
            rank_list = []
            itr = self.head
            while itr:
                rank_list.append(itr) 
                itr = itr.next
            
            rank_list.sort(key=lambda x: x.games_played, reverse=True)
            top_5 = rank_list[:5]
            list = []

            for i in top_5:
                list.append((i.username, i.games_played))
            return list
    
    def ranking_total_wins_games(self):
            """Lấy bảng xếp hạng người chơi dựa trên số trận thắng."""
            if self.is_empty():
                print("No player")
                return
            
            rank_list = []
            itr = self.head
            while itr:
                rank_list.append(itr) 
                itr = itr.next
            

            rank_list.sort(key=lambda x: x.total_wins, reverse=True)
            top_5 = rank_list[:5]
            list = []

            for i in top_5:
                list.append((i.username, i.total_wins))
            return list


# HÀM BIỂU ĐỒ CỘT SỐ TRẬN THẮNG THEO ĐỘ KHÓ
    def bar_chart_diff(self, username):
        """Lấy dữ liệu để vẽ biểu đồ cột cho số trận thắng theo từng độ khó."""
        user = self.get_player(username)
        return {
            "Easy": user.win_easy,
            "Normal": user.win_normal,
            "Hard": user.win_hard
        }


            

    
        
