from letter_state import Letter_state
from collections import Counter

class Wordle:
    MAX_ATTEMPTS = 6

    def __init__(self, word):
        self.secret = word
        self.attempts =[]
        self.WORDS_LENGTH = len(word)
        pass

    def attempt(self, answer):
        self.attempts.append(answer)

    def attempts_remaining(self):
        left = self.MAX_ATTEMPTS - len(self.attempts)
        return left
    
    def guess_word(self,word):
        result = [Letter_state(char) for char in word] # Tạo list Letter_state
        
        # 1. Khởi tạo bộ đếm số lần xuất hiện của các chữ cái trong từ bí mật
        # Ví dụ: Nếu self.secret = "APPLE", letter_counts = {'A': 1, 'P': 1, 'L': 2, 'E': 1}
        letter_counts = Counter(self.secret)
        
        # ------------------------------------
        # LƯỢT QUÉT 1: ƯU TIÊN XANH LÁ (GREEN)
        # ------------------------------------
        for i in range(self.WORDS_LENGTH):
            char = word[i]
            
            # Nếu chữ cái đúng vị trí
            if char == self.secret[i]:
                result[i].right_position = True
                
                # Giảm số lượng chữ cái này trong bộ đếm
                if char in letter_counts:
                    letter_counts[char] -= 1
                    
        # ------------------------------------
        # LƯỢT QUÉT 2: TÌM VÀNG (YELLOW) và XÁM (GRAY)
        # ------------------------------------
        for i in range(self.WORDS_LENGTH):
            # Chỉ xử lý các ô chưa được gán Xanh lá
            if not result[i].right_position:
                char = word[i]
                
                # Kiểm tra:
                # 1. Chữ cái có tồn tại trong từ bí mật không?
                # 2. Số lượng chữ cái còn lại trong bộ đếm có lớn hơn 0 không?
                if char in letter_counts and letter_counts[char] > 0:
                    result[i].right_letter = True
                    # Giảm số lượng chữ cái này (đã được cấp phát Vàng)
                    letter_counts[char] -= 1
                    
        return result
        # result = []
        # for i in range (self.WORDS_LENGTH):
        #     char = word[i]
        #     letter = Letter_state(char)
        #     if char in self.secret:
        #         letter.right_letter = True
        #         if char == self.secret[i]:
        #             letter.right_position = True
        #     result.append(letter)
        # return result

    def is_solved(self):
        if self.attempts[-1] == self.secret:
            return True
        else:
            return False
        
    def can_attempts(self):
        if self.attempts_remaining() > 0:
            return True
        else:
            return False
    

    