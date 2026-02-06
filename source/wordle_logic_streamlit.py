from collections import Counter
import streamlit as st 

class Wordle:
    MAX_ATTEMPTS = 6

    def __init__(self, word):
        self.secret = word
        self.attempts =[]
        self.redo_stack =[]
        self.WORDS_LENGTH = len(word)
        pass

    def attempt(self, answer):
        """Thêm từ đoán vào danh sách các lần đoán."""
        self.attempts.append(answer)

    def attempts_remaining(self):
        """Trả về số lần đoán còn lại."""
        left = self.MAX_ATTEMPTS - len(self.attempts)
        return left
    
    def get_guess_statuses(self, guess):
        """Trả về danh sách các class CSS cho từng chữ cái trong từ đoán."""
        guess = guess.upper()

        result = ["tile-absent"] * self.WORDS_LENGTH
        
        letter_counts = Counter(self.secret)
        
        for i in range(self.WORDS_LENGTH):
            if guess[i] == self.secret[i]:
                result[i] = "tile-correct"
                letter_counts[guess[i]] -= 1
                
        for i in range(self.WORDS_LENGTH):
            if result[i] != "tile-correct": 
                char = guess[i]
                if char in letter_counts and letter_counts[char] > 0:
                    result[i] = "tile-present"
                    letter_counts[char] -= 1
                    
        return result
    
    def is_solved(self):
        """Kiểm tra xem đã thắng chưa."""
        if self.attempts[-1] == self.secret:
            return True
        else:
            return False
        
    def can_attempts(self):
        """Kiểm tra xem người chơi còn lượt đoán hay không."""
        if self.attempts_remaining() > 0:
            return True
        else:
            return False
        
    def undo(self):
        """Hoàn tác lần đoán cuối cùng."""
        if not self.attempts:
            st.warning("Nothing to undo")
            return
        
        undo_words = self.attempts.pop()
        self.redo_stack.append(undo_words)
        return
    
    def redo(self):
        """Làm lại lần đoán đã hoàn tác."""
        if not self.redo_stack:
            st.warning("Nothing to redo")
            return
        
        redo_words = self.redo_stack.pop()
        self.attempts.append(redo_words)

    def check_valid_words(self, word, file_path):
        """Kiểm tra xem từ có tồn tại trong file dữ liệu từ hay không."""
        with open(file_path, "r") as file:
            word_list = {line.strip().upper() for line in file}
        return word in word_list

    def already_guessed(self, guess):
        """Kiểm tra xem từ đã được đoán trước đó hay chưa."""
        return guess in self.attempts
    

    