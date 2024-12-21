# DetectChars.py
import os

import cv2
import numpy as np
import math
import random

import Main
import Preprocess
import PossibleChar

# Các biến cấp module ##########################################################################

kNearest = cv2.ml.KNearest_create()

        # hằng số cho checkIfPossibleChar, cái này kiểm tra một ký tự khả thi duy nhất (không so sánh với ký tự khác)
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

        # hằng số dùng để so sánh hai ký tự
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

        # các hằng số khác
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

###################################################################################################
def loadKNNDataAndTrainKNN():
    allContoursWithData = []                # khai báo các danh sách rỗng,
    validContoursWithData = []              # chúng ta sẽ điền vào đây trong thời gian tới

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # đọc các phân loại huấn luyện
    except:                                                                                 # nếu không thể mở file
        print("Lỗi, không thể mở file classifications.txt, thoát chương trình\n")  # hiển thị thông báo lỗi
        os.system("pause")
        return False                                                                        # và trả về False
    # end try

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # đọc các ảnh huấn luyện
    except:                                                                                 # nếu không thể mở file
        print("Lỗi, không thể mở file flattened_images.txt, thoát chương trình\n")  # hiển thị thông báo lỗi
        os.system("pause")
        return False                                                                        # và trả về False
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # thay đổi kích thước mảng numpy thành 1d, cần thiết để truyền vào huấn luyện

    kNearest.setDefaultK(1)                                                             # đặt K mặc định là 1

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)           # huấn luyện đối tượng KNN

    return True                             # nếu đến đây, việc huấn luyện thành công nên trả về True
# end function


def detectCharsInPlates(listOfPossiblePlates):
    intPlateCounter = 0
    imgContours = None
    contours = []

    if len(listOfPossiblePlates) == 0:          # nếu danh sách các biển số khả thi trống
        return listOfPossiblePlates             # trả về ngay
    # end if

            # tại thời điểm này, chúng ta có thể chắc chắn rằng danh sách các biển số khả thi có ít nhất một biển số

    for possiblePlate in listOfPossiblePlates:          # với mỗi biển số khả thi, vòng lặp lớn này chiếm phần lớn chức năng

        possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(possiblePlate.imgPlate)     # xử lý ảnh để có ảnh grayscale và ảnh threshold

        if Main.showSteps == True: # hiển thị các bước
            cv2.imshow("5a", possiblePlate.imgPlate)
            cv2.imshow("5b", possiblePlate.imgGrayscale)
            cv2.imshow("5c", possiblePlate.imgThresh)
        # end if # hiển thị các bước

                # tăng kích thước ảnh biển số để dễ dàng xem và phát hiện ký tự
        possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = 1.6, fy = 1.6)

                # threshold lại để loại bỏ các vùng xám
        thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        if Main.showSteps == True: # hiển thị các bước
            cv2.imshow("5d", possiblePlate.imgThresh)
        # end if # hiển thị các bước

                # tìm tất cả các ký tự khả thi trong biển số,
                # chức năng này đầu tiên tìm tất cả các đường viền, sau đó chỉ bao gồm các đường viền có thể là ký tự (chưa so sánh với ký tự khác)
        listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh)

        if Main.showSteps == True: # hiển thị các bước
            height, width, numChannels = possiblePlate.imgPlate.shape
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]                                         # xóa danh sách contours

            for possibleChar in listOfPossibleCharsInPlate:
                contours.append(possibleChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)

            cv2.imshow("6", imgContours)
        # end if # hiển thị các bước

                # với một danh sách tất cả các ký tự khả thi, tìm các nhóm ký tự khớp trong biển số
        listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)

        if Main.showSteps == True: # hiển thị các bước
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]

            for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
                intRandomBlue = random.randint(0, 255)
                intRandomGreen = random.randint(0, 255)
                intRandomRed = random.randint(0, 255)

                for matchingChar in listOfMatchingChars:
                    contours.append(matchingChar.contour)
                # end for
                cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for
            cv2.imshow("7", imgContours)
        # end if # hiển thị các bước

        if (len(listOfListsOfMatchingCharsInPlate) == 0):			# nếu không tìm thấy nhóm ký tự nào trong biển số

            if Main.showSteps == True: # hiển thị các bước
                print("Không tìm thấy ký tự trong biển số " + str(
                    intPlateCounter) + " = (không có), nhấn vào bất kỳ ảnh nào và nhấn một phím để tiếp tục . . .")
                intPlateCounter = intPlateCounter + 1
                cv2.destroyWindow("8")
                cv2.destroyWindow("9")
                cv2.destroyWindow("10")
                cv2.waitKey(0)
            # end if # hiển thị các bước

            possiblePlate.strChars = ""
            continue						# quay lại đầu vòng lặp for
        # end if

        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):                              # trong mỗi danh sách ký tự khớp
            listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)        # sắp xếp ký tự từ trái sang phải
            listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i])              # và loại bỏ các ký tự chồng lên nhau
        # end for

        if Main.showSteps == True: # hiển thị các bước
            imgContours = np.zeros((height, width, 3), np.uint8)

            for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
                intRandomBlue = random.randint(0, 255)
                intRandomGreen = random.randint(0, 255)
                intRandomRed = random.randint(0, 255)

                del contours[:]

                for matchingChar in listOfMatchingChars:
                    contours.append(matchingChar.contour)
                # end for

                cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for
            cv2.imshow("8", imgContours)
        # end if # hiển thị các bước

                # trong mỗi biển số khả thi, giả sử rằng danh sách dài nhất của các ký tự khớp là danh sách ký tự thực sự
        intLenOfLongestListOfChars = 0
        intIndexOfLongestListOfChars = 0

                # lặp qua tất cả các vector ký tự khớp, lấy chỉ mục của cái có nhiều ký tự nhất
        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
            if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
                intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
                intIndexOfLongestListOfChars = i
            # end if
        # end for

                # giả sử rằng danh sách dài nhất của các ký tự khớp trong biển số là danh sách ký tự thực sự
        longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]

        if Main.showSteps == True: # hiển thị các bước
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]

            for matchingChar in longestListOfMatchingCharsInPlate:
                contours.append(matchingChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)

            cv2.imshow("9", imgContours)
        # end if # hiển thị các bước

        possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)

        if Main.showSteps == True: # hiển thị các bước
            print("Ký tự tìm thấy trong biển số " + str(
                intPlateCounter) + " = " + possiblePlate.strChars + ", nhấn vào bất kỳ ảnh nào và nhấn một phím để tiếp tục . . .")
            intPlateCounter = intPlateCounter + 1
            cv2.waitKey(0)
        # end if # hiển thị các bước

    # end of vòng lặp lớn chiếm phần lớn chức năng

    if Main.showSteps == True:
        print("\nHoàn tất phát hiện ký tự, nhấn vào bất kỳ ảnh nào và nhấn một phím để tiếp tục . . .\n")
        cv2.waitKey(0)
    # end if

    return listOfPossiblePlates
# end function


def findPossibleCharsInPlate(imgGrayscale, imgThresh):
    listOfPossibleChars = []                        # đây sẽ là giá trị trả về
    contours = []
    imgThreshCopy = imgThresh.copy()

            # tìm tất cả các đường viền trong biển số
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:                        # với mỗi đường viền
        possibleChar = PossibleChar.PossibleChar(contour)

        if checkIfPossibleChar(possibleChar):              # nếu đường viền là một ký tự khả thi, lưu ý là chưa so sánh với ký tự khác (chưa)
            listOfPossibleChars.append(possibleChar)       # thêm vào danh sách các ký tự khả thi
        # end if
    # end if

    return listOfPossibleChars
# end function


def checkIfPossibleChar(possibleChar):
            # chức năng này là "kiểm tra sơ bộ" để xem một đường viền có thể là một ký tự không,
            # lưu ý là chúng ta chưa so sánh ký tự này với ký tự khác để tìm nhóm ký tự
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False
    # end if
# end function


def findListOfListsOfMatchingChars(listOfPossibleChars):
            # với chức năng này, chúng ta bắt đầu với tất cả các ký tự khả thi trong một danh sách lớn
            # mục đích của chức năng này là sắp xếp lại danh sách lớn của các ký tự thành các danh sách con của các ký tự khớp,
            # lưu ý là các ký tự không nằm trong nhóm khớp không cần phải được xem xét thêm
    listOfListsOfMatchingChars = []                  # đây sẽ là giá trị trả về

    for possibleChar in listOfPossibleChars:                        # với mỗi ký tự khả thi trong danh sách lớn
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        # tìm tất cả các ký tự trong danh sách lớn khớp với ký tự hiện tại

        listOfMatchingChars.append(possibleChar)                # cũng thêm ký tự hiện tại vào danh sách ký tự khớp

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:     # nếu danh sách các ký tự khớp không đủ dài để cấu thành một biển số khả thi
            continue                            # quay lại đầu vòng lặp for và thử với ký tự tiếp theo, lưu ý không cần phải lưu lại danh sách này
                                                # vì nó không đủ ký tự để là một biển số khả thi
        # end if

                                                # nếu đến đây, nghĩa là danh sách hiện tại đã vượt qua kiểm tra là một "nhóm" hoặc "cụm" các ký tự khớp
        listOfListsOfMatchingChars.append(listOfMatchingChars)      # thêm vào danh sách các danh sách các ký tự khớp

        listOfPossibleCharsWithCurrentMatchesRemoved = []          # loại bỏ các ký tự đã khớp khỏi danh sách lớn

                                                # loại bỏ các ký tự khớp hiện tại khỏi danh sách lớn để không sử dụng các ký tự đó lần nữa,
                                                # cần phải tạo một danh sách lớn mới vì không muốn thay đổi danh sách gốc
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)      # gọi đệ quy

        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        # với mỗi danh sách các ký tự khớp tìm được từ gọi đệ quy
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             # thêm vào danh sách các danh sách ký tự khớp
        # end for

        break       # thoát vòng lặp for

    # end for

    return listOfListsOfMatchingChars
# end function


def findListOfMatchingChars(possibleChar, listOfChars):
            # mục đích của chức năng này là, given một ký tự khả thi và một danh sách lớn các ký tự khả thi,
            # tìm tất cả các ký tự trong danh sách lớn khớp với ký tự đơn và trả về những ký tự khớp đó dưới dạng một danh sách
    listOfMatchingChars = []                # đây sẽ là giá trị trả về

    for possibleMatchingChar in listOfChars:                # với mỗi ký tự trong danh sách lớn
        if possibleMatchingChar == possibleChar:    # nếu ký tự chúng ta đang tìm kiếm là chính xác ký tự giống hệt với ký tự trong danh sách lớn
                                                    # thì chúng ta không nên đưa nó vào danh sách khớp vì điều này sẽ gây ra việc thêm ký tự hiện tại vào danh sách hai lần
            continue                                # vì vậy không thêm vào danh sách khớp và quay lại đầu vòng lặp for
        # end if
                    # tính toán các yếu tố để xem các ký tự có khớp hay không
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)

        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)

        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

                # kiểm tra nếu các ký tự có khớp không
        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):

            listOfMatchingChars.append(possibleMatchingChar)        # nếu các ký tự khớp, thêm ký tự hiện tại vào danh sách ký tự khớp
        # end if
    # end for

    return listOfMatchingChars                  # trả về kết quả
# end function


# sử dụng định lý Pythagoras để tính khoảng cách giữa hai ký tự
def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))
# end function

# sử dụng lượng giác cơ bản (SOH CAH TOA) để tính góc giữa hai ký tự
def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:                           # kiểm tra để chắc chắn không chia cho 0 nếu vị trí X của trung tâm là giống nhau, chia cho 0 sẽ gây lỗi trong Python
        fltAngleInRad = math.atan(fltOpp / fltAdj)      # nếu cạnh kề khác 0, tính góc
    else:
        fltAngleInRad = 1.5708                          # nếu cạnh kề bằng 0, dùng giá trị này làm góc, điều này để thống nhất với phiên bản C++ của chương trình này
    # end if

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)       # tính góc theo độ

    return fltAngleInDeg
# end function


# nếu chúng ta có hai ký tự chồng lên nhau hoặc quá gần nhau để có thể là hai ký tự riêng biệt, loại bỏ ký tự bên trong (nhỏ hơn),
# mục đích là để tránh việc bao gồm cùng một ký tự hai lần nếu hai đường viền được tìm thấy cho cùng một ký tự,
# ví dụ đối với chữ 'O' cả vòng trong và vòng ngoài có thể được tìm thấy như là các đường viền, nhưng chúng ta chỉ nên bao gồm ký tự đó một lần
def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)                # đây sẽ là giá trị trả về

    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            if currentChar != otherChar:        # nếu ký tự hiện tại và ký tự khác không phải là cùng một ký tự . . .
                                                                            # nếu vị trí trung tâm của ký tự hiện tại và ký tự khác gần giống nhau . . .
                if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                                # nếu vào đây, có nghĩa là chúng ta đã tìm thấy các ký tự chồng lên nhau
                                # tiếp theo, chúng ta xác định ký tự nào nhỏ hơn, nếu ký tự đó chưa bị loại bỏ trong lần kiểm tra trước thì sẽ loại bỏ
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:         # nếu ký tự hiện tại nhỏ hơn ký tự khác
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:              # nếu ký tự hiện tại chưa bị loại bỏ trong lần kiểm tra trước . . .
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)         # thì loại bỏ ký tự hiện tại
                        # end if
                    else:                                                                       # nếu ký tự khác nhỏ hơn ký tự hiện tại
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:                # nếu ký tự khác chưa bị loại bỏ trong lần kiểm tra trước . . .
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)           # thì loại bỏ ký tự khác
                        # end if
                    # end if
                # end if
            # end if
        # end for
    # end for

    return listOfMatchingCharsWithInnerCharRemoved
# end function


# đây là nơi chúng ta áp dụng nhận diện ký tự thực tế
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = ""               # đây sẽ là giá trị trả về, các ký tự trong biển số

    height, width = imgThresh.shape

    imgThreshColor = np.zeros((height, width, 3), np.uint8)

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sắp xếp ký tự từ trái sang phải

    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)                     # tạo phiên bản màu của ảnh threshold để chúng ta có thể vẽ đường viền màu lên đó

    for currentChar in listOfMatchingChars:                                         # với mỗi ký tự trong biển số
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

        cv2.rectangle(imgThreshColor, pt1, pt2, Main.SCALAR_GREEN, 2)           # vẽ hình chữ nhật màu xanh quanh ký tự

                # cắt ký tự ra khỏi ảnh threshold
        imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))           # thay đổi kích thước ảnh, điều này cần thiết cho nhận diện ký tự

        npaROIResized = imgROIResized.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))        # làm phẳng ảnh thành mảng 1d numpy

        npaROIResized = np.float32(npaROIResized)               # chuyển từ mảng 1d numpy các số nguyên sang mảng 1d numpy các số thực

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)              # cuối cùng chúng ta có thể gọi hàm findNearest !!!

        strCurrentChar = str(chr(int(npaResults[0][0])))            # lấy ký tự từ kết quả

        strChars = strChars + strCurrentChar                        # nối ký tự hiện tại vào chuỗi ký tự hoàn chỉnh

    # end for

    if Main.showSteps == True: # hiển thị các bước
        cv2.imshow("10", imgThreshColor)
    # end if # hiển thị các bước

    return strChars
# end function

