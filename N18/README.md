# ML241

# Project Sinh Ảnh Bằng DCGAN

## Tổng Quan
Project này triển khai mô hình **Deep Convolutional Generative Adversarial Network (DCGAN)** để sinh ảnh chân dung giả lập từ một vector không gian ẩn (*latent space vector*). Mô hình được xây dựng bằng Python, sử dụng TensorFlow và Keras làm thư viện chính. DCGAN gồm hai thành phần chính:
- **Generator**: Tạo ra các ảnh giả từ dữ liệu ngẫu nhiên.
- **Discriminator**: Phân biệt giữa ảnh thật và ảnh giả.  
Cả hai models được huấn luyện đối kháng để cải thiện khả năng của nhau, giúp mô hình sinh ảnh ngày càng chân thực.

---

## Cấu Trúc Thư Mục
- **`/DATA/`**: Thư mục gốc chứa tập dữ liệu.
- **`/DATASET/`**: Bộ dữ liệu ảnh gốc, đã được tổ chức lại.
- **`/DATA_SCALE/`**: Thư mục tạm thời chứa ảnh đã được tiền xử lý và tăng cường (*data augmentation*).
- **`/GAN_MODEL/`**: Thư mục lưu trữ các mô hình đã huấn luyện.
- Đảm bảo cấu trúc thư mục như trên để mã hoạt động OK.

---
## Dữ Liệu và model đã train (Dataset)
Dataset được sử dụng trong dự án này có thể tải xuống từ đường link dưới đây:

[Link Dataset](https://drive.google.com/drive/folders/1XkmeU5rGCft0SHc9c3X6LketgfiNTCKS?usp=sharing)

[Link Model](https://drive.google.com/drive/folders/17D1AApf118ZWjPpfhi3YkcaovjHREfQD?usp=sharing)

---

## Các Thành Phần Chính
### 1. **Generator (Mô hình Tạo Ảnh)**
- Chuyển đổi vector ngẫu nhiên 1D từ không gian ẩn (*latent space*) thành ảnh RGB kích thước 64x64.
- Sử dụng các lớp:
  - **Dense** để tạo tensor 3D từ vector 1D.
  - **Conv2DTranspose** để tăng kích thước tensor qua các lớp chuyển vị tích chập.
  - **ReLU** và **sigmoid** để tăng độ phi tuyến và chuẩn hóa giá trị ảnh.

### 2. **Discriminator (Mô hình Phân Loại Ảnh)**
- Phân loại ảnh (kích thước 64x64) là ảnh thật (1) hoặc ảnh giả (0).
- Sử dụng các lớp:
  - **Conv2D** để trích xuất đặc trưng từ ảnh.
  - **MaxPooling** để giảm chiều dữ liệu.
  - **LeakyReLU** để tránh chết neuron.
  - **Dense** để kết nối và đưa ra kết quả dự đoán.

### 3. **DCGAN (Mô hình Kết Hợp)**
- Kết hợp Generator và Discriminator thành một mô hình đối kháng.
- Generator cố gắng tạo ra ảnh đủ thuyết phục để "đánh lừa" Discriminator, trong khi Discriminator cải thiện khả năng phân biệt ảnh thật/giả.
- Quá trình huấn luyện sử dụng:
  - **Binary Cross-Entropy Loss** để đánh giá sai số.
  - **Adam Optimizer** với tốc độ học khác nhau cho từng thành phần:
    - Generator: `0.0002`
    - Discriminator: `0.00005`

---

## Điểm Nổi Bật
### **1. Điều Chỉnh latent space**
- Có thể thay đổi **kích thước không gian ẩn (latent space)** để sinh nhiều kiểu ảnh khác nhau.
- Tùy chỉnh **cấu trúc Generator** (số lớp, kích thước filter) để tăng chất lượng ảnh.

### **2. Tiền Xử Lý Dữ Liệu**
- Bộ dữ liệu ảnh gốc được tiền xử lý bằng `ImageDataGenerator`:
  - Tăng cường dữ liệu qua xoay, lật ngang (*horizontal flip*).
  - Rescale giá trị pixel về [0, 1].
- Ảnh được giảm kích thước về 64x64 để giảm độ phức tạp của mô hình.

### **3. Huấn Luyện ổn địnhđịnh**
- **Label Smoothing**: Thêm nhiễu vào nhãn đầu ra để làm mô hình bền vững hơn.
- **Callbacks**:
  - Tự động lưu mô hình sau mỗi 10 epoch.
  - Hiển thị ảnh được sinh bởi Generator trong quá trình huấn luyện.

### **4. Phân Bổ Tài Nguyên**
- Generator được huấn luyện với tốc độ nhanh hơn để bù đắp khi Discriminator thường mạnh hơn trong giai đoạn đầu.

---

## Quy Trình Huấn Luyện
1. **Chuẩn bị Dữ Liệu**:
   - Tổ chức ảnh vào thư mục `/DATA/DATASET/`.
   - Mã sẽ tự động chuyển ảnh vào thư mục tạm `/DATA_SCALE/` và thực hiện tiền xử lý.
2. **Khởi tạo DCGAN**:
   - Generator và Discriminator được kết nối trong mô hình đối kháng.
3. **Huấn luyện**:
   - Số epoch: 100 (Đề xuất 200)
   - Sau mỗi epoch, lưu mô hình và sinh tập ảnh để theo dõi chất lượng.
4. **Tự động hóa**:
   - Callback lưu trữ các mô hình và sinh ảnh từ vector noise cố định để so sánh qua từng epoch.

---

## Điều Nhận Được Sau Khi Hoàn Thành
1. **Học cách tạo mô hìnhhình**:
   - Sinh ảnh giả như thiệt.
   - Tạo dữ liệu bổ sung cho các bài toán học sâu.
2. **Nghiên cứu GAN**:
   - Dự án này có thể mở rộng để thử nghiệm các biến thể GAN như WGAN hoặc StyleGAN.
3. **Giáo dục**:
   - Mô hình dễ hiểu, phù hợp để dạy về Generative Adversarial Networks.

