# DetectPlates.py

import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

# Các biến cấp module
PLATE_WIDTH_PADDING_FACTOR = 1.1
PLATE_HEIGHT_PADDING_FACTOR = 1.1


def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []                   # Đây sẽ là giá trị trả về

    height, width, numChannels = imgOriginalScene.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True: # Hiển thị các bước
        cv2.imshow("0", imgOriginalScene)
    # end if # Hiển thị các bước

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)         # Tiền xử lý để có ảnh grayscale và ảnh threshold

    if Main.showSteps == True: # Hiển thị các bước
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)
    # end if # Hiển thị các bước

            # Tìm tất cả các ký tự khả thi trong cảnh,
            # Chức năng này đầu tiên tìm tất cả các đường viền, sau đó chỉ bao gồm các đường viền có thể là ký tự (chưa so sánh với các ký tự khác)
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    if Main.showSteps == True: # Hiển thị các bước
        print("Bước 2 - len(listOfPossibleCharsInScene) = " + str(
            len(listOfPossibleCharsInScene)))  # 131 với ảnh MCLRNF1

        imgContours = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar.contour)
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("2b", imgContours)
    # end if # Hiển thị các bước

            # Với danh sách tất cả các ký tự khả thi, tìm các nhóm ký tự khớp
            # Trong các bước tiếp theo, mỗi nhóm ký tự khớp sẽ cố gắng được nhận diện là một biển số
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    if Main.showSteps == True: # Hiển thị các bước
        print("Bước 3 - listOfListsOfMatchingCharsInScene.Count = " + str(
            len(listOfListsOfMatchingCharsInScene)))  # 13 với ảnh MCLRNF1

        imgContours = np.zeros((height, width, 3), np.uint8)

        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)

            contours = []

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        # end for

        cv2.imshow("3", imgContours)
    # end if # Hiển thị các bước

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                   # Với mỗi nhóm ký tự khớp
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)         # Cố gắng trích xuất biển số

        if possiblePlate.imgPlate is not None:                          # Nếu biển số được tìm thấy
            listOfPossiblePlates.append(possiblePlate)                  # Thêm vào danh sách các biển số khả thi
        # end if
    # end for

    print("\n" + str(len(listOfPossiblePlates)) + " biển số khả thi đã tìm thấy")  # 13 với ảnh MCLRNF1

    if Main.showSteps == True: # Hiển thị các bước
        print("\n")
        cv2.imshow("4a", imgContours)

        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = cv2.boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)

            cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)

            print("Biển số khả thi " + str(i) + ", nhấn vào bất kỳ ảnh nào và nhấn một phím để tiếp tục . . .")

            cv2.imshow("4b", listOfPossiblePlates[i].imgPlate)
            cv2.waitKey(0)
        # end for

        print("\nHoàn thành phát hiện biển số, nhấn vào bất kỳ ảnh nào và nhấn một phím để bắt đầu nhận diện ký tự . . .\n")
        cv2.waitKey(0)
    # end if # Hiển thị các bước

    return listOfPossiblePlates
# end function


def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []                # Đây sẽ là giá trị trả về

    intCountOfPossibleChars = 0

    imgThreshCopy = imgThresh.copy()

    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   # Tìm tất cả các đường viền

    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contours)):                       # Với mỗi đường viền

        if Main.showSteps == True: # Hiển thị các bước
            cv2.drawContours(imgContours, contours, i, Main.SCALAR_WHITE)
        # end if # Hiển thị các bước

        possibleChar = PossibleChar.PossibleChar(contours[i])

        if DetectChars.checkIfPossibleChar(possibleChar):                   # Nếu đường viền là một ký tự khả thi, lưu ý là chưa so sánh với các ký tự khác (chưa)
            intCountOfPossibleChars = intCountOfPossibleChars + 1           # Tăng số lượng ký tự khả thi
            listOfPossibleChars.append(possibleChar)                        # Và thêm vào danh sách các ký tự khả thi
        # end if
    # end for

    if Main.showSteps == True: # Hiển thị các bước
        print("\nBước 2 - len(contours) = " + str(len(contours)))  # 2362 với ảnh MCLRNF1
        print("Bước 2 - intCountOfPossibleChars = " + str(intCountOfPossibleChars))  # 131 với ảnh MCLRNF1
        cv2.imshow("2a", imgContours)
    # end if # Hiển thị các bước

    return listOfPossibleChars
# end function


def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()           # Đây sẽ là giá trị trả về

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # Sắp xếp ký tự từ trái sang phải dựa trên vị trí x

            # Tính toán điểm trung tâm của biển số
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

            # Tính toán chiều rộng và chiều cao của biển số
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

            # Tính toán góc điều chỉnh của vùng biển số
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

            # Đóng gói điểm trung tâm của biển số, chiều rộng và chiều cao, và góc điều chỉnh vào biến thành viên rotated rect của biển số
    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

            # Các bước cuối cùng là thực hiện xoay thực tế

            # Lấy ma trận xoay cho góc điều chỉnh đã tính toán
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape      # Giải nén chiều rộng và chiều cao của ảnh gốc

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # Xoay toàn bộ ảnh

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    possiblePlate.imgPlate = imgCropped         # Sao chép ảnh biển số đã cắt vào biến thành viên thích hợp của biển số khả thi

    return possiblePlate
# end function
