# ML241 - Tìm kiếm bài hát thích hợp (Finding matching song)

## Giới thiệu (Introduction)
Dự án này xây dựng một hệ thống tìm kiếm bài hát từ một đoạn nhạc có sẵn.

## Yêu Cầu Hệ Thống (System Requirements)
* **Python**: Phiên bản >= 3.8
* **Thư viện cần thiết**:
   * `tensorflow`
   * `librosa`
   * `numpy`
   * `pandas`
   * `soundlife`
   * `scipy`
   * `os`
   * `matplotlib`
* **Google Colab** 

## Cấu Trúc Dự Án (Project Structure)
* `BTL_ML_2024_Tao_Spectrogram.ipynb`: Tạo spectrogram cho bài hát trong database, đây là quá trình xử lý tín hiệu số sau đó tạo ảnh.
* `BTL_ML_2024_CNN.ipynb`: Huấn luyện mô hình bằng CNN, đây là quá trình xử lý ảnh.
* `database/`: Thư mục chứa dữ liệu huấn luyện gồm 10 bài hát.
* `spectrogram/`: Thư mục chứa dữ liệu hình ảnh spectrogram của 10 bài hát.
* `README.md`: Tài liệu hướng dẫn sử dụng dự án.


### Cách thức hoạt động của `BTL_ML_2024_Tao_Spectrogram.ipynb`
*  Data preprocessed python (Tải dữ liệu trong database)
*  Butterworth lowpass filter functions (Sử dụng bộ lọc thông thấp Butterwworth cho âm thanh)
*  Convert MP3 to WAV and stereo to mono (Chuyển đổi file mp3 sang wva)
*  Generate spectrogram with Hamming window (Tạo spectrogram với cửa sổ Hamming)
*  Plot and save spectrograms as images (Vẽ spectrogram và lưu lại file ảnh)

### Hướng Dẫn Huấn Luyện Mô Hình Trên Colab `BTL_ML_2024_CNN.ipynb`
*  Build CNN model for classifying the spectrogram images
*  Trainning Model CNN từ đó phát hiện bài nhạc đang tìm là bài nào trong database

## Kết luận
*  Do database được sử dụng ít (chỉ 10 songs) nên metric cho ra kết quả chưa chính xác. Tuy nhiên, mục đích chính của dự án là tìm kiếm bài nhạc phù hợp từ audio test trong database.
*  Nhóm vẫn tiếp tục dự án cho database lớn hơn.

Với tài liệu này, bạn sẽ tìm kiếm được bài nhạc thích hợp, triển khai mở rộng mô hình có thể gợi ý bài nhạc phù hợp theo nhiều mục đích khác nhau như Emotion...


