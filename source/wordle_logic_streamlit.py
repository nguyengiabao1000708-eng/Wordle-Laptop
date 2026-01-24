# from letter_state import Letter_state
from collections import Counter

class Wordle:
    MAX_ATTEMPTS = 5

    def __init__(self, word):
        self.secret = word
        self.attempts =[]
        self.redo_stack =[]
        self.WORDS_LENGTH = len(word)
        pass

    def attempt(self, answer):
        self.attempts.append(answer)

    def attempts_remaining(self):
        left = self.MAX_ATTEMPTS - len(self.attempts)
        return left
    
    def get_guess_statuses(self, guess):
        """
        Trả về danh sách các class CSS cho từng chữ cái trong từ đoán.
        Ví dụ: ['tile-correct', 'tile-absent', 'tile-present', ...]
        """
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
        if self.attempts[-1] == self.secret:
            return True
        else:
            return False
        
    def can_attempts(self):
        if self.attempts_remaining() > 0:
            return True
        else:
            return False
        
    def undo(self):
        if not self.attempts:
            print("Nothing to undo")
            return
        undo_words = self.attempts.pop()
        self.redo_stack.append(undo_words)
        return
    
    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo")
            return
        redo_words = self.redo_stack.pop()
        self.attempts.append(redo_words)
        pass

    

    