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

user_manager = UserManager()
user_manager.load_data()
st.set_page_config(page_title="Ranking", layout="centered")
st.title("Bảng xếp hạng người chơi")
ranking = user_manager.ranking_total_games()
if ranking:
    for i, (username, games_played) in enumerate (ranking, start=1):
        st.write(f"{i}. {username}  ---  Số trận đã chơi: {games_played}")