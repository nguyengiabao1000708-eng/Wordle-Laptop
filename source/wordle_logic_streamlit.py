from collections import Counter
import streamlit as st 
import math
from collections import Counter

class Wordle:
    MAX_ATTEMPTS = 6

    def __init__(self, word):
        self.secret = word
        self.attempts =[]
        self.redo_stack =[]
        self.WORDS_LENGTH = len(word)

# CÁC HÀM THAO TÁC CƠ BẢN
    def attempt(self, answer):
        """Ghi nhận một từ đoán hợp lệ vào lịch sử trò chơi.

            Hàm này thêm từ người chơi vừa đoán vào danh sách `self.attempts`.
            Lưu ý: Việc kiểm tra tính hợp lệ của từ (có trong từ điển hay không)
            cần được thực hiện trước khi gọi hàm này.

            Args:
                answer (str): Từ mà người chơi đã nhập và nhấn Enter.

            Returns:
                None
        """
        self.attempts.append(answer)

    def attempts_remaining(self):
        """Tính toán số lượt đoán còn lại của người chơi.

                Args:
                    None

                Returns:
                    int: Số lượt chơi còn lại (MAX_ATTEMPTS - số lượt đã đoán).
        """
        left = self.MAX_ATTEMPTS - len(self.attempts)
        return left
    
    def get_guess_statuses(self, guess):
        """Tạo danh sách các lớp CSS để hiển thị màu sắc trên giao diện.

        Hàm này chuyển đổi kết quả từ `get_pattern` (số) thành tên class CSS 
        tương ứng để Streamlit hiển thị màu (Xanh, Vàng, Xám).

        Args:
            guess (str): Từ cần kiểm tra màu sắc.

        Returns:
            list[str]: Danh sách các chuỗi class CSS (ví dụ: ["tile-correct", "tile-absent", ...]).
        """
        pattern = self.get_pattern(guess, self.secret)
        result = ["tile-absent"] * self.WORDS_LENGTH
        for i in range(len(pattern)):
            if pattern[i] == 2:
                result[i] =  "tile-correct"
            elif pattern[i] == 1:
                result[i] = "tile-present"
        return result

    def is_solved(self):
        """Kiểm tra xem người chơi đã đoán đúng từ bí mật hay chưa.

        So sánh từ đoán cuối cùng trong danh sách `attempts` với `secret`.

        Args:
            None

        Returns:
            bool: True nếu từ cuối cùng trùng khớp với secret, ngược lại là False.
        """
        if self.attempts[-1] == self.secret:
            return True
        else:
            return False
        
    def can_attempts(self):
        """Kiểm tra xem trò chơi có thể tiếp tục hay không.

        Điều kiện tiếp tục là người chơi vẫn còn ít nhất 1 lượt đoán.

        Args:
            None

        Returns:
            bool: True nếu số lượt còn lại > 0, ngược lại là False.
        """
        if self.attempts_remaining() > 0:
            return True
        else:
            return False
        
    def undo(self):
        """Hoàn tác (Undo) lượt đoán gần nhất.

        Loại bỏ từ đoán cuối cùng khỏi danh sách `attempts` và đẩy nó sang 
        ngăn xếp `redo_stack` để có thể khôi phục nếu cần.

        Args:
            None

        Returns:
            None: Hàm cập nhật trực tiếp vào thuộc tính của object.
        """
        if not self.attempts:
            st.warning("Nothing to undo")
            return
        
        undo_words = self.attempts.pop()
        self.redo_stack.append(undo_words)
        return
    
    def redo(self):
        """Làm lại (Redo) lượt đoán vừa bị hoàn tác.

        Lấy từ trên đỉnh ngăn xếp `redo_stack` và đưa trở lại danh sách `attempts`.

        Args:
            None

        Returns:
            None
        """
        if not self.redo_stack:
            st.warning("Nothing to redo")
            return
        
        redo_words = self.redo_stack.pop()
        self.attempts.append(redo_words)

    def check_valid_words(self, word, file_path):
        """Kiểm tra sự tồn tại của một từ trong từ điển dữ liệu.

        Hàm mở file văn bản, đọc toàn bộ nội dung và kiểm tra xem từ `word`
        có nằm trong tập hợp các từ đó không.

        Args:
            word (str): Từ cần kiểm tra.
            file_path (str): Đường dẫn đến file .txt chứa danh sách từ hợp lệ.

        Returns:
            bool: True nếu từ tồn tại trong file, False nếu không.
        """
        with open(file_path, "r") as file:
            word_list = {line.strip().upper() for line in file}
        return word in word_list

    def already_guessed(self, guess):
        """Kiểm tra xem từ này đã từng được đoán trong ván này chưa.

        Ngăn người chơi nhập lại một từ đã đoán trước đó để tránh lãng phí lượt.

        Args:
            guess (str): Từ người chơi đang nhập.

        Returns:
            bool: True nếu từ đã có trong lịch sử đoán, False nếu chưa.
        """
        return guess in self.attempts
    
# HÀM INFORMATIONT THEORY (HINT WORDLE)
    
    def get_pattern(self, guess, secret):
        """Tính toán mẫu so khớp (Pattern) giữa từ đoán và từ bí mật.

        Đây là hàm cốt lõi xác định trạng thái màu sắc của các ký tự:
        - 2 (Green): Đúng ký tự, đúng vị trí.
        - 1 (Yellow): Đúng ký tự, sai vị trí.
        - 0 (Grey): Ký tự không có trong từ bí mật (hoặc đã được dùng hết).

        Args:
            guess (str): Từ người dùng đoán.
            secret (str): Từ bí mật (Target word).

        Returns:
            tuple[int]: Một tuple chứa các số nguyên (0, 1, 2) có độ dài bằng độ dài từ.
        """
        guess = guess.upper()
        secret = secret.upper()
        length = len(guess)
        result = [0] * length
        

        letter_counts = Counter(secret)
        
        for i in range(length):
            if guess[i] == secret[i]:
                result[i] = 2
                letter_counts[guess[i]] -= 1
                
        for i in range(length):
            if result[i] == 0: 
                char = guess[i]
                if char in letter_counts and letter_counts[char] > 0:
                    result[i] = 1
                    letter_counts[char] -= 1
                    
        return tuple(result)
    
    def get_distribution(self, guess, candidates):
        """Tạo bảng phân phối tần suất các patterns có thể xảy ra.

        Hàm giả định nếu chọn từ `guess`, nó sẽ tạo ra bao nhiêu loại pattern
        khác nhau khi so sánh với toàn bộ từ trong tập `candidates`.

        Args:
            guess (str): Từ đang được cân nhắc để làm gợi ý.
            candidates (list[str]): Danh sách các từ mục tiêu còn khả thi.

        Returns:
            dict: Dictionary với key là pattern (tuple) và value là số lượng từ tạo ra pattern đó.
        """
        distribution = {}
        for cand in candidates:
            pattern = self.get_pattern(guess, cand)
            if pattern not in distribution:
                distribution[pattern] = 1
            else:
                distribution[pattern] += 1
        return distribution
    
    def calculate_entropy(self, distribution, total_candidates):
        """Tính toán giá trị Entropy (lượng tin) của một phân phối.

        Áp dụng công thức Shannon Entropy: H(X) = -sum(p(x) * log2(p(x))).
        Entropy càng cao, từ đoán càng có khả năng loại bỏ nhiều ứng viên sai.

        Args:
            distribution (dict): Bảng phân phối tần suất pattern (output của `get_distribution`).
            total_candidates (int): Tổng số lượng từ khả thi còn lại.

        Returns:
            float: Giá trị Entropy (đơn vị: bits).
        """
        entropy = 0.0   
        for value in distribution.values():
            p = value/total_candidates
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def find_best_hint(self, all_words, candidates):
        """Tìm từ gợi ý tối ưu nhất dựa trên Information Theory.

        Duyệt qua toàn bộ không gian từ `all_words`, tính entropy cho từng từ
        dựa trên tập `candidates` hiện tại và chọn từ có entropy cao nhất.

        Args:
            all_words (list[str]): Tập hợp tất cả các từ được phép đoán.
            candidates (list[str]): Tập hợp các từ có thể là đáp án đúng (đã được lọc).

        Returns:
            str: Từ có giá trị entropy cao nhất (từ gợi ý tốt nhất).
                 Nếu entropy = 0 (không loại được từ nào), trả về từ đầu tiên trong candidates.
        """
        best_word = None
        max_entropy = -1

        for word in all_words:
            dist = self.get_distribution(word, candidates)
            
            entropy = self.calculate_entropy(dist, len(candidates))
            
            if entropy > max_entropy:
                max_entropy = entropy
                best_word = word
        
        if max_entropy == 0 :
            return st.session_state.candidates[0]
                
        return best_word
    
    def update_candidates(self, current_candidates, guess, actual_pattern):
        """Lọc danh sách ứng viên dựa trên kết quả của lần đoán vừa rồi.

        Giữ lại những từ trong `current_candidates` mà nếu đoán `guess` với từ đó,
        nó cũng sẽ sinh ra pattern y hệt `actual_pattern`.

        Args:
            current_candidates (list[str]): Danh sách ứng viên trước khi lọc.
            guess (str): Từ người chơi vừa đoán.
            actual_pattern (tuple): Pattern thực tế nhận được từ từ bí mật.

        Returns:
            list[str]: Danh sách ứng viên mới (nhỏ hơn hoặc bằng danh sách cũ).
        """
        new_candidates = []
        
        for cand in current_candidates:
            if self.get_pattern(guess, cand) == actual_pattern:
                new_candidates.append(cand)
                
        return new_candidates