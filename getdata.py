import cv2 as cv
import time
import numpy as np
import os

imageCnt = 0
x0 = 300
y0 = 100
width = 300
height = 300
MIN_DESCRIPTOR = 32
imageSaveSwitch = False

def getRoi(frame, x0, y0, width, height):
    roi = frame[y0:y0 + height, x0:x0 + width]
    cv.imshow('roi', roi)
    return roi

def getSkin(frame):
    ycrcb = cv.cvtColor(frame, cv.COLOR_BGR2YCR_CB)
    y, cr, cb = cv.split(ycrcb)
    cr_ = cv.GaussianBlur(cr, (5, 5), 0) # 高斯模糊
    _, skin = cv.threshold(cr_, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU) # otsu二值化 
    ret = cv.bitwise_and(frame, frame, mask=skin)
    return ret

def findContour(Laplacian):
    h = cv.findContours(Laplacian, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contour = h[0]
    contour = sorted(contour, key=cv.contourArea, reverse=True)
    return contour

def trucate(des):
    ret = np.fft.fftshift(des)
    centerIdx = int(len(ret) / 2)
    low, high = centerIdx - int(MIN_DESCRIPTOR / 2), centerIdx + int(MIN_DESCRIPTOR / 2)
    ret = ret[low:high]
    ret = np.fft.ifftshift(ret)
    return ret

def reconstruct(img, desInUse):
    contour_reconstruct = np.fft.ifft(descirptor_in_use)
    contour_reconstruct = np.array([contour_reconstruct.real, contour_reconstruct.imag])
    contour_reconstruct = np.transpose(contour_reconstruct)
    contour_reconstruct = np.expand_dims(contour_reconstruct, axis=1)
    if contour_reconstruct.min() < 0:
        contour_reconstruct -= contour_reconstruct.min()
    contour_reconstruct *= img.shape[0] / contour_reconstruct.max()
    contour_reconstruct = contour_reconstruct.astype(np.int32, copy=False)

    black_np = np.ones(img.shape, np.uint8)  # 创建黑色幕布
    black = cv2.drawContours(black_np, contour_reconstruct, -1, (255, 255, 255), 1)  # 绘制白色轮廓
    cv2.imshow("contour_reconstruct", black)
    return black

def fourier(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    dst = cv.Laplacian(gray, cv.CV_16S, ksize=3)
    Laplacian = cv.convertScaleAbs(dst)
    contour = findContour(Laplacian)
    contourArray = contour[0][:, 0, :]
    retbg = np.ones(dst.shape, np.uint8)
    ret = cv.drawContours(retbg, contour[0], -1, (255, 255, 255), 1)
    contourComplex = np.empty(contourArray.shape[:-1], dtype=complex)
    contourComplex.real = contourArray[:, 0]
    contourComplex.imag = contourArray[:, 1]
    fourierResult = np.fft.fft(contourComplex)
    desInUse = trucate(fourierResult)
    return ret, desInUse



def debug(name, frame):
    cv.imshow(name, frame)

imageMaxiCnt = 300
curImageCnt = 100


def saveSample(folder, image):
    if not os.path.exists(folder):
        os.mkdir(folder)
    global imageCnt
    filename = folder + str(imageCnt).zfill(3) + '.png'
    cv.imwrite(filename, image)
    print('saving ' + filename)
    imageCnt += 1
    time.sleep(0.1)

subtractor = cv.createBackgroundSubtractorKNN(detectShadows=True)

capture = cv.VideoCapture(0)
path = './data/0/'
while True:
    ret, frame = capture.read()
    frame = cv.flip(frame, 1)
    cv.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0))
    cv.imshow('video', frame)
    roi = getRoi(frame, x0, y0 ,width, height)
    Skin = getSkin(roi)
    result, fourierResult = fourier(Skin)
    cv.imshow('result', result)
    if imageSaveSwitch and curImageCnt < imageMaxiCnt:
        saveSample(path, result)
        curImageCnt = curImageCnt + 1
    key = cv.waitKey(1) & 0xff
    if key == ord('q'):
        break
    elif key == ord('s'):
        imageSaveSwitch = not imageSaveSwitch

capture.read()
cv.destroyAllWindows()
