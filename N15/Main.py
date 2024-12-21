import cv2
import numpy as np
import os
import time
from plot_training import plot_training_results  # Import hàm vẽ biểu đồ

import DetectChars
import DetectPlates
import PossiblePlate

# Các biến cấp module 
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

# Các biến để lưu thông tin huấn luyện
num_chars_detected = []  # Lưu số ký tự nhận diện được trong mỗi ảnh
training_times = []  # Lưu thời gian huấn luyện cho mỗi ảnh


def main():
    # Bắt đầu thời gian huấn luyện
    start_time = time.time()

    # Thử huấn luyện mô hình KNN
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         

    if blnKNNTrainingSuccessful == False:                               # Nếu huấn luyện KNN không thành công
        print("\nerror: KNN training was not successful\n")  # Hiển thị thông báo lỗi
        return                                                          # Thoát chương trình
    # Kết thúc if

    # Lựa chọn hình ảnh đầu vào từ menu
    imgOriginalScene = choose_image()

    if imgOriginalScene is None:  # Nếu ảnh không được đọc thành công
        print("\nerror: image not read from file \n\n")  # Thông báo lỗi
        os.system("pause")  # Tạm dừng để người dùng xem thông báo lỗi
        return  # Thoát chương trình

    # Phát hiện biển số xe trong ảnh
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    # Nhận diện ký tự trên biển số
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    cv2.imshow("imgOriginalScene", imgOriginalScene)  # Hiển thị ảnh gốc

    if len(listOfPossiblePlates) == 0:  # Nếu không phát hiện biển số nào
        print("\nno license plates were detected\n")  # Thông báo không tìm thấy biển số
    else:  # Nếu có biển số
        # Nếu vào đây, danh sách biển số tiềm năng chứa ít nhất một biển số

        # Sắp xếp danh sách biển số theo số lượng ký tự nhận diện được (giảm dần)
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # Giả sử biển số với số ký tự nhận diện được nhiều nhất (đầu tiên trong danh sách) là biển số chính xác
        licPlate = listOfPossiblePlates[0]

        # Hiển thị ảnh cắt của biển số và ảnh ngưỡng
        cv2.imshow("imgPlate", licPlate.imgPlate)
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:  # Nếu không nhận diện được ký tự nào trên biển số
            print("\nno characters were detected\n\n")  # Thông báo
            return  # Thoát chương trình
        # Kết thúc if

        # Vẽ hình chữ nhật đỏ xung quanh biển số
        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)

        # Hiển thị ký tự nhận diện được từ biển số
        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")

        # Ghi ký tự biển số lên ảnh gốc
        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)

        # Hiển thị lại ảnh gốc
        cv2.imshow("imgOriginalScene", imgOriginalScene)

        # Lưu ảnh gốc với chú thích ra file
        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

        # Lưu số ký tự nhận diện được và thời gian huấn luyện cho biểu đồ
        num_chars_detected.append(len(licPlate.strChars))
        training_times.append(time.time() - start_time)

    # Kết thúc if else

    cv2.waitKey(0)  # Giữ các cửa sổ mở cho đến khi người dùng nhấn phím

    # Vẽ biểu đồ huấn luyện
    plot_training_results(num_chars_detected, training_times)  # Gọi hàm vẽ biểu đồ từ file plot_training.py

    return


# Hàm vẽ hình chữ nhật đỏ xung quanh biển số
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    # Lấy 4 đỉnh của hình chữ nhật quay (rotated rectangle)
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)

    # Chuyển đổi các tọa độ góc về kiểu integer
    p2fRectPoints = np.int0(p2fRectPoints)

    # Tính tâm, chiều rộng và chiều cao của biển số
    rectCenter, (rectWidth, rectHeight), rectAngle = licPlate.rrLocationOfPlateInScene

    # Mở rộng khung bao theo tỷ lệ (tăng kích thước)
    scaleWidth = 1.0  # Tăng chiều rộng lên 20%
    scaleHeight = 1.7  # Tăng chiều cao lên 50%

    # Tính chiều rộng và chiều cao mới sau khi mở rộng
    newWidth = rectWidth * scaleWidth
    newHeight = rectHeight * scaleHeight

    # Tạo hình chữ nhật quay với kích thước mở rộng
    expandedRect = ((rectCenter, (newWidth, newHeight), rectAngle))

    # Lấy lại 4 góc của hình chữ nhật mở rộng
    expandedPoints = cv2.boxPoints(expandedRect)
    expandedPoints = np.int0(expandedPoints)

    # Vẽ các đường kết nối 4 điểm để tạo khung bao
    cv2.line(imgOriginalScene, tuple(expandedPoints[0]), tuple(expandedPoints[1]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(expandedPoints[1]), tuple(expandedPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(expandedPoints[2]), tuple(expandedPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(expandedPoints[3]), tuple(expandedPoints[0]), SCALAR_RED, 2)

# Hàm ghi ký tự biển số lên ảnh
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0  # Tọa độ tâm của vùng sẽ ghi ký tự
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0  # Tọa độ góc dưới bên trái của vùng sẽ ghi ký tự
    ptLowerLeftTextOriginY = 0

    # Lấy kích thước ảnh và biển số
    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX  # Chọn font chữ đơn giản
    fltFontScale = float(plateHeight) / 30.0  # Tỷ lệ font dựa trên chiều cao của biển số
    intFontThickness = int(round(fltFontScale * 1.5))  # Độ dày font dựa trên tỷ lệ font

    # Tính toán kích thước văn bản
    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)

    # Giải nén tọa độ của hình chữ nhật quay
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)  # Đảm bảo tọa độ trung tâm là số nguyên
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)  # Vị trí ngang của vùng văn bản trùng với biển số

    # Xác định vị trí văn bản dựa vào vị trí biển số trong ảnh
    if intPlateCenterY < (sceneHeight * 0.75):
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))  # Ghi văn bản dưới biển số
    else:
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))  # Ghi văn bản trên biển số

    # Kết thúc if

    # Giải nén kích thước văn bản
    textSizeWidth, textSizeHeight = textSize

    # Tính tọa độ góc dưới bên trái của vùng văn bản
    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))

    # Ghi văn bản lên ảnh
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)

# Hàm chọn hình ảnh
def choose_image():
    # Liệt kê các hình ảnh có sẵn trong thư mục
    image_folder = "LicPlateImages/"
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg'))]

    print("Chọn hình ảnh bằng cách nhập số tương ứng:")
    for idx, image_file in enumerate(image_files):
        print(f"{idx+1}. {image_file}")

    choice = input("Nhập số để chọn hình ảnh: ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(image_files):
            image_path = os.path.join(image_folder, image_files[choice - 1])
            img = cv2.imread(image_path)
            return img
        else:
            print("Lựa chọn không hợp lệ!")
            return None
    except ValueError:
        print("Vui lòng nhập số!")
        return None


if __name__ == "__main__":
    main()
