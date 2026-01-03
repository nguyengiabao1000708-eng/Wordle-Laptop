pre = "data_words/raw_data/"
valid_words_n = "data_words/valid_word_with_length_n.txt"
words_n = "data_words/word_with_length_n.txt"

def choose_file(n,file_input,file_output):
    valid_word =[]
    with open (file_input, "r") as common_wf:
        for i in common_wf :
            i = i.strip().upper()
            if len(i) == n:
                valid_word.append(i)

    with open(file_output, "w") as valid_wf:
        valid_wf.write("\n".join(valid_word))

def default():
    choose_file(5, pre + "common_words_eng.txt",valid_words_n)
    choose_file(5, pre + "all_words_eng.txt",words_n)
    
def main():
    while True:
        language = input("vietnamese/english/math: ").lower()
        if language == "vietnamese":
            n = int(input("Chooose the word's length: "))   
            choose_file(n, pre + "common_words_vn.txt", valid_words_n)
            choose_file(n, pre + "all_words_vn.txt", words_n)
            break
        elif language == "english":
            n = int(input("Chooose the word's length: ")) 
            choose_file(n, pre + "common_words_eng.txt", valid_words_n)
            choose_file(n, pre + "all_words_eng.txt", words_n)
            break
        elif language == "math":
            n = int(input("Chooose the equation length: "))
            choose_file(n, pre + "math.txt", valid_words_n)
            break
        else:
            print("Unvalid, please type again!!")


# words = []
# with open("vi_dictionary.csv", "r") as f:
#     line = f.readlines()
#     print(len(line))
#     for i in line:
#         i = i.strip().split(",")
#         words.append(i[0])
#     print(words)
# with open("word_with_length_n.txt", "w") as wf:
#     for i in words:
#         wf.write(f"{i}\n")




