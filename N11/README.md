# ML241
Nhóm 11 - ML241:
Thành viên: Nguyễn Lê Quang Huy, Kim Sô Vút Thi

(Mở README.md này ở mode Code, không phải Preview) 
Hướng dẫn chạy code mô hình "Dự đoán chất lượng sản phẩm rượu đỏ Bồ Đào Nha"

Chuẩn bị file dataset, có đường dẫn "ML241/N11/dataset"
  + Tải xuống máy 
  + Mở sẵn file bằng ứng dụng như Notepad nhằm copy dữ liệu của 1 sản phẩm rượu bất kỳ

I. Chương trình sử dụng Random Forest, link Google Collab: https://colab.research.google.com/drive/1wWMZFhaolsM_-WAhuZIH9EsLtAbAU9Gt?usp=sharing
  Thầy và các bạn chạy lần lượt các cell code từ trên xuống theo mục lục sau
  Table of contents
      1. Thư viện được sử dụng
      2. Dataset           (chỉ cần chạy cell đầu tiên _ load dataset)
      3. *Phần mở rộng: Phân tích bộ dataset rượu đỏ     (có thể bỏ qua)
      4. Phần giải thuật chính: Các bước training cho mô hình dự đoán
      .
      5. Triển khai mô hình dự đoán chất lượng rượu
      ****Hướng dẫn nhập input:
          + Mở file "winequality-red.csv" bằng Notepad, hay các phần mềm text tương tự ...
          + Chọn 1 hàng bất kỳ (1 hàng là 1 sản phẩm rượu, gồm 11 thông số và 1 giá trị kết quả)
          + Copy 11 số đầu tiên trong list/mảng ở hàng đó, trừ con số cuối cùng (Quality) ra
          + Dán vào phần mảng của lệnh khai báo biến input, nó sẽ trông như:
                new_input = np.array([7.9,0.35,0.46,3.6,0.078,15.0,37.0,0.9973,3.35,0.86,12.8]) 
          + Chạy code/cell, kết quả sẽ trông như thế này:
                Bộ 11 thông số của sản phẩm rượu cần đánh giá:
                               [ 7.9   0.35  0.46  3.6   0.08 15.   37.    1.    3.35  0.86 12.8 ]
                Chất lượng rượu tốt
          + Trong code, chọn ngưỡng phân lớp cho label là Quality = 6 (score 1 đến 10), các bạn hãy so sánh:
                Kết quả print " Chất lượng rượu ...... "    so với   Con số cuối cùng (Quality thật sự) trong list mà các bạn lấy 11 giá trị làm input
                                                                        (từ dataset)  <6 Chưa tốt      và     >=6 Chất lượng tốt
      *
      6. Mô phỏng đơn giản chiến lược marketing của hãng (Tạo 50 mẫu input ngẫu nhiên)
    -----------
      Github operation commands (Don't open here)
    *
II. Chương trình sử dụng Logistic Regression, link Google Collab: https://colab.research.google.com/drive/19OHkWdfYxcNfwIGq1UK5JZpIE3FB-q4C?usp=sharing
  
   Trước khi load dataset: Mọi người chịu khó upload file dataset (đã tải từ "ML241/N11/dataset/winequality-red.csv") lên thẳng trang Google Collab của link trên 
   (vì em không thể clone folder repo vào 2 notebook khác nhau đc)
   
   Thầy và các bạn cũng chạy lần lượt các cell code từ trên xuống đến khi gặp:
  .........
        A. Build a Predictive model (single manual input)
        *****Thực hiện tương tự như Chương trình (I) trên
  ------B. Mô phỏng đơn giản chiến lược marketing của hãng (Tạo 50 mẫu input ngẫu nhiên)
