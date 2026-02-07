import streamlit as st
from . import file_process as f

# HÀM BẢNG HIỆN CHỮ
def render_wordle_board(attempts, wordle):
    """Tạo và hiển thị lưới HTML biểu diễn trạng thái hiện tại của trò chơi.

    Hàm này xây dựng chuỗi HTML chứa các ô chữ (tiles). Màu sắc của ô được 
    xác định bởi trạng thái đoán (Xanh/Vàng/Xám) lấy từ object `wordle`.
    Nó hiển thị:
    1. Các từ đã đoán (có màu).
    2. Từ đang nhập dở (chưa có màu).
    3. Các hàng trống còn lại.

    Args:
        attempts (list[str]): Danh sách các từ người chơi đã đoán.
        wordle (Wordle): Object chứa logic game và từ bí mật.

    Returns:
        None: Render trực tiếp HTML vào giao diện Streamlit bằng st.markdown.
    """
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
    """Thêm một ký tự vào chuỗi đoán hiện tại (callback function).

    Hàm được gọi khi người dùng nhấn phím ảo. Nó kiểm tra giới hạn độ dài
    trước khi cập nhật vào `st.session_state.cur_guess`.

    Args:
        char (str): Ký tự người dùng vừa chọn.
        length_limit (int): Độ dài tối đa cho phép của từ (thường là 5 hoặc độ dài từ bí mật).

    Returns:
        None: Cập nhật trực tiếp vào st.session_state.
    """
    if len(st.session_state.cur_guess) < length_limit:
        st.session_state.cur_guess += char
    else:
        st.warning("Đã đủ chữ!")

def del_char():
    """Xóa ký tự cuối cùng trong chuỗi đoán hiện tại (Backspace).

    Hàm xử lý cắt chuỗi (string slicing) để loại bỏ ký tự vừa nhập sai.

    Args:
        None

    Returns:
        None: Cập nhật trực tiếp vào st.session_state.
    """
    st.session_state.cur_guess = st.session_state.cur_guess[:-1]

def math_logic(guess):
    """Kiểm tra tính hợp lệ về mặt toán học và cú pháp của biểu thức.

    Hàm thực hiện các kiểm tra nghiêm ngặt cho chế độ Math Wordle:
    1. Phải có đúng một dấu bằng '='.
    2. Không có toán tử ở đầu hoặc cuối.
    3. Vế trái là biểu thức, vế phải là số kết quả.
    4. Kết quả tính toán phải là số nguyên.
    5. Hai vế phải bằng nhau về giá trị.

    Args:
        guess (str): Chuỗi biểu thức người dùng nhập (ví dụ: "2+3=5").

    Returns:
        bool: True nếu biểu thức hợp lệ và đúng toán học, False nếu vi phạm.
    """
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
    """Xử lý sự kiện nộp từ đoán (Enter) và cập nhật trạng thái game.

    Hàm thực hiện một loạt các hành động:
    1. Validate độ dài, từ có nghĩa (check_valid_words), hoặc logic toán.
    2. Cập nhật lịch sử đoán vào `wordle.attempts`.
    3. Lưu trạng thái game (Resume) vào database thông qua `um`.
    4. Xóa Redo stack (do có nhánh mới).
    5. Cập nhật thuật toán AI (lọc candidates cho gợi ý).
    6. Kiểm tra điều kiện Thắng/Thua.

    Args:
        length_limit (int): Độ dài bắt buộc của từ.
        wordle (Wordle): Object xử lý logic game.
        um (UserManager): Object quản lý dữ liệu người dùng (để lưu resume).

    Returns:
        None: Cập nhật toàn bộ trạng thái game trong st.session_state.
    """
    guess = st.session_state.cur_guess
    if len(guess) < len(wordle.secret):
        st.warning(f"Vui lòng nhập đủ {wordle.WORDS_LENGTH} chữ cái!")
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
    """Xác định các phím cần bị vô hiệu hóa (tô màu xám đậm).

    Duyệt qua lịch sử các lần đoán, tìm những ký tự đã đoán sai (không có trong secret)
    để làm mờ trên bàn phím ảo, giúp người chơi loại trừ.

    Args:
        wordle (Wordle): Object chứa secret word và lịch sử đoán.

    Returns:
        set: Tập hợp các ký tự cần disabled.
    """
    disabled_chars = []
    for guess in wordle.attempts:
        for char in guess:
            if char not in wordle.secret:
                disabled_chars.append(char)
    return set(disabled_chars)

def render_keyboard(length_limit, wordle, um):
    """Render bàn phím ảo tương tác tùy theo chế độ chơi.

    Hỗ trợ 3 layout bàn phím:
    - Tiếng Anh/Việt: QWERTY.
    - Toán học: Số và các dấu phép tính (+, -, *, /, =).
    Các phím được tô màu (xanh/vàng/xám) dựa trên trạng thái game.

    Args:
        length_limit (int): Độ dài từ (truyền vào callback add_char).
        wordle (Wordle): Dùng để xác định màu sắc phím và logic Undo/Redo.
        um (UserManager): Truyền vào callback submit_char để lưu dữ liệu.

    Returns:
        None: Render các nút bấm (st.button) ra giao diện.
    """
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
    """Hiển thị menu Popover để thay đổi chế độ chơi và độ khó.

    Cho phép chuyển đổi giữa English/Vietnamese/Math và Easy/Normal/Hard.
    Lưu ý: Khi đổi mode, toàn bộ trạng thái game hiện tại (từ đang đoán, 
    lịch sử thắng thua tạm thời) sẽ bị reset để bắt đầu ván mới.

    Args:
        None

    Returns:
        None: Hiển thị UI trong một st.popover.
    """
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
    """Hiển thị menu Popover để nâng cấp trạng thái tài khoản.

    Cho phép chuyển đổi giữa Basic (miễn phí) và Premium (trả phí).
    Reset lại game khi thay đổi trạng thái để áp dụng logic mới (ví dụ: Daily word vs Random word).

    Args:
        None

    Returns:
        None
    """
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
    """Thanh điều hướng chính (Top Bar) của trang chủ.

    Chứa các nút chức năng: Settings, Stats, Ranking, Login và Hint (Gợi ý AI).
    Nút Hint sẽ kích hoạt thuật toán Information Theory tốn tài nguyên tính toán.

    Args:
        wordle (Wordle): Object cần thiết để tính toán Hint (AI).

    Returns:
        None
    """
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
    """Thanh điều hướng dành riêng cho các trang phụ (Ranking, Stats...).

    Giống thanh điều hướng chính nhưng có nút 'Trang chủ' để quay về 
    và không có nút Settings/Hint.

    Args:
        None

    Returns:
        None
    """
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
