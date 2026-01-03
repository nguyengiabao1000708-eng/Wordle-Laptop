from wordle_logic import Wordle
import random
from user_manager import UserManager
import data_words.file_process as f


def display_result(wordle):
    if " " in wordle.secret:
        vn_words =[]
        for i in wordle.secret:
            if i == " ":
                vn_words.append(i)
            else:
                vn_words.append("_")
        print(" ".join(vn_words))

    for word in wordle.attempts:
        result = wordle.guess_word(word)
        print(*result, sep=" ") 

    for _ in range (wordle.attempts_remaining()):
        print("_ "*wordle.WORDS_LENGTH)

def words(file):
    with open(file,"r") as f:
        word_list = f.readlines()
    
    if not word_list:
        print("Lỗi: File rỗng, không có từ nào để chọn.")
        return None

    random_line = random.choice(word_list)
    selected_word = random_line.strip().upper()
    return selected_word

def check_valid_words(word,file):
    if "=" in word:
        expression, answer = word.split("=")
        if eval(expression) == int(answer):
            return True
        else:
            return False
    else: 
        with open(file,"r") as f:
            word_list = []
            for i in f.readlines():
                word_list.append(i.strip())
        if word not in word_list:
            return False
        else:
            return True
    


def main():

    username = input("USERNAME: ")

    while True:
        a = input("MODE/DEFAULT: ").upper()
        if a == "MODE":
            f.main()
            break
        elif a == "DEFAULT":
            f.default()
            break
        else:
            print("unvalid")

    user= UserManager()
    user.load_data()

    wordle = Wordle(words("data_words/valid_word_with_length_n.txt"))
    is_win = False

    while wordle.can_attempts():
        display_result(wordle)

        guess = input("GUESS THE WORD: ").upper()

        if guess == "UNDO":
            wordle.undo()
            continue
        elif guess == "REDO":
            wordle.redo()
            continue
        else:
            wordle.redo_stack =[]

        if guess == "REVEAL":
            print("YOU LOSE, LOSER !!")
            user.update_data(username,is_win)
            print(f"the answer is : {wordle.secret}")
            user.player_statistics(username)
            user.ranking_total_games()
            break

        if guess in wordle.attempts:
            print("Already guessed !!")
            continue
        if len(guess) != wordle.WORDS_LENGTH:
            print(f"the word's length is {wordle.WORDS_LENGTH} ")
            continue
        if check_valid_words(guess,"data_words/word_with_length_n.txt") == False:
            print("Not a real word !!")
            continue

        wordle.attempt(guess)

        if wordle.is_solved():
            print("YOU GUESSED RIGHT !!")
            display_result(wordle)
            is_win = True
            user.update_data(username,is_win)
            user.player_statistics(username)
            break
        else:
            print(" ")
            # print("\nGUESS AGAIN !!")
            # print(wordle.attempts_remaining())
    else:

        display_result(wordle)
        print("YOU LOSE, LOSER !!")
        user.update_data(username,is_win)
        print(f"the answer is : {wordle.secret}")
        user.player_statistics(username)
    user.save_data()

if __name__ == "__main__":
    main()