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
        """Tuần tự hóa (Serialize) danh sách liên kết và lưu vào file nhị phân.

        Hàm duyệt qua từng node trong danh sách liên kết, chuyển đổi các thuộc tính
        của người chơi thành byte array theo cấu trúc cố định (record_size) và ghi vào file.
        
        Cấu trúc bản ghi (Record Structure - Total bytes: self.record_size):
        - Username (10 bytes) | Password (10 bytes)
        - Games Played (4 bytes) | Total Wins (4 bytes)
        - Cur Streak (4 bytes) | Best Streak (4 bytes)
        - Win Easy/Normal/Hard (4x3 = 12 bytes)
        - Last Played Date (10 bytes)
        - Resume Mode (1 byte) | Resume Diff (1 byte)
        - Resume Target (13 bytes) | Resume Attempts (69 bytes)

        Args:
            None

        Returns:
            None: Ghi trực tiếp vào file self.file_path.
        """
            
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
        """Đọc file nhị phân và khôi phục lại danh sách liên kết người chơi.

        Hàm đọc lần lượt từng block dữ liệu (kích thước = self.record_size),
        giải mã (decode) các byte thành string hoặc integer và tạo lại các 
        UserNode tương ứng.

        Args:
            None

        Returns:
            None: Cập nhật trực tiếp vào self.head (tạo linked list mới).
        """
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
        """Kiểm tra xem người chơi có ván game nào chưa hoàn thành không.

        Điều kiện có resume:
        - Chuỗi `resume_attempts` không rỗng.
        - Số lượt đoán chưa đạt tối đa (khác 6).

        Args:
            username (str): Tên người dùng cần kiểm tra.

        Returns:
            bool: True nếu có game đang dang dở, False nếu không.
        """
        user = self.get_player(username)
        if len(user.resume_attempts) == 0 or len(user.resume_attempts) == 6:
            return False
        return True

    def get_resume(self, username):
        """Truy xuất thông tin chi tiết của ván game đang được lưu.

        Giải mã các mã số (1, 2, 3) thành các chuỗi cấu hình (easy, normal, hard...)
        để khởi tạo lại môi trường chơi game.

        Args:
            username (str): Tên người dùng.

        Returns:
            tuple: (mode, diff, target_word, list_of_attempts)
        """
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
        """Cập nhật trạng thái ván game hiện tại vào thông tin người dùng.

        Chuyển đổi các cấu hình game (str) thành mã số (int) để tiết kiệm 
        không gian lưu trữ nhị phân.

        Args:
            mode (str): Chế độ chơi (easy/normal/hard).
            diff (str): Loại từ điển (vietnamese/english/math).
            target (str): Từ bí mật của ván đấu.
            attempts (list[str]): Danh sách các từ đã đoán.
            username (str): Tên người dùng.

        Returns:
            None: Gọi hàm save_data() để ghi xuống đĩa ngay lập tức.
        """
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
        """Xóa dữ liệu resume khi ván game kết thúc (Thắng hoặc Thua).

        Reset các trường thông tin resume về giá trị mặc định (0 hoặc rỗng).

        Args:
            username (str): Tên người dùng.

        Returns:
            None: Gọi hàm save_data() để cập nhật file.
        """
        user = self.get_player(username)
        user.resume_mode = 0
        user.resume_diff = 0
        user.resume_target = ""
        user.resume_attempts = ""
        self.save_data()


# HÀM LIÊN QUAN ĐẾN KIỂM SOÁT LƯỢT CHƠI TRONG NGÀY
    def check_can_play(self, username):
        """Kiểm tra giới hạn chơi Daily Challenge (chỉ cho phép 1 lần/ngày).

        So sánh ngày chơi cuối cùng (`last_played`) với ngày hiện tại của hệ thống.

        Args:
            username (str): Tên người dùng.

        Returns:
            bool: True nếu hôm nay chưa chơi, False nếu đã chơi rồi.
        """
        user = self.get_player(username)
        if user.last_played == str(date.today()):
            return False
        return True

    def mark_played_today(self, username):
        """Đánh dấu người chơi đã hoàn thành lượt chơi trong ngày hôm nay.

        Args:
            username (str): Tên người dùng.

        Returns:
            None: Cập nhật ngày hiện tại vào `last_played` và lưu file.
        """
        user = self.get_player(username)
        user.last_played = str(date.today())
        self.save_data()


# HÀM THAO TÁC LINKEDLIST NGƯỜI CHƠI
    def is_empty(self):
        """Kiểm tra danh sách liên kết người dùng có rỗng không.

        Args:
            None

        Returns:
            bool: True nếu self.head là None.
        """
        return self.head == None

    def insert_at_beginning(self, username, password):
        """Tạo node người dùng mới và chèn vào đầu danh sách liên kết (O(1)).

        Args:
            username (str): Tên đăng nhập.
            password (str): Mật khẩu.

        Returns:
            UserNode: Node người dùng vừa được tạo.
        """
        new_node = UserNode(username, password)
        new_node.next = self.head
        self.head = new_node
        return new_node

    def get_player(self, username):
        """Tìm kiếm và trả về object UserNode dựa trên username.

        Hàm bao đóng (wrapper) cho hàm `player_is_exist`.

        Args:
            username (str): Tên đăng nhập cần tìm.

        Returns:
            UserNode | bool: Trả về object UserNode nếu tìm thấy, False nếu không.
        """
        # if self.is_empty():
        #     user = self.create_new_player(username, password)
        # elif self.player_is_exist(username) == False:
        #     user = self.create_new_player(username, password)
        # else:
        user = self.player_is_exist(username)
        return user

    def create_new_player(self, username, password):
        """Hàm tiện ích (Wrapper) để tạo người chơi mới.

        Args:
            username (str): Tên đăng nhập.
            password (str): Mật khẩu.

        Returns:
            UserNode: Node người dùng mới.
        """
        new_user = self.insert_at_beginning(username, password)
        return new_user

    def player_is_exist(self,username):
        """Duyệt danh sách liên kết để tìm người chơi (Linear Search).

        Args:
            username (str): Tên đăng nhập cần kiểm tra.

        Returns:
            UserNode: Trả về node người dùng nếu tìm thấy.
            False: Nếu duyệt hết danh sách mà không thấy.
        """
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
        """Xóa một người dùng khỏi danh sách liên kết.

        Xử lý 2 trường hợp:
        1. Xóa node đầu (Head).
        2. Xóa node ở giữa hoặc cuối danh sách.

        Args:
            username (str): Tên người dùng cần xóa.

        Returns:
            None
        """
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
        """Cập nhật các chỉ số thống kê sau khi kết thúc một ván game.

        Cập nhật: Tổng số game, số trận thắng, chuỗi thắng (Streak), 
        thắng theo độ khó (Easy/Normal/Hard).

        Args:
            username (str): Tên người dùng.
            is_win (bool): Kết quả ván đấu (True = Thắng).
            which_diff (str): Độ khó của ván đấu vừa chơi.

        Returns:
            None: Chỉ cập nhật trong RAM (cần gọi save_data sau đó).
        """
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
        """Tạo bảng xếp hạng Top 5 người chơi chăm chỉ nhất (nhiều game nhất).

        Chuyển Linked List thành List thường, sắp xếp giảm dần theo `games_played`
        và lấy 5 phần tử đầu tiên.

        Args:
            None

        Returns:
            list[tuple]: Danh sách các tuple (username, games_played).
        """
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
        """Tạo bảng xếp hạng Top 5 cao thủ (nhiều trận thắng nhất).

        Sắp xếp giảm dần theo tiêu chí `total_wins`.

        Args:
            None

        Returns:
            list[tuple]: Danh sách các tuple (username, total_wins).
        """
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
        """Chuẩn bị dữ liệu cho biểu đồ cột phân bố chiến thắng.

        Trích xuất số trận thắng ở từng cấp độ khó để vẽ biểu đồ thống kê cá nhân.

        Args:
            username (str): Tên người dùng.

        Returns:
            dict: Dictionary dạng {"Easy": int, "Normal": int, "Hard": int}.
        """
        user = self.get_player(username)
        return {
            "Easy": user.win_easy,
            "Normal": user.win_normal,
            "Hard": user.win_hard
        }


            

    
        
