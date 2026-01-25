from source import UserManager
import streamlit as st

def hide_sidebar():
    st.markdown(
        """
        <style>
            /* Ẩn hoàn toàn sidebar */
            [data-testid="stSidebar"] {
                display: none;
            }
            /* Ẩn luôn nút mũi tên để mở sidebar (Collapsed Control) */
            [data-testid="collapsedControl"] {
                display: none;
            }
            /* Mở rộng phần nội dung chính ra giữa màn hình khi không còn sidebar */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

hide_sidebar()

username = st.session_state.get("username")
game_over = st.session_state.get("game_over")
is_win = st.session_state.get("is_win")

status = False
if game_over == True and is_win == True:
    status = True

st.set_page_config(page_title="Player Statistics", layout="centered")
st.title("Thống kê người chơi")
st.write(f"Username: {username}")

user_manager = UserManager()
user_manager.load_data()
user_manager.get_player(username)

user = user_manager.get_player(username)

st.write("Số trận đã chơi:", user.games_played)
st.write("Tổng số trận thắng:", user.total_wins)
st.write("Chuỗi thắng hiện tại:", user.cur_streak)
st.write("Chuỗi thắng dài nhất:", user.best_streak)
