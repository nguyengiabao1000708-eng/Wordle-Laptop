import streamlit as st
from source import UserManager
from source import ui

def sign_up(um):
    """Hiển thị biểu mẫu đăng ký và xử lý đăng ký người dùng mới."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("## SIGN UP WORDLE")
            with st.form("sign_up_form"):
                username = st.text_input("Username", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                password = st.text_input("Password", type="password", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                confirm_password = st.text_input("Confirm Password", max_chars=10, type="password", placeholder="a-z, A-Z, 0-9 only")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    if um.player_is_exist(username):
                        st.error("Username already exists. Please choose a different username.")
                    else:
                        if password != confirm_password:
                            st.error("Passwords do not match. Please try again.")
                        else:
                            um.create_new_player(username, password)
                            um.save_data()
                            st.success("Sign up successful! You can now log in.")
            st.write("Already have an account?")
            if st.button("Back to Log in"):
                st.session_state.auth_mode = "Log in"
                st.rerun()

def log_in(um):
    """Hiển thị biểu mẫu đăng nhập và xử lý xác thực người dùng."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("## Log in WORDLE")
            with st.form("log_in_form"):
                username = st.text_input("Username", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                password = st.text_input("Password", type="password", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    if um.player_is_exist(username):
                        user = um.get_player(username)
                        if user.password == password:
                            st.success("Log in successful!")
                            st.session_state["username"] = username
                            st.session_state["game_over"] = False
                            st.session_state["is_win"] = False
                            st.session_state.auth_mode = "after_log_in"
                            st.rerun()
                        else:
                            st.error("Incorrect password. Please try again.")
                    else:
                        st.error("Username does not exist.")
            st.write("Don't have an account?")
            if st.button("Sign Up"):
                st.session_state.auth_mode = "signup"
                st.rerun()

def change_password(um):
    """Hiển thị biểu mẫu thay đổi mật khẩu và xử lý thay đổi mật khẩu."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("## Change Password")
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                new_password = st.text_input("New Password", type="password", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                confirm_new_password = st.text_input("Confirm New Password", type="password", max_chars=10, placeholder="a-z, A-Z, 0-9 only")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    username = st.session_state.get("username")
                    user = um.get_player(username)
                    if user.password == current_password:
                        if new_password != confirm_new_password:
                            st.error("New passwords do not match. Please try again.")
                        else:
                            if user.password == new_password:
                                st.error("New password cannot be the same as the current password. Please choose a different password.")
                            else:
                                user.password = new_password
                                um.save_data()
                                st.success("Password changed successfully!")
                    else:
                        st.error("Incorrect current password. Please try again.")
        if st.button("Back to Profile"):
            st.session_state.auth_mode = "after_log_in"
            st.rerun()

def after_log_in(um):
    """Xử lý sau khi người dùng đăng nhập thành công."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown(f"# Hello, {st.session_state.username}!")
            st.divider()

            cola, colb = st.columns([1, 1])
            with cola:
                if st.button("Start Game"):
                        st.switch_page("Home_page.py")
                if st.button("Change Password"):
                    st.session_state.auth_mode = "change_password"
                    st.rerun()
            with colb:
                if st.button("Log out"):
                    st.session_state.auth_mode = "Log in"
                    st.session_state.clear()
                    st.rerun()  
                if st.button("Delete Account"):
                    delete_account(um)
            if um.have_resume(st.session_state["username"]):
                st.write("Bạn đang chơi 1 game dang dở. Muốn tiếp tục không?")
                if st.button("Resume Game"):
                    st.session_state.has_resume = True
                    st.switch_page("Home_page.py")

def delete_account(um):
    """Xử lý xóa tài khoản người dùng."""
    username = st.session_state.get("username")
    um.delete_player(username)
    um.save_data()
    st.session_state.auth_mode = "Log in"
    st.session_state.clear()
    st.rerun()

def main():
    st.set_page_config(page_title="Log in", layout="centered")
    ui.navigation_subpages()

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Log in"

    um = UserManager()
    um.load_data()

    if st.session_state.auth_mode == "Log in":
        log_in(um)
    elif st.session_state.auth_mode == "signup":
        sign_up(um)
    elif st.session_state.auth_mode == "after_log_in":
        after_log_in(um)
    elif st.session_state.auth_mode == "change_password":
        change_password(um)

if __name__ == "__main__":
    main()