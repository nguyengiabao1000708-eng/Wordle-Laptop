import streamlit as st
from source import Wordle, UserManager, ui
import source.file_process as f
import datetime
import random

# HÀM KHỞI TẠO TRẠNG THÁI
def init_states():
    """Khởi tạo và thiết lập các giá trị mặc định cho Session State.

    Hàm này đảm bảo các biến trạng thái quan trọng (state, wordle object, 
    mode, diff, user info...) luôn tồn tại trước khi render giao diện.
    Đồng thời, nó cũng tải danh sách từ (all_words, candidates) dựa trên 
    chế độ chơi hiện tại (Math hoặc Word).

    Args:
        None

    Returns:
        None: Hàm cập nhật trực tiếp vào st.session_state.
    """
    if "state" not in st.session_state:
        st.session_state.state = "basic"
    if "wordle" not in st.session_state:
        st.session_state.wordle = Wordle(get_random_word("source/data/words_data/valid_word_with_length_n.txt"))
        st.session_state.game_over = False
        st.session_state.is_win = False
    if "cur_guess" not in st.session_state:
        st.session_state.cur_guess = ""
    if "mode" not in st.session_state:
        st.session_state.mode = "english"
    if "diff" not in st.session_state:
        st.session_state.diff = "easy"
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "has_saved" not in st.session_state:
        st.session_state.has_saved = False
    if "has_resume" not in st.session_state:
        st.session_state.has_resume = False

    if st.session_state.mode == "math":
        DATA_PATH = "source/data/words_data/valid_word_with_length_n.txt"
    else:
        DATA_PATH = "source/data/words_data/word_with_length_n.txt"

    if "all_words" not in st.session_state:
        st.session_state.all_words = get_all_words(DATA_PATH)
    if "candidates" not in st.session_state:
        st.session_state.candidates = get_all_words(DATA_PATH)

# HÀM ĐỌC CSS VÀ HÀM CHỌN TỪ

def get_all_words(file_path):
    """Đọc và tải toàn bộ danh sách từ từ file văn bản.

    Hàm mở file, đọc từng dòng, loại bỏ ký tự xuống dòng và khoảng trắng thừa,
    sau đó trả về một danh sách chứa các từ sạch.

    Args:
        file_path (str): Đường dẫn tương đối hoặc tuyệt đối đến file dữ liệu (.txt).

    Returns:
        list[str]: Danh sách các từ đã được xử lý (strip).
    """
    with open(file_path, "r") as f:
        words = []
        for i in f.readlines():
            words.append(i.strip())
    return words

def local_css(file_name):
    """Đọc file CSS và nhúng style vào ứng dụng Streamlit.

    Sử dụng st.markdown với unsafe_allow_html=True để áp dụng các quy tắc CSS 
    tùy chỉnh (giao diện, màu sắc ô chữ, bàn phím) cho trang web.

    Args:
        file_name (str): Đường dẫn đến file .css cần tải.

    Returns:
        None: CSS được inject trực tiếp vào DOM của trang.
    """
    with open (file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

local_css("source/static/style.css")

def get_random_word(file_path):
    """Chọn một từ bí mật (Secret Word) từ file dữ liệu.

    Hàm có 2 cơ chế hoạt động dựa trên trạng thái tài khoản (st.session_state.state):
    1. Basic: Sử dụng ngày hiện tại làm seed để chọn từ (Mọi người chơi Basic 
       đều có từ giống nhau trong ngày - Daily Challenge).
    2. Premium: Chọn từ hoàn toàn ngẫu nhiên mỗi lần chơi.

    Args:
        file_path (str): Đường dẫn đến file chứa danh sách từ hợp lệ.

    Returns:
        str: Từ bí mật được chọn (đã chuyển sang in hoa).
        None: Nếu file rỗng hoặc không đọc được.
    """         
    with open(file_path, "r") as file:
        word_list = file.readlines()
    if not word_list: return None

    if st.session_state.state == "basic":
        today_str = datetime.date.today().strftime("%Y%m%d")
        seed_value = int(today_str)
        random.seed(seed_value)
        return random.choice(word_list).strip().upper()
    else:
        return random.choice(word_list).strip().upper()

# HÀM CHÍNH
def main():
    st.set_page_config(page_title="Wordle HCMUS", layout="centered", initial_sidebar_state= "collapsed")
    init_states()
    user_manager = UserManager()

    user_manager.load_data()

    username = st.session_state.username
    user = user_manager.get_player(username)
    if username:
        st.title(f"Welcome, {username}")
    else:
        st.title("Welcome to Wordle!")

    if st.session_state.has_resume == True:
        mode, diff, target, attempts = user_manager.get_resume(username)
        st.session_state.wordle = Wordle(target)
        wordle = st.session_state.wordle
        wordle.attempts +=  attempts
        st.session_state.mode = mode
        st.session_state.diff = diff
        st.session_state.has_resume = False
        user_manager.clear_resume(username)
    else:
        wordle = st.session_state.wordle
        target = wordle.secret

    ui.navigation(wordle)
    ui.render_wordle_board(wordle.attempts, wordle)

    if user:
        can_play = user_manager.check_can_play(username)
        if can_play == False and st.session_state.state == "basic":
            st.warning("Bạn đã chơi từ hôm nay rồi! Vui lòng quay lại vào ngày mai")
            st.warning("Nếu muốn tiếp tục chơi hãy mua gói premium để mở khoá full")
        else:
            if st.session_state.game_over == False:
                ui.render_keyboard(len(target), wordle, user_manager)
            else:
                if not st.session_state.has_saved :
                    if st.session_state.is_win:
                            user_manager.update_data(username, True, st.session_state.diff)
                    else:
                            user_manager.update_data(username, False, st.session_state.diff)

                    if username:      
                        user_manager.save_data()

                    st.session_state.has_saved = True

                if st.session_state.is_win:
                    st.success(f"Chúc mừng! Bạn đã đoán đúng từ '{target}'")
                else:
                    st.error(f"Bạn đã thua! Từ đúng là '{target}'")
                user_manager.clear_resume(username)

                user_manager.mark_played_today(username)
            
                if st.button("new game"):
                    del st.session_state.is_win
                    del st.session_state.wordle
                    del st.session_state.game_over
                    del st.session_state.cur_guess
                    del st.session_state.has_saved
                    st.rerun()
    else: 
        if st.session_state.game_over == False:
            ui.render_keyboard(len(target), wordle, user_manager)
        else:
            if st.session_state.is_win:
                st.success(f"Chúc mừng! Bạn đã đoán đúng từ '{target}'")
            else:
                st.error(f"Bạn đã thua! Từ đúng là '{target}'")
            st.warning("Vui lòng đăng nhập để thông tin của bạn được lưu!")
        
            if st.button("new game"):
                del st.session_state.is_win
                del st.session_state.wordle
                del st.session_state.game_over
                del st.session_state.cur_guess
                del st.session_state.has_saved
                del st.session_state.has_resume
                del st.session_state.candidates
                del st.session_state.all_words
                st.rerun()

if __name__ == "__main__":
    main()


 





