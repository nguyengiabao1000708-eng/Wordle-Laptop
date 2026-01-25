import streamlit as st
import random
from source import Wordle, UserManager
import source.file_process as f

#Hàm khởi tạo
def init_states():
    if "wordle" not in st.session_state:
        st.session_state.wordle = Wordle(get_random_word("source/data/words_data/valid_word_with_length_n.txt"))
        st.session_state.game_over = False
        st.session_state.is_win = False
    if "cur_guess" not in st.session_state:
        st.session_state.cur_guess = ""
    if "mode" not in st.session_state:
        st.session_state.mode = "English"
    if "diff" not in st.session_state:
        st.session_state.diff = "Easy"
    if "username" not in st.session_state:
        st.session_state.username = ""


#Những hàm liên quan đến thanh bar điều hướng
def change_mode():
    with st.popover("Đổi Mode", icon= "😎"):
        st.write(f"Mode Hiện tại: {st.session_state.mode}, {st.session_state.diff} ")
        st.write("Chọn chế độ:")
        c1, c2, c3 = st.columns(3)

        def handle_mode_change(new_mode):
            f.main(new_mode, st.session_state.diff)
            st.session_state.mode = new_mode
            if "wordle" in st.session_state:
                del st.session_state.wordle
        
        c1.button("Eng", on_click=handle_mode_change, args=("english",))
        c2.button("VN", on_click=handle_mode_change, args=("vietnamese",))
        c3.button("Math", on_click=handle_mode_change, args=("math",))

        st.write("Chọn độ khó:")

        def handle_diff_change(new_diff):
            f.main(st.session_state.mode , new_diff)
            st.session_state.diff = new_diff
            if "wordle" in st.session_state:
                del st.session_state.wordle

        d1, d2, d3 = st.columns(3)       
        d1.button("Easy", on_click=handle_diff_change, args=("easy",))
        d2.button("Normal", on_click=handle_diff_change, args=("normal",))
        d3.button("Hard", on_click=handle_diff_change, args=("hard",))

def username():
    def save_name():
        if st.session_state.temp:
            st.session_state.username = st.session_state.temp

    with st.popover("Username"):
        st.text_input("Player's username: ", key="temp")

        if st.button("Xac nhan ten", on_click=save_name):
            st.rerun()


def navigation():
    col1, col2, col3, col4 = st.columns([1.5, 2, 2, 1.2])
    with col1:
        change_mode()
    with col2:
        if st.button("Thông số người chơi", icon= "📈", use_container_width=True):
            if st.session_state.game_over == True:
                del st.session_state.is_win
                del st.session_state.wordle
                del st.session_state.game_over
            st.switch_page("pages/player_stats.py")

    with col3:
        if st.button("Bảng xếp hạng", icon= "📉", use_container_width=True):
            st.switch_page("pages/ranking.py")
    with col4:
        username()



#Bàn phím và các thao tác
def add_char(char, length_limit):
    if len(st.session_state.cur_guess) < length_limit:
        st.session_state.cur_guess += char
    else:
        st.warning("Đã đủ chữ!")

def del_char():
    st.session_state.cur_guess = st.session_state.cur_guess[:-1]

def submit_char(length_limit, wordle):
    guess = st.session_state.cur_guess
    if len(guess) < len(wordle.secret):
        st.warning(f"Vui lòng nhập đủ {wordle.secret} chữ cái!")
    elif already_guessed(guess,wordle):
        st.warning("Từ này đã được đoán!")
    elif not check_valid_words(guess,"source/data/words_data/word_with_length_n.txt"):
        st.warning("Từ không tồn tại")
    else:
        wordle.attempts.append(guess)
        wordle.redo_stack.clear()
        if guess == wordle.secret:
            st.session_state.game_over = True
            st.session_state.is_win = True
        elif wordle.attempts_remaining() ==0 :
            st.session_state.game_over = True

    st.session_state.cur_guess = ""

def get_disabled_chars(wordle):
    disabled_chars = []
    for guess in wordle.attempts:
        for char in guess:
            if char not in wordle.secret:
                disabled_chars.append(char)
    return set(disabled_chars)

def render_keyboard(length_limit, wordle):
    keys = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    disabled_chars = get_disabled_chars(wordle)

    row1 = st.columns(len(keys[0]))
    for i, char in enumerate(keys[0]):
        if char in disabled_chars:
            color = "tertiary"
        else:
            color = "secondary"
        row1[i].button(char, on_click = add_char, args = (char, length_limit),
                        use_container_width = True,type = color )
        
    row2 = st.columns([1.5] + [1]*len(keys[1]) + [1.5])

    row2[0].button("UNDO", on_click = wordle.undo,
                    use_container_width = True)
    row2[-1].button("REDO", on_click= wordle.redo,
                     use_container_width=True)   
    
    for i, char in enumerate(keys[1]):
        if char in disabled_chars:
            color = "tertiary"
        else:
            color = "secondary"
        row2[i+1].button(char, on_click= add_char, args= (char, length_limit),
                        use_container_width= True, type = color)
        
    row3 = st.columns([1.5] + [1]*len(keys[2]) + [1.5])



    row3[0].button("ENTER", on_click = submit_char, args = (length_limit, wordle),
                    use_container_width = True)
    row3[-1].button("⌫", on_click= del_char,
                     use_container_width=True)
    
    for i, char in enumerate(keys[2]):
        if char in disabled_chars:
            color = "tertiary"
        else:
            color = "secondary"
        row3[i+1].button(char, on_click = add_char, args = (char, length_limit),
                        use_container_width = True, type = color)



#Bảng hiện chữ
def render_wordle_board(attempts, wordle):
    cur = st.session_state.cur_guess
    board_html = "<div class = 'wordle-grid'>"

    for guess in attempts:
        board_html += "<div class = 'wordle-row'>"
        statuses = wordle.get_guess_statuses(guess)
        
        for i, char in enumerate(guess):
            board_html += f'<div class="tile {statuses[i]}">{char}</div>'
        board_html += '</div>'

    if st.session_state.game_over == False:
        board_html += "<div class= 'wordle-row'>"
        for char in cur:
            board_html += f'<div class="tile">{char}</div>'
        for _ in range (len(wordle.secret) - len(cur)):
            board_html += f'<div class="tile"></div>'
        board_html += "</div>"

    rows_to_render = wordle.attempts_remaining()
    
    if not st.session_state.game_over:
        rows_to_render -= 1

    for _ in range (rows_to_render):
        board_html += '<div class="wordle-row">'
        for _ in range(len(wordle.secret)):
            board_html += '<div class="tile"></div>'
        board_html += '</div>'

    board_html += '</div>'
    st.markdown(board_html, unsafe_allow_html=True)



#Linh tinh 
def local_css(file_name):
    with open (file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
local_css("source/static/style.css")

def get_random_word(file_path):
    try:
        with open(file_path, "r") as file:
            word_list = file.readlines()
        if not word_list: return None
        return random.choice(word_list).strip().upper()
    except FileNotFoundError:
        st.error(f"Không tìm thấy file: {file_path}")
        return None
    
def check_valid_words(word, file_path):
    try:
        with open(file_path, "r") as file:
            word_list = {line.strip().upper() for line in file}
        return word in word_list
    except FileNotFoundError:
        return False
    
def already_guessed(guess, wordle):
    return guess in wordle.attempts



# HÀM CHÍNH
def main():
    st.set_page_config(page_title="Wordle HCMUS", layout="centered")
    st.title("Wordle Minimalist")

    init_states()
    wordle = st.session_state.wordle
    target = wordle.secret
    user_manager = UserManager()
    user_manager.load_data()

    username = st.session_state.username
    user_manager.get_player(username)
    st.write(username)

    navigation()
    render_wordle_board(wordle.attempts, wordle)

    if st.session_state.game_over == False:
        render_keyboard(len(target), wordle)

    # if not st.session_state.game_over:
    #     guess = st.text_input("Guess the word: ", max_chars = len(target)).upper()
        
    #     if st.button("enter"):
    #         if len(guess) < len(target):
    #             st.warning(f"Vui lòng nhập đủ {target} chữ cái!")
    #         elif already_guessed(guess,wordle):
    #             st.warning("Từ này đã được đoán!")
    #         elif not check_valid_words(guess,"source/data/words_data/word_with_length_n.txt"):
    #             st.warning("Từ không tồn tại")
    #         else:
    #             wordle.attempts.append(guess)
    #             if guess == target:
    #                 st.session_state.game_over = True
    #                 st.session_state.is_win = True
    #             elif wordle.attempts_remaining() ==0 :
    #                 st.session_state.game_over = True
    #             st.rerun()  

    else:
        if st.button("new game"):
            del st.session_state.is_win
            del st.session_state.wordle
            del st.session_state.game_over
            st.rerun()

        if st.session_state.is_win:
            st.success("You win")
            st.write(f"The word is: {target}")
            if username != "":
                user_manager.update_data(username, True)
        else:
            st.write(f"The word is: {target}") 
            st.warning("you lose")
            if username != "":      
                user_manager.update_data(username, False)
        if username != "":      
            user_manager.save_data()
            


if __name__ == "__main__":
    main()


 





