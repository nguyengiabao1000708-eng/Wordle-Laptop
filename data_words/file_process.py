
def choose_common_words(n,file_input,file_output):
    valid_word =[]
    with open (file_input, "r") as common_wf:
        for i in common_wf :
            i = i.strip().upper()
            if len(i) == n:
                valid_word.append(i)

    with open(file_output, "w") as valid_wf:
        valid_wf.write("\n".join(valid_word))

def choose_all_words(n,file_input,file_output):
    word = []
    with open (file_input, "r") as alpha_wf:
        for i in alpha_wf :
            i = i.strip().upper()
            if len(i) == n:
                word.append(i)

    with open(file_output, "w") as all_wf:
        all_wf.write("\n".join(word))

def default():
    choose_common_words(5,"data_words/common_words_eng.txt","data_words/valid_word_with_length_n.txt")
    choose_all_words(5,"data_words/all_words_eng.txt","data_words/word_with_length_n.txt")
    
def main():
    while True:
        language = input("vietnamese or english: ").lower()
        if language == "vietnamese":
            n = int(input("Chooose the word's length: "))   
            choose_common_words(n,"data_words/common_words_vn.txt","data_words/valid_word_with_length_n.txt")
            choose_all_words(n,"data_words/all_words_vn.txt","data_words/word_with_length_n.txt")
            break
        elif language == "english":
            n = int(input("Chooose the word's length: "))
            choose_common_words(n,"data_words/common_words_eng.txt","data_words/valid_word_with_length_n.txt")
            choose_all_words(n,"data_words/all_words_eng.txt","data_words/word_with_length_n.txt")
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




