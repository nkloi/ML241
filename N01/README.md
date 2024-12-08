
# ML241 - Chatbox Câu Hỏi Về Luật (Legal Question Chatbox)

## Giới Thiệu (Introduction)

Dự án này xây dựng một hệ thống chatbox thông minh để trả lời các câu hỏi liên quan đến luật pháp. Chatbox sử dụng mô hình `unsloth/Llama-3.2-1B-Instruct` và được huấn luyện qua notebook `training_chat_bot.ipynb`.


## Yêu Cầu Hệ Thống (System Requirements)

- Python >= 3.8
- Các thư viện cần thiết (Required libraries): 
  - `transformers`
  - `torch`
  - `datasets`
  - `notebook`
  - `scikit-learn`
  - `pandas`
- Google Colab (tuỳ chọn, để huấn luyện mô hình / optional, for model training)


## Huấn Luyện Mô Hình (Model Training)

1. Mở file `training_chat_bot.ipynb` bằng Jupyter Notebook hoặc Google Colab.

2. Tải dữ liệu và chỉnh sửa các tham số mô hình.

3. Chạy lần lượt các cell trong notebook để huấn luyện mô hình.

4. File kết quả huấn luyện sẽ được lưu trong thư mục `models`.

5. Thực hiện lưu mô hình vào Hunggingface của bạn để tái sử dụng

## Chạy Chatbox (Running Chatbox)

```bash
python app.py
```

Chatbox sẽ chạy trên local server (mặc định `http://127.0.0.1:5000`).
Chatbox will run on a local server (default `http://127.0.0.1:5000`).

## Cấu Trúc Dự Án (Project Structure)

- `training.ipynb`: Notebook huấn luyện mô hình
- `models/`: Thư mục lưu trữ các mô hình đã huấn luyện
- `data/`: Thư mục chứa dữ liệu huấn luyện
- `app.py`: File chạy ứng dụng chatbox
- `requirements.txt`: Danh sách các thư viện cần thiết
- `README.md`: Tài liệu hướng dẫn sử dụng dự án

## Video Hướng Dẫn (Tutorial Video)

Để hiểu rõ hơn cách huấn luyện mô hình và sử dụng chatbox, bạn có thể tham khảo video hướng dẫn tại đây.

- [Training model on colab](https://youtu.be/VLAtu-ziW3U)
- [Inference with streamlit](https://youtu.be/VLAtu-ziW3U)


