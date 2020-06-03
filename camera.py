import cv2 as cv2
import numpy as np

# capture = cv2.VideoCapture(0)
# index = 1
# while True:
#     ret, frame = capture.read()
#     if ret is True:
#         cv2.imshow("frame", frame)
#         index += 1
#         if index % 5 == 0:
#             cv2.imwrite("./" + str(index) + ".jpg", frame)
#         c = cv2.waitKey(50)
#         if c == 27: # ESC
#             break
#     else:
#         break

# cv2.destroyAllWindows()



def skinMask(roi):
    YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
    (y,cr,cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
    cr1 = cv2.GaussianBlur(cr, (5,5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Ostu处理
    res = cv2.bitwise_and(roi,roi, mask = skin)
    return res


def process_photo(name):
    imgName = name
    kernel_size = (5, 5)
    sigma = 1.5
    img = cv2.imread(imgName)
    img = cv2.GaussianBlur(img, kernel_size, sigma)
    # new_imgName = "New_" + str(kernel_size[0]) + "_" + str(sigma) + "_" + imgName
    # cv2.imwrite(new_imgName, img)

    img = skinMask(img)
    # cv2.imshow("Image",img)#显示图像
    # cv2.waitKey()
    image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#将图像转化为灰度图像
    # cv2.imshow("Image",image)#显示图像
    # cv2.waitKey()
    #Canny边缘检测
    canny = cv2.Canny(image,30,150)
    return canny
    # cv2.imshow("Canny",canny)
    # cv2.waitKey()

img = process_photo('./New_5_1.5_205.jpg')
cv2.imwrite("./Sign-Language-Digits-Dataset/1/New_5_1.5_205.jpg", img)
