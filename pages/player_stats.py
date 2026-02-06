from source import UserManager
import streamlit as st
from source import ui

def main():
    st.set_page_config(page_title="Player Statistics", layout="centered")
    st.title("Thống kê người chơi")
    ui.navigation_subpages()

    username = st.session_state.get("username")
    game_over = st.session_state.get("game_over")
    is_win = st.session_state.get("is_win")

    status = False
    if game_over == True and is_win == True:
        status = True

    user_manager = UserManager()
    user_manager.load_data()
    user = user_manager.get_player(username)

    if user:
        st.markdown(f"## Người chơi: **{username}**")

        c1, c2, c3 , c4 = st.columns(4)
        with c1:
            st.metric("Số trận đã chơi:", user.games_played)
        with c2:
            st.metric("Tổng số trận thắng:", user.total_wins)
        with c3:
            st.metric("Chuỗi thắng hiện tại:", user.cur_streak)
        with c4:
            st.metric("Chuỗi thắng dài nhất:", user.best_streak)
        st.bar_chart(user_manager.bar_chart_diff(username), use_container_width=True)
    else:
        st.write("Vui lòng đăng nhập để xem thông số người chơi.")

if __name__ == "__main__":
    main()