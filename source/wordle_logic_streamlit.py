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
        pattern = self.get_pattern(guess, self.secret)
        result = ["tile-absent"] * self.WORDS_LENGTH
        for i in range(len(pattern)):
            if pattern[i] == 2:
                result[i] =  "tile-correct"
            elif pattern[i] == 1:
                result[i] = "tile-present"
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
    
# HÀM INFORMATIONT THEORY (HINT WORDLE)
    
    def get_pattern(self, guess, secret):
        """Hàm lõi trả về tuple số (2: Green, 1: Yellow, 0: Grey)"""
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
        distribution = {}
        for cand in candidates:
            pattern = self.get_pattern(guess, cand)
            if pattern not in distribution:
                distribution[pattern] = 1
            else:
                distribution[pattern] += 1
        return distribution
    
    def calculate_entropy(self, distribution, total_candidates):
        entropy = 0.0   
        for value in distribution.values():
            p = value/total_candidates
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def find_best_hint(self, all_words, candidates):
        best_word = None
        max_entropy = -1

        for word in all_words:
            dist = self.get_distribution(word, candidates)
            
            entropy = self.calculate_entropy(dist, len(candidates))
            
            if entropy > max_entropy:
                max_entropy = entropy
                best_word = word
        if len(st.session_state.candidates) == 1 :
            return st.session_state.candidates[0]
                
        return best_word
    
    def update_candidates(self, current_candidates, guess, actual_pattern):
        new_candidates = []
        
        for cand in current_candidates:
            if self.get_pattern(guess, cand) == actual_pattern:
                new_candidates.append(cand)
                
        return new_candidates