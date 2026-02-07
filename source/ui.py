import streamlit as st
from . import file_process as f

# HÀM BẢNG HIỆN CHỮ
def render_wordle_board(attempts, wordle):
    """Hiển thị bảng trò chơi Wordle với các trạng thái đoán."""
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


# HÀM BÀN PHÍM VÀ MỘT SỐ THAO TÁC 
def add_char(char, length_limit):
    """Thêm ký tự vào đoán hiện tại nếu chưa đạt giới hạn độ dài."""
    if len(st.session_state.cur_guess) < length_limit:
        st.session_state.cur_guess += char
    else:
        st.warning("Đã đủ chữ!")

def del_char():
    """Xóa ký tự cuối cùng khỏi đoán hiện tại."""
    st.session_state.cur_guess = st.session_state.cur_guess[:-1]

def math_logic(guess):
    """Kiểm tra tính hợp lệ của biểu thức toán học."""
    a, b = guess.split("=")
    result = False

    if guess.count('=') != 1:
        st.warning("Biểu thức phải chứa ĐÚNG một dấu '='")
    elif guess[-1] in '+-*/=' or guess[0] in '+-*/=':
        st.warning("Dấu '=' và các toán tử không thể ở đầu hoặc cuối biểu thức")
    elif len(a) < len(b):
        st.warning("Bên trái của '=' phải là một biểu thức và bên phải là một số")
    elif eval(a) != int(eval(a)):
        st.warning("Kết quả của biểu thức PHẢI là một số nguyên") 
    elif eval(a) != int(b):
        st.warning("2 vế PHẢI bằng nhau")
    else:
        result = True

    return result


def submit_char(length_limit, wordle, um):
    """Xử lý khi người dùng nhấn nút ENTER để gửi đoán."""
    guess = st.session_state.cur_guess
    if len(guess) < len(wordle.secret):
        st.warning(f"Vui lòng nhập đủ {wordle.secret} chữ cái!")
    elif wordle.already_guessed(guess):
        st.warning("Từ này đã được đoán!")
    elif st.session_state.mode == "math" and math_logic(guess) == False :
        pass
    elif st.session_state.mode != "math" and not wordle.check_valid_words(guess,"source/data/words_data/word_with_length_n.txt"):
        st.warning("Từ không tồn tại")
    else:
        wordle.attempts.append(guess)

        if st.session_state.username:
            um.update_resume(st.session_state.mode, st.session_state.diff, wordle.secret, wordle.attempts, st.session_state.username)

        wordle.redo_stack.clear()
        st.session_state.candidates =wordle.update_candidates(st.session_state.candidates, guess, wordle.get_pattern(guess, wordle.secret))

        if guess == wordle.secret:
            st.session_state.game_over = True
            st.session_state.is_win = True
        elif wordle.attempts_remaining() ==0 :
            st.session_state.game_over = True

    st.session_state.cur_guess = ""

def get_disabled_chars(wordle):
    """Lấy danh sách các ký tự đã bị vô hiệu hóa trên bàn phím."""
    disabled_chars = []
    for guess in wordle.attempts:
        for char in guess:
            if char not in wordle.secret:
                disabled_chars.append(char)
    return set(disabled_chars)

def render_keyboard(length_limit, wordle, um):
    """Hiển thị bàn phím ảo và xử lý các nút bấm."""
    if st.session_state.mode != "math":
        if  st.session_state.mode == "vietnamese":
            keys = ["QWERTYUIOP", "ASDFGHJKL", "ZXCV BNM"]
        else:
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
            
        row2 = st.columns([1.4] + [1]*len(keys[1]) + [1.4])

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
    


        row3[0].button("ENTER", on_click = submit_char, args = (length_limit, wordle, um),
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
    else:
        keys = ["1234567890", "+-*/=",]
        disabled_chars = get_disabled_chars(wordle)

        row1 = st.columns(len(keys[0]))
        for i, char in enumerate(keys[0]):
            if char in disabled_chars:
                color = "tertiary"
            else:
                color = "secondary"
            row1[i].button(char, on_click = add_char, args = (char, length_limit),
                            use_container_width = True,type = color )

        row2 = st.columns([1] + [1] + [0.8]*len(keys[1]) + [1] + [1])

        row2[0].button("ENTER", on_click = submit_char, args = (length_limit, wordle, um),
                        use_container_width = True)
        row2[-1].button("⌫", on_click= del_char,
                        use_container_width=True)   
        row2[1].button("UNDO", on_click = wordle.undo,
                        use_container_width = True)
        row2[-2].button("REDO", on_click= wordle.redo,
                        use_container_width=True)   

        for i, char in enumerate(keys[1]):
            if char in disabled_chars:
                color = "tertiary"
            else:
                color = "secondary"
            label = char
            if char in ["+", "-", "*"]:
                label = f"\\{char}"
            row2[i+2].button(label, on_click= add_char, args= (char, length_limit),
                            use_container_width= True, type = color)
            

# HÀM ĐIỀU HƯỚNG VÀ THAY ĐỔI CHẾ ĐỘ, TRẠNG THÁI
def change_mode():
    """Cho phép người dùng thay đổi chế độ chơi và độ khó."""
    with st.popover("Đổi Mode", icon= "😎"):
        st.write(f"Mode Hiện tại: {st.session_state.mode}, {st.session_state.diff} ")

        disabled_state = False
        if st.session_state.state == "basic":
            disabled_state = True
            st.error("Nạp tiền để mở khoá full")

        st.write("Chọn chế độ:")
        c1, c2, c3 = st.columns(3)

        def handle_mode_change(new_mode):
            f.main(new_mode, st.session_state.diff)
            st.session_state.mode = new_mode
            if "wordle" in st.session_state:
                del st.session_state.is_win
                del st.session_state.wordle
                del st.session_state.game_over
                del st.session_state.cur_guess
                del st.session_state.has_saved
                del st.session_state.has_resume
                del st.session_state.candidates
                del st.session_state.all_words
            

        
        c1.button("Eng", on_click=handle_mode_change, args=("english",))
        c2.button("VN", on_click=handle_mode_change, args=("vietnamese",), disabled = disabled_state)
        c3.button("Math", on_click=handle_mode_change, args=("math",), disabled= disabled_state)

        st.write("Chọn độ khó:")

        def handle_diff_change(new_diff):
            f.main(st.session_state.mode , new_diff)
            st.session_state.diff = new_diff
            if "wordle" in st.session_state:
                del st.session_state.is_win
                del st.session_state.wordle
                del st.session_state.game_over
                del st.session_state.cur_guess
                del st.session_state.has_saved
                del st.session_state.has_resume
                del st.session_state.candidates
                del st.session_state.all_words


        d1, d2, d3 = st.columns(3)       
        d1.button("Easy", on_click=handle_diff_change, args=("easy",))
        d2.button("Normal", on_click=handle_diff_change, args=("normal",), disabled= disabled_state)
        d3.button("Hard", on_click=handle_diff_change, args=("hard",), disabled= disabled_state)

def change_state():
    """Cho phép người dùng thay đổi trạng thái chơi (cơ bản hoặc nâng cao)."""
    with st.popover("Đổi State", icon= "🎯"):
        st.write(f"State Hiện tại: {st.session_state.state} ")
        st.write("Chọn trạng thái:")
        s1, s2 = st.columns(2)

        def handle_state_change(new_state):
            st.session_state.state = new_state
            if "wordle" in st.session_state:
                del st.session_state.is_win
                del st.session_state.wordle
                del st.session_state.game_over
                del st.session_state.cur_guess
                del st.session_state.has_saved
                del st.session_state.has_resume
                del st.session_state.candidates
                del st.session_state.all_words
        
        s1.button("Basic", on_click=handle_state_change, args=("basic",))
        s2.button("Premium", on_click=handle_state_change, args=("premium",))

def navigation(wordle):
    """Thanh điều hướng trang chủ"""
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        with st.popover("Settings", icon= "⚙️", use_container_width=True):
            change_mode()
            change_state()
    with col2:
        if st.button("Thông số người chơi", icon= "📈", use_container_width=True):
            st.switch_page("pages/player_stats.py")

    with col3: 
        if st.button("Bảng xếp hạng", icon= "📉", use_container_width=True):
            st.switch_page("pages/ranking.py")
    with col4:
        if st.button("Login", icon= "👤", use_container_width=True):
            st.switch_page("pages/login.py")
    with col5:
        if st.button("Hint", icon="💡", use_container_width=True):
            with st.spinner("AI đang tính toán..."):
                best_guess = wordle.find_best_hint(st.session_state.all_words, st.session_state.candidates)
            st.info(f"Từ tối ưu nhất là: **{best_guess}**")

def navigation_subpages():
    """Thanh điều hướng trang phụ"""
    col1, col2, col3, col4 = st.columns([1.5, 2, 2, 1.2])
    with col1:
        if st.button("Trang chủ", icon= "🏠", use_container_width=True):
            st.switch_page("Home_page.py")
    with col2:
        if st.button("Thông số người chơi", icon= "📈", use_container_width=True):
            st.switch_page("pages/player_stats.py")
    with col3:
        if st.button("Bảng xếp hạng", icon= "📉", use_container_width=True):
            st.switch_page("pages/ranking.py")
    with col4:
        if st.button("Login", icon= "👤", use_container_width=True):
            st.switch_page("pages/login.py")
