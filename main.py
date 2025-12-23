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
        a = input("CHANGE MODE OR PLAY DEFAULT: ").upper()
        if a == "CHANGE MODE":
            f.main()
            break
        elif a == "PLAY DEFAULT":
            f.default()
            break
        else:
            print("unvalid")

    user= UserManager()
    wordle = Wordle(words("data_words/valid_word_with_length_n.txt"))
    is_win = False

    while wordle.can_attempts():
        display_result(wordle)

        guess = input("GUESS THE WORD: ").upper()
        if guess == "REVEAL":
            print("YOU LOSE, LOSER !!")
            user.update_stats(username,is_win,len(wordle.attempts))
            print(f"the answer is : {wordle.secret}")
            print(user.get_stats_summary(username))
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
            is_win = True
            user.update_stats(username,is_win,len(wordle.attempts))
            user.get_stats_summary(username)
            display_result(wordle)
            break
        else:
            print(" ")
            # print("\nGUESS AGAIN !!")
            # print(wordle.attempts_remaining())
    else:

        display_result(wordle)
        print("YOU LOSE, LOSER !!")
        user.update_stats(username,is_win,len(wordle.attempts))
        print(f"the answer is : {wordle.secret}")
        user.get_stats_summary(username)

if __name__ == "__main__":
    main()