# PHÂN TÍCH HÀNH VI NGƯỜI DÙNG THIẾT BỊ DI ĐỘNG BẰNG MÔ HÌNH KNN

**Giảng viên hướng dẫn**: ThS. Nguyễn Khánh Lợi

|        Họ và tên       |       MSSV     |     Đóng góp    |     Ghi chú    |
|:----------------------:|:--------------:|:---------------:|:--------------:|
|        Phạm Khánh      |     2011391    |        40%      |        NT      |
|      Võ Văn Trí Anh    |     2010137    |        30%      |                |
|     Phan Vũ Bảo Tín    |     2010701    |        30%      |                |

## Giải thích các file

| File                      | Mô tả                                                          |
|---------------------------|----------------------------------------------------------------|
| user_behavior_dataset.csv | Dataset về hành vi sử dụng thiết bị di động của người dùng     |
| data_analysis.ipynb       | Phân tích dữ liệu                                              |
| data_visualization.ipynb  | Trực quan hóa dữ liệu                                          |
| knn.ipynb                 | File chính định nghĩa, huấn luyện mô hình và thực hiện dự đoán |

Trong đó dataset cũng như mô tả chi tiết có thể được tìm thấy ở [Kaggle](https://www.kaggle.com/datasets/valakhorasani/mobile-device-usage-and-user-behavior-dataset/).

## Hướng dẫn setup môi trường

`cd` tới thư mục này và tạo môi trường ảo:
```
python -m venv .venv
```

Activate môi trường ảo:
```
.\.venv\Scripts\activate
```

Cài đặt các thư viện cần thiết:
```
pip install -r requirements.txt
```

## Chạy code

File chính là notebook `knn.ipynb`, hai file còn lại phục vụ mục đích phân tích. Mở một notebook mong muốn bằng IDE mong muốn và chạy theo thứ tự.