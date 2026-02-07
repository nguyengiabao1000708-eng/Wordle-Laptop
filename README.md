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
| Tiêu chí | Chức năng | Mức độ hoàn thiện | Ghi chú kỹ thuật |
| :--- | :--- | :---: | :--- |
| **Logic Game** | Kiểm tra từ hợp lệ, logic màu sắc | 100% | Sử dụng `Collections.Counter` để xử lý chính xác tần suất ký tự (tránh lỗi hiển thị vàng/xám khi từ có ký tự trùng). |
| | Math Mode Logic | 100% | Validate biểu thức toán học (syntax, semantic check) nghiêm ngặt. |
| **Cấu trúc dữ liệu** | Linked List (User Management) | 100% | Tự cài đặt Node, Insert, Delete, Search. Không dùng thư viện ngoài cho cấu trúc này. |
| | Binary File Processing | 100% | Đọc/Ghi theo block cố định, xử lý `bytearray`, `decode/encode` utf-8 an toàn. |
| | Stack (Undo/Redo) | 100% | Cài đặt ngăn xếp chuẩn cho thao tác hoàn tác. |
| **Thuật toán** | Information Theory (AI Hint) | 100% | Tính toán Entropy chính xác. Tuy nhiên, tốc độ có thể giảm nhẹ với không gian mẫu lớn (>5000 từ) do độ phức tạp tính toán cao. |
| **Trải nghiệm** | Resume/Save Game | 100% | Lưu trạng thái game vào cấu trúc user binary, khôi phục chính xác 100%. |
| | Giao diện (UI) | 95% | Streamlit UI thân thiện, có Responsive cơ bản. Hạn chế nhỏ: Page sẽ reload (rerun) mỗi khi tương tác do đặc thù của Framework Streamlit. |
