# ML241
# Phát Hiện và Nhận Diện Biển Số Xe Sử Dụng YOLOv8

## Giới Thiệu

Đề tài "Phát hiện và nhận diện biển số xe sử dụng YOLOv8" nhằm phát triển một hệ thống tự động phát hiện và đọc biển số xe từ hình ảnh hoặc video.
Hệ thống áp dụng YOLOv8 - một kiến trúc deep learning tiên tiến trong lĩnh vực nhận diện ảnh.

## Mục Tiêu

- Xây dựng hệ thống tự động phát hiện và nhận diện biển số xe từ ảnh/video.
- Nâng cao độ chính xác trong việc nhận diện biển số.
- Tích hợp đọc nội dung biển số sử dụng OCR (Optical Character Recognition).

## Công Nghệ Sử Dụng

- **YOLOv8**: Mô hình deep learning cho nhận diện đối tượng trong ảnh.
- **Python**: Ngôn ngữ chính cho việc xây dựng mô hình.
- **OpenCV**: Thư viện xử lý ảnh.
- **PyTorch**: Framework xây dựng mô hình học sâu.
- **Tesseract OCR**: Nhận dạng ký tự từ biển số.

## Tính Năng

1. **Phát hiện biển số xe**:
   - Nhận diện khu vực biển số trong hình ảnh/video.
2. **Nhận diện nội dung biển số**:
   - Sử dụng OCR để đọc nội dung biển số.
3. **Xử lý video theo thời gian thực**:
   - Nhận diện liên tục từ luồng video.

## Cài Đặt

1. Clone repo:
   ```bash
   git clone https://github.com/your-repo/license-plate-recognition-yolov8.git
   cd license-plate-recognition-yolov8
   ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

3. Tải trọng mô hình YOLOv8:
   - Tải từ [Ultralytics](https://github.com/ultralytics/ultralytics).

## Cách Sử Dụng

1. Chạy demo trên tập hình ảnh:
   ```bash
   python detect.py --source path/to/image.jpg --weights path/to/yolov8-weights.pt
   ```

2. Nhận diện biển số từ video:
   ```bash
   python detect.py --source path/to/video.mp4 --weights path/to/yolov8-weights.pt
   ```

3. Kết hợp OCR để đọc nội dung biển số:
   ```bash
   python detect_with_ocr.py --source path/to/image_or_video
   ```

## Cấu Trúc Thư Mục

- **/models**: Chứa trọng YOLOv8.
- **/data**: Chứa dữ liệu dùng để huấn luyện và test.
- **/scripts**: Các script xử lý dữ liệu và nhận diện.
- **/outputs**: Kết quả đầu ra.
