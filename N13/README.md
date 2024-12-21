# ML241
# Hệ thống đánh giá chất lượng đất
# Overview
Mô hình được training từ tập dataset cho trước
Mô hình chạy dự đoán trên một 100 bộ dữ liệu để tính ra mức Accuracy
Mô hình chạy dự đoán theo dữ liệu người dùng nhập vào
# Technologies
Python 3.12.7
Thư viện python được sử dụng:
    Numpy
    csv
# Input Feature
Thông số đưa vào được lấy dựa trên cảm biến ES-NPK-01:
Đạm (N) 1-1999 mg/kg (mg/L)
Lân (P) 1-1999 mg/kg (mg/L)
Kali (K) 1-1999 mg/kg (mg/L)
# Output Label
Có 4 nhãn đánh giá tương ứng với 4 lớp đầu ra của mô hình:
Thấp, nghèo
Trung bình
Trung bình đến giàu
Rất giàu

# Training Parameters
learning_rate = 0.01
num_iterations = 1000
batch_size = 32

# Operating instructions
Chạy file training.py để tiến hành training mô hình từ tập dữ liệu lấy từ dataset.csv
Để kiểm tra ma trận trọng số và bias sau khi training sẽ được lưu vào weight.csv
Để cho mô hình chạy đánh giá chất lượng đất chạy file running.py
File running.py sẽ có 2 phần bao gồm: đánh giá 100 dữ liệu lấy từ dataset_bonus.csv và đánh giá dữ liệu được người dùng nhập vào