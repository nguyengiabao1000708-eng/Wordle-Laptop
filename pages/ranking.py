from source import UserManager
import streamlit as st
import pandas as pd
from source import ui


def main(): 
    st.set_page_config(page_title="Ranking", layout="centered")
    st.title("Bảng xếp hạng người chơi")
    ui.navigation_subpages()

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

if __name__ == "__main__":
    main()