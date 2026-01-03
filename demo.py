import streamlit as st
import random
from user_manager import UserManager
from wordle_logic import Wordle
import data_words.file_process as f

import sys
import os
st.write(sys.path)
st.write(os.getcwd())


# === CẤU HÌNH TRANG ===
st.set_page_config(page_title="Wordle HCMUS", layout="centered")

# === CSS (GIỮ NGUYÊN) ===
st.markdown("""
<style>
    .wordle-box {
        width: 100%;
        aspect-ratio: 1 / 1;
        border: 2px solid #d3d6da;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
        margin: 2px;
        color: white; 
    }
    .correct { background-color: #6aaa64; border-color: #6aaa64; }
    .present { background-color: #c9b458; border-color: #c9b458; }
    .absent  { background-color: #787c7e; border-color: #787c7e; }
    .empty   { background-color: transparent; color: black; }
    
    @media (prefers-color-scheme: dark) {
        .empty { color: white; border-color: #3a3a3c; }
    }
</style>
""", unsafe_allow_html=True)

# === HELPER FUNCTIONS ===
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

# --- SỬA LẠI LOGIC CẬP NHẬT MÀU PHÍM ---
def update_keyboard_colors():
    if 'key_states' not in st.session_state:
        st.session_state.key_states = {}
    
    wordle = st.session_state.wordle
    
    for guess in wordle.attempts:
        results = wordle.guess_word(guess)
        for letter, state in zip(guess, results):
            current_color = st.session_state.key_states.get(letter, 'default')
            
            if current_color == 'correct':
                continue
            
            # Dùng thuộc tính object thay vì ép kiểu string
            if state.right_position:
                st.session_state.key_states[letter] = 'correct'
            elif state.right_letter and current_color != 'correct':
                st.session_state.key_states[letter] = 'present'
            elif not state.right_position and not state.right_letter and current_color not in ['correct', 'present']:
                st.session_state.key_states[letter] = 'absent'

def render_keyboard():
    keys_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    letter_clicked = None
    action_clicked = None

    def draw_key(col, char):
        status = st.session_state.key_states.get(char, 'default')
        if status == 'correct':
            btn_type, is_disabled = "primary", False
        elif status == 'absent':
            btn_type, is_disabled = "secondary", True
        else:
            btn_type, is_disabled = "secondary", False

        if col.button(char, key=f"btn_{char}", type=btn_type, disabled=is_disabled, use_container_width=True):
            return char
        return None

    for row in keys_layout[:2]:
        cols = st.columns(len(row))
        for i, char in enumerate(row):
            if draw_key(cols[i], char): letter_clicked = char

    cols = st.columns([1.5] + [1]*7 + [1.5])
    if cols[0].button("ENTER", key="btn_enter", use_container_width=True):
        action_clicked = "ENTER"

    for i, char in enumerate(keys_layout[2]):
        if draw_key(cols[i+1], char): letter_clicked = char
            
    if cols[-1].button("⌫", key="btn_del", use_container_width=True):
        action_clicked = "DELETE"

    return letter_clicked, action_clicked

# === SESSION STATE INIT ===
if 'current_input' not in st.session_state: st.session_state.current_input = ""
if 'key_states' not in st.session_state: st.session_state.key_states = {}
if 'game_active' not in st.session_state: st.session_state.game_active = False

def start_new_game():
    f.default() 
    secret_word = get_random_word("data_words/valid_word_with_length_n.txt")
    if secret_word:
        st.session_state.wordle = Wordle(secret_word)
        st.session_state.game_active = True
        st.session_state.message = ""
        st.session_state.current_input = "" # Reset input khi game mới
        st.session_state.key_states = {}    # Reset màu bàn phím
    else:
        st.error("Lỗi khởi tạo từ ngữ!")

# === SIDEBAR ===
with st.sidebar:
    st.title("Cài đặt")
    username_input = st.text_input("Username:", value="Player1")
    if st.button("New Game / Reset"):
        start_new_game()
        st.rerun()
    if st.button("Change Data Mode"):
        f.main()
        st.success("Done!")

# === MAIN LOGIC ===
st.title("👾 Wordle - Streamlit Edition")

if 'wordle' not in st.session_state:
    start_new_game()

wordle = st.session_state.wordle
user_manager = UserManager()

# 1. VẼ LƯỚI
grid_container = st.container()
with grid_container:
    for guess in wordle.attempts:
        cols = st.columns(wordle.WORDS_LENGTH)
        results = wordle.guess_word(guess) 
        for i, (letter, state) in enumerate(zip(guess, results)):
            # SỬA LẠI LOGIC CHECK THUỘC TÍNH
            if state.right_position: css_class = "correct"
            elif state.right_letter: css_class = "present"
            else: css_class = "absent"
            cols[i].markdown(f'<div class="wordle-box {css_class}">{letter}</div>', unsafe_allow_html=True)

    remaining = wordle.attempts_remaining()
    for _ in range(remaining):
        cols = st.columns(wordle.WORDS_LENGTH)
        for i in range(wordle.WORDS_LENGTH):
            cols[i].markdown(f'<div class="wordle-box empty"></div>', unsafe_allow_html=True)

# Cập nhật màu bàn phím dựa trên kết quả mới nhất
update_keyboard_colors()

# 2. XỬ LÝ GAMEPLAY (Chỉ hiện khi game đang chạy)
if st.session_state.game_active:
    st.write("---")
    
    # Hiển thị thông báo lỗi (nếu có)
    if 'message' in st.session_state and st.session_state.message:
        st.warning(st.session_state.message)

    st.markdown(f"<h3 style='text-align: center; letter-spacing: 5px;'>{st.session_state.current_input}</h3>", unsafe_allow_html=True)

    clicked_char, clicked_action = render_keyboard()

    if clicked_char:
        if len(st.session_state.current_input) < wordle.WORDS_LENGTH:
            st.session_state.current_input += clicked_char
            st.session_state.message = "" # Xóa lỗi khi nhập mới
            st.rerun()

    elif clicked_action == "DELETE":
        st.session_state.current_input = st.session_state.current_input[:-1]
        st.session_state.message = ""
        st.rerun()

    elif clicked_action == "ENTER":
        guess = st.session_state.current_input
        
        # --- LOGIC KIỂM TRA QUAN TRỌNG ---
        if guess == "REVEAL": # Cheat code
             st.session_state.game_active = False
             st.session_state.message = f"Thua rồi! Đáp án là: {wordle.secret}"
             user_manager.update_stats(username_input, False, len(wordle.attempts))
             st.rerun()

        elif len(guess) != wordle.WORDS_LENGTH:
            st.session_state.message = "Chưa đủ ký tự!"
            st.rerun()
            
        elif not check_valid_words(guess, "data_words/word_with_length_n.txt"):
            st.session_state.message = "Từ không có nghĩa!"
            st.rerun()
            
        elif guess in wordle.attempts:
             st.session_state.message = "Từ này đoán rồi!"
             st.rerun()

        else:
            # Hợp lệ -> Thực hiện đoán
            wordle.attempt(guess)
            st.session_state.current_input = "" 
            
            # Check Thắng
            if wordle.is_solved():
                st.session_state.game_active = False
                st.balloons()
                st.success(f"CHÚC MỪNG! BẠN ĐÃ ĐOÁN ĐÚNG: {wordle.secret}")
                user_manager.update_stats(username_input, True, len(wordle.attempts))
            
            # Check Thua
            elif not wordle.can_attempts():
                st.session_state.game_active = False
                st.error(f"HẾT LƯỢT! ĐÁP ÁN LÀ: {wordle.secret}")
                user_manager.update_stats(username_input, False, len(wordle.attempts))
            
            st.rerun()

# 3. MÀN HÌNH KẾT THÚC (Hiện khi game_active = False)
else:
    st.write("---")
    if st.button("🔄 Chơi lại ván mới", type="primary"):
        start_new_game()
        st.rerun()
    
    st.info(f"Kết quả trận đấu: {wordle.secret}")
    stats = user_manager.get_stats_summary(username_input)
    st.text(stats)