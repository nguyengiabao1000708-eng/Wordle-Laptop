import json
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
        self.last_played = "1970-01-01"
        self.next = None

class UserManager:
    def __init__(self):
        self.head = None
        self.file_path = "source/data/users_data/users.bin"
        self.name_size = 10
        self.password_size = 10
        self.last_played_size = 10
        self.int_size = 4
        self.record_size = 46 # 10 + 10 + 4 + 4 + 4 + 4 + 10

    def save_data(self):
        """Lưu dữ liệu người dùng vào file nhị phân."""
        if self.is_empty():
            return
            
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
                
                last_date_str = str(current.last_played)
                date_bytes = last_date_str.encode('utf-8')[:10] 
                buffer[36:36+len(date_bytes)] = date_bytes

                f.write(buffer)
                current = current.next

    def load_data(self):
        """Tải dữ liệu người dùng từ file nhị phân."""
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
                user_node.last_played  = data[36:46].decode('utf-8', errors='ignore').rstrip('\x00')
    # def load_data(self):
    #"""Tải dữ liệu người dùng từ file văn bản."""
    #     with open(self.file_path, "r") as f:
    #         for i in f.readlines():
    #             user = i.strip().split("|")
    #             user_node = self.insert_at_beginning(user[0])
    #             user_node.games_played = int(user[1])
    #             user_node.total_wins = int(user[2])
    #             user_node.cur_streak = int(user[3])
    #             user_node.best_streak = int(user[4])

    # def save_data (self):
    # """Lưu dữ liệu người dùng vào file văn bản."""
    #     if self.is_empty():
    #         print("Nothing to save")
    #         return
    #     with open(self.file_path, "w") as f:
    #         current = self.head
    #         while current:
    #             line =f"{current.username}|{current.games_played}|{current.total_wins}|{current.cur_streak}|{current.best_streak}\n"
    #             f.write(line)
    #             current = current.next]

    def check_can_play(self, username):
        """Kiểm tra xem người dùng có thể chơi trong ngày hôm nay hay không."""
        user = self.get_player(username)
        if user.last_played == str(date.today()):
            return False
        return True

    def mark_played_today(self, username):
        """Đánh dấu người dùng đã chơi trong ngày hôm nay."""
        user = self.get_player(username)
        user.last_played = str(date.today())
        self.save_data()

    def insert_at_beginning(self, username, password):
        """Chèn một người dùng mới vào đầu danh sách liên kết."""
        new_node = UserNode(username, password)
        new_node.next = self.head
        self.head = new_node
        return new_node

    def is_empty(self):
        """Kiểm tra xem danh sách người dùng có rỗng hay không."""
        return self.head == None
    
    def update_data(self, username, is_win):
        """Cập nhật dữ liệu người dùng sau mỗi trận chơi."""
        user = self.get_player(username)
        user.games_played +=1
        if is_win == True:
            user.total_wins +=1
            user.cur_streak +=1
            if user.cur_streak > user.best_streak:
                user.best_streak = user.cur_streak
        else:
            user.cur_streak = 0


    def get_player(self, username):
        """Lấy thông tin người dùng dựa trên tên đăng nhập."""
        # if self.is_empty():
        #     user = self.create_new_player(username, password)
        # elif self.player_is_exist(username) == False:
        #     user = self.create_new_player(username, password)
        # else:
        user = self.player_is_exist(username)
        return user


    def create_new_player(self, username, password):
        """Tạo một người dùng mới và thêm vào danh sách."""
        new_user = self.insert_at_beginning(username, password)
        return new_user


    def player_is_exist(self,username):
        """Kiểm tra xem người dùng có tồn tại trong danh sách hay không."""
        if self.is_empty():
            print("not exist")
            return
        itr = self.head
        while itr:
            if itr.username == username.strip():
                return itr
            itr = itr.next
        return False

    def player_statistics(self,username, password):
        """Lấy thống kê người chơi dưới dạng chuỗi."""
        user = self.get_player(username, password)
        return(f"{user.games_played}{user.total_wins}{user.cur_streak}{user.best_streak}")


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


            

    
        
