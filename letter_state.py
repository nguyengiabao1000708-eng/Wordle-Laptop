
class Letter_state:
    def __init__(self, char):
        self.character = char
        self.right_position = False
        self.right_letter = False

    def __repr__(self):
        GREEN = '\033[32m' 
        YELLOW = '\033[33m' 
        WHITE = "\033[37m" 
        RESET = '\033[0m'
        result =[]

        if self.right_position == True:
            return (f"{GREEN}{self.character}{RESET}")
        elif self.right_letter == True:
            return (f"{YELLOW}{self.character}{RESET}")
        else:
            return (f"{WHITE}{self.character}{RESET}")
         