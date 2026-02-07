import streamlit as st
from source import UserManager
from source import ui

def sign_up(um):
    """Hiển thị biểu mẫu đăng ký và xử lý logic tạo tài khoản mới.

        Hàm này kiểm tra tính hợp lệ của username (không trùng lặp) và 
        password (khớp với xác nhận), sau đó lưu người dùng mới vào database.

        Args:
            um (UserManager): Đối tượng quản lý người dùng, dùng để kiểm tra 
                sự tồn tại của tài khoản và lưu dữ liệu mới.

        Returns:
            None: Hàm tương tác trực tiếp với giao diện Streamlit.
    """
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
    """Hiển thị biểu mẫu đăng nhập và xác thực thông tin người dùng.

        Hàm kiểm tra username và password. Nếu đúng, hệ thống sẽ khởi tạo 
        các biến session_state cần thiết cho phiên chơi game.

        Args:
            um (UserManager): Đối tượng quản lý người dùng, dùng để truy xuất
                thông tin tài khoản (password) từ database.

        Returns:
            None: Hàm cập nhật trực tiếp vào st.session_state và chuyển trang.
    """
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
    """Xử lý quy trình đổi mật khẩu cho người dùng hiện tại.

        Yêu cầu người dùng nhập mật khẩu cũ để xác thực, sau đó kiểm tra 
        tính hợp lệ của mật khẩu mới (không trùng mật khẩu cũ, khớp xác nhận).

        Args:
            um (UserManager): Đối tượng quản lý người dùng, dùng để cập nhật
                và lưu mật khẩu mới vào file dữ liệu.

        Returns:
            None: Hiển thị thông báo thành công hoặc lỗi trên giao diện.
    """
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
    """Hiển thị bảng điều khiển (Dashboard) chính sau khi đăng nhập thành công.

        Cung cấp các tùy chọn điều hướng: Bắt đầu game, Đổi mật khẩu, 
        Đăng xuất, Xóa tài khoản hoặc Tiếp tục game (Resume) nếu có.

        Args:
            um (UserManager): Đối tượng quản lý người dùng, dùng để kiểm tra
                xem người chơi có ván game nào đang dang dở hay không.

        Returns:
            None: Điều hướng trang (switch_page) dựa trên nút bấm của người dùng.
    """
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
    """Xóa vĩnh viễn tài khoản hiện tại khỏi hệ thống và đăng xuất.

        Hàm này sẽ xóa node người dùng khỏi danh sách liên kết trong UserManager,
        cập nhật lại file dữ liệu và xóa sạch session hiện tại.

        Args:
            um (UserManager): Đối tượng quản lý người dùng, chịu trách nhiệm
                thực hiện thao tác xóa trong cấu trúc dữ liệu.

        Returns:
            None: Tự động rerender lại trang về trạng thái Đăng nhập.
    """
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