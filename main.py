from wordle_logic import Wordle
import random        
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
    wordle = Wordle(words("data/valid_word_with_length_n.txt"))
    while wordle.can_attempts():
        display_result(wordle)

        guess = input("GUESS THE WORD: ").upper()
        if guess in wordle.attempts:
            print("Already guessed !!")
            continue
        if guess == "REVEAL":
            print(f"the answer is {wordle.secret}")
            break
        if len(guess) != wordle.WORDS_LENGTH:
            print(f"the word's length is {wordle.WORDS_LENGTH} ")
            continue
        if check_valid_words(guess,"data/word_with_length_n.txt") == False:
            print("Not a real word !!")
            continue

        wordle.attempt(guess)

        if wordle.is_solved():
            print("YOU GUESSED RIGHT !!")
            break
        else:
            print("\nGUESS AGAIN !!")
            print(wordle.attempts_remaining())
    else:

        display_result(wordle)
        print("YOU LOSE, LOSER !!")
        print(f"the answer is : {wordle.secret}")

if __name__ == "__main__":
    main()