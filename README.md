- references:
    - https://github.com/winstonleedev/tudien ( data vn)
    - https://huggingface.co/datasets/tsdocode/vietnamese-dictionary/tree/main ( data vn)
    - https://github.com/dwyl/english-words ( data eng)
    - https://github.com/mahsu/IndexingExercise/blob/master/5000-words.txt ( data eng)

- tutorial support references:
    - https://www.youtube.com/watch?v=SyWeex-S6d0&t=2251s (Basic wordle)
    - [Gemini Pro](https://gemini.google.com/app?hl=vi) 
    - https://30days.streamlit.app/ (Streamlit)
    - https://www.youtube.com/watch?v=VXtjG_GzO7Q&t=3465s (Pandas)
    - https://www.youtube.com/watch?v=v68zYyaEmEA&t=450s (information theory for wordle)

- Hướng dẫn:
    - Sau khi tải full source về thì sync uv để tải về những thư viện và version python cần thiết
    - cd vào dir wordle và nhập lệnh streamlit run Home_page.py là có thể chơi
    - Nếu chơi mà không tạo tài khoản thì sẽ không lưu thông tin -> Nhớ tạo tài khoản để có trải nghiệm tốt nhất
    - Người mới vào sẽ được mặc định trạng thái basic (có thể tùy chỉnh lên premium bằng Settings(sau này có thể code thêm lên premium phải nạp tiền))
    - Có thể sẽ còn 1 số lỗi có thể xuất hiện trong quá trình chơi vì chưa được test đủ nhiều
    - Có 1 số tính năng chỉ nên áp dụng ở premium và khi ở basic sẽ hơi trục trặc nhẹ hoặc ngược lại
    - Vid hướng dẫn: https://youtu.be/JiqYQ7pFNBo

- Gameplay flow:
    - Vào game đăng nhập
    - chọn chế độ yêu thích và bắt đầu chơi
    - Có thể "hint" khi bí -> Game sẽ chọn cho từ được nhiều thông tin nhất
    - Có tính năng undo, redo nếu muốn dùng
    - Xem thông tin cá nhân ở "Thông số người chơi"
    - Xem bảng ranking ở "Bảng xếp hạng"
    - Đang chơi giữa chừng thoát ra vẫn có resume để chơi tiếp
    - Có thể xóa account nếu muốn reset

- Bảng tự đánh giá:
### 📋 Bảng Tính Năng Dự Án (Feature List)

| STT | Nhóm Chức Năng | Tên Chức Năng | Mô Tả Chi Tiết & Kỹ Thuật Áp Dụng | Hoàn Thiện |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **Core Game Logic** | Cơ chế chơi (Gameplay) | - Xử lý nhập liệu, kiểm tra độ dài từ.<br>- So khớp từ đoán/từ khóa: 🟩 Xanh (Đúng), 🟨 Vàng (Sai vị trí), ⬜ Xám (Không có).<br>- **Kỹ thuật:** Sử dụng `Counter` để xử lý tần suất ký tự chính xác. | 100% |
| 2 | | Đa dạng chế độ (Modes) | - Hỗ trợ 3 chế độ: Tiếng Anh, Tiếng Việt, Toán học (Math).<br>- 3 độ khó: Easy, Normal, Hard (thay đổi độ dài từ/biểu thức). | 100% |
| 3 | | Math Mode Logic | - Kiểm tra tính hợp lệ của biểu thức (1 dấu `=`, 2 vế bằng nhau, kết quả nguyên).<br>- Bàn phím số và toán tử riêng biệt. | 95% |
| 4 | **Data Structures** | Quản lý người dùng<br>(User Management) | - Đăng ký, Đăng nhập, Đổi mật khẩu, Xóa tài khoản.<br>- **Kỹ thuật:** Tự cài đặt **Linked List** (Danh sách liên kết đơn) để quản lý danh sách trong RAM. | 100% |
| 5 | | Lưu trữ dữ liệu<br>(File I/O) | - Lưu/Tải dữ liệu người chơi xuống ổ cứng.<br>- **Kỹ thuật:** Xử lý **Binary File**, tuần tự hóa (`serialize`) object thành `byte array` với cấu trúc cố định (`record_size = 142 bytes`). | 100% |
| 6 | **Algorithms** | AI Gợi ý<br>(Smart Hint) | - Gợi ý từ tối ưu nhất cho người chơi.<br>- **Kỹ thuật:** Áp dụng **Information Theory**, tính toán **Shannon Entropy** để tìm từ loại bỏ được nhiều ứng viên sai nhất.<br>-Chưa tối ưu cho file lớn | 90% |
| 7 | | Undo / Redo | - Cho phép quay lại hoặc làm lại thao tác nhập liệu/đoán từ.<br>- **Kỹ thuật:** Sử dụng cấu trúc **Stack** (Ngăn xếp) để quản lý lịch sử. | 95% |
| 8 | **User Experience** | Lưu game<br>(Resume Game) | - Tự động lưu trạng thái (từ đang đoán, lượt còn lại) khi thoát.<br>- Khôi phục chính xác khi đăng nhập lại. | 90% |
| 9 | | Phân quyền<br>(Basic/Premium) | - **Basic:** Giới hạn chơi 1 lần/ngày (Daily Challenge) dựa trên `date.today()`.<br>- **Premium:** Chơi không giới hạn (Random Word). | 90% |
| 10 | **Statistics** | Thống kê & Xếp hạng | - Xem lịch sử đấu: Số trận, Thắng, Chuỗi thắng (Streak), Biểu đồ.<br>- **Leaderboard:** Top 5 chăm chỉ & Top 5 cao thủ.<br>- Có thể nâng cấp thêm sau này | 90% |
| 11 | **Interface** | Giao diện (UI) | - Giao diện **Streamlit** thân thiện, bố cục chia cột hợp lý.<br>- Hỗ trợ Dark/Light mode, Responsive cơ bản.<br>- CSS tùy chỉnh cho ô chữ và bàn phím.<br>- Có thể nâng cấp thêm sau này | 90% |
