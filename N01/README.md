# ML241 - Chatbox Câu Hỏi Về Luật (Legal Question Chatbox)

## Giới Thiệu (Introduction)
Dự án này xây dựng một hệ thống chatbox thông minh để trả lời các câu hỏi liên quan đến luật pháp. Chatbox được phát triển dựa trên mô hình `unsloth/Llama-3.2-1B-Instruct` và huấn luyện thông qua notebook `training_chat_bot.ipynb`.


## Yêu Cầu Hệ Thống (System Requirements)
* **Python**: Phiên bản >= 3.8
* **Thư viện cần thiết**:
   * `transformers`
   * `torch`
   * `datasets`
   * `notebook`
   * `pandas`
* **Google Colab** *(không bắt buộc, dùng cho việc huấn luyện mô hình)*

## Hướng Dẫn Huấn Luyện Mô Hình (Model Training)
1. Mở file `training_chat_bot.ipynb` bằng Jupyter Notebook hoặc Google Colab.
2. Tải dữ liệu và chỉnh sửa các tham số mô hình theo nhu cầu.
3. Chạy lần lượt từng cell trong notebook để thực hiện quá trình huấn luyện.
4. Kết quả huấn luyện sẽ được lưu tại thư mục `models/`.
5. Lưu mô hình lên Huggingface để sử dụng lại trong tương lai.

## Chạy Chatbox (Running Chatbox)
1. Mở file `chat_box_with_streamlit.ipynb` bằng Jupyter Notebook hoặc Google Colab.
2. Cài đặt các package liên quan như `streamlit`, `transformers`, và `ngrok`.
3. Đăng ký tài khoản trên ngrok và lấy token của bạn.
4. Thay thế token ngrok trong file bằng token cá nhân của bạn.

Chatbox sẽ hoạt động trên server mà ngrok mở lên.

## Cấu Trúc Dự Án (Project Structure)
* `training_chat_bot.ipynb`: Notebook dùng để huấn luyện mô hình.
* `chat_box_with_streamlit.ipynb`: Notebook dùng để chạy ứng dụng Streamlit với mô hình đã huấn luyện.
* `data/`: Thư mục chứa dữ liệu huấn luyện.
* `app.py`: File chạy ứng dụng chatbox.
* `README.md`: Tài liệu hướng dẫn sử dụng dự án.

## Hình Ảnh Minh Họa (Project Illustrations)

### Hình 1: Giao Diện Chatbox
![Hình 1: Giao Diện Chatbox](img/1.jpg)
Giao diện chatbox pháp lý với thiết kế bằng Streamlit.

### Hình 2: Quá Trình Huấn Luyện Mô Hình
![Hình 2: Quá Trình Huấn Luyện Mô Hình](img/2.jpg)
Nhập vào câu hỏi để kiểm tra.

### Hình 3: Kết Quả Truy Vấn
![Hình 3: Kết Quả Truy Vấn](img/3.jpg)
Model phản hồi câu trả lời phù hợp với câu hỏi.


## Video Hướng Dẫn (Tutorial Videos)
Tham khảo các video dưới đây để hiểu rõ cách huấn luyện và sử dụng chatbox:

### 1. Hướng Dẫn Huấn Luyện Mô Hình Trên Colab
[![Hướng Dẫn Huấn Luyện Mô Hình](https://img.youtube.com/vi/VLAtu-ziW3U/0.jpg)](https://www.youtube.com/watch?v=VLAtu-ziW3U)

**Link Video**: [Hướng Dẫn Chi Tiết Huấn Luyện Mô Hình Trên Google Colab](https://www.youtube.com/watch?v=VLAtu-ziW3U)

### 2. Chạy Inference Với Streamlit
[![Chạy Inference Với Streamlit](https://img.youtube.com/vi/Oi0BLE57QHY/0.jpg)](https://youtu.be/Oi0BLE57QHY)

**Link Video**: [Hướng Dẫn Chạy Chatbox Sử Dụng Streamlit](https://youtu.be/Oi0BLE57QHY)

Với tài liệu này, bạn sẽ dễ dàng triển khai và sử dụng hệ thống chatbox thông minh cho các câu hỏi pháp lý. 🚀

