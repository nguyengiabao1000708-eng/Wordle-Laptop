pre = "source/data/words_data/"
valid_words_n = "source/data/words_data/valid_word_with_length_n.txt"
words_n = "source/data/words_data/word_with_length_n.txt"

def choose_file(n,file_input,file_output):
    valid_word =[]
    with open (file_input, "r") as common_wf:
        for i in common_wf :
            i = i.strip().upper()
            if len(i) == n:
                valid_word.append(i)

    with open(file_output, "w") as valid_wf:
        valid_wf.write("\n".join(valid_word))
    
def main(mode, diff):
    language = mode
    n = 5
    if language == "vietnamese":
        if diff == "easy":
            n = 5
        elif diff == "normal":
            n = 7
        else:
            n = 9
        choose_file(n, pre + "common_words_vn.txt", valid_words_n)
        choose_file(n, pre + "all_words_vn.txt", words_n)
    elif language == "english":
        if diff == "easy":
            n = 5
        elif diff == "normal":
            n = 7
        else:
            n = 9
        choose_file(n, pre + "common_words_eng.txt", valid_words_n)
        choose_file(n, pre + "all_words_eng.txt", words_n)
    elif language == "math":
        if diff == "easy":
            n = 7
        elif diff == "normal":
            n = 10
        else:
            n = 13
        choose_file(n, pre + "math.txt", valid_words_n)
    else:
        print("Unvalid, please type again!!")





