from source import UserManager
import streamlit as st

user_manager = UserManager()
user_manager.load_data()
st.set_page_config(page_title="Ranking", layout="centered")
st.title("Bảng xếp hạng người chơi")
ranking = user_manager.ranking_total_games()
if ranking:
    for i, (username, games_played) in enumerate (ranking, start=1):
        st.write(f"{i}. {username}  ---  Số trận đã chơi: {games_played}")