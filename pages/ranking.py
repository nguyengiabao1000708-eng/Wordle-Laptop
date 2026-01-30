from source import UserManager
import streamlit as st
import pandas as pd
 
def navigation():
    """Hiển thị thanh điều hướng giữa các trang."""
    col1, col2, col3 = st.columns([1.5, 2, 2])
    with col1:
        if st.button("Trang chủ", icon= "🏠", use_container_width=True):
            st.switch_page("demo_streamlit.py")
    with col2:
        if st.button("Thông số người chơi", icon= "📈", use_container_width=True):
            st.switch_page("pages/player_stats.py")
    with col3:
        if st.button("Bảng xếp hạng", icon= "📉", use_container_width=True):
            st.switch_page("pages/ranking.py")


st.set_page_config(page_title="Ranking", layout="centered")
st.title("Bảng xếp hạng người chơi")

navigation()
user_manager = UserManager()
user_manager.load_data()

c1, c2, c3 = st.columns([2, 0.5, 2]) 
with c1:
    st.subheader("Xếp hạng số trận")
    ranking_played = user_manager.ranking_total_games()
    if ranking_played:
        df_played = pd.DataFrame(ranking_played, columns=["Người chơi", "Số trận"])
        df_played.index = df_played.index + 1
        st.table(df_played)

with c2:
    pass

with c3:
    st.subheader("Xếp hạng trận thắng")
    ranking_wins = user_manager.ranking_total_wins_games()
    if ranking_wins:
        df_wins = pd.DataFrame(ranking_wins, columns=["Người chơi", "Số trận thắng"])
        df_wins.index = df_wins.index + 1
        st.table(df_wins)