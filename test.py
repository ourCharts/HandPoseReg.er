import numpy as np
import cv2
imname = "./95.JPG"
# 读入图像
'''
使用函数 cv2.imread() 读入图像。这幅图像应该在此程序的工作路径，或者给函数提供完整路径.
警告：就算图像的路径是错的，OpenCV 也不会提醒你的，但是当你使用命令print(img)时得到的结果是None。
'''
img = cv2.imread(imname, cv2.IMREAD_COLOR)
'''
imread函数的第一个参数是要打开的图像的名称(带路径)
第二个参数是告诉函数应该如何读取这幅图片. 其中
    cv2.IMREAD_COLOR 表示读入一副彩色图像, alpha 通道被忽略, 默认值
    cv2.IMREAD_ANYCOLOR 表示读入一副彩色图像
    cv2.IMREAD_GRAYSCALE 表示读入一副灰度图像
    cv2.IMREAD_UNCHANGED 表示读入一幅图像，并且包括图像的 alpha 通道
'''
# 显示图像
'''
使用函数 cv2.imshow() 显示图像。窗口会自动调整为图像大小。第一个参数是窗口的名字，
其次才是我们的图像。你可以创建多个窗口，只要你喜欢，但是必须给他们不同的名字.
'''
cv2.imshow("image", img) # "image" 参数为图像显示窗口的标题, img是待显示的图像数据
cv2.waitKey(0) #等待键盘输入,参数表示等待时间,单位毫秒.0表示无限期等待
cv2.destroyAllWindows() # 销毁所有cv创建的窗口
# 也可以销毁指定窗口:
#cv2.destroyWindow("image") # 删除窗口标题为"image"的窗口
# 保存图像
'''
使用函数 cv2.imwrite() 来保存一个图像。首先需要一个文件名，之后才是你要保存的图像。
保存的图片的格式由后缀名决定.
'''
#cv2.imwrite(imname + "01.png", img) 
cv2.imwrite(imname + "01.jpg", img)

#肤色检测之一: YCrCb之Cr分量 + OTSU二值化
img = cv2.imread(imname, cv2.IMREAD_COLOR)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb) # 把图像转换到YUV色域
(y, cr, cb) = cv2.split(ycrcb) # 图像分割, 分别获取y, cr, br通道图像
# 高斯滤波, cr 是待滤波的源图像数据, (5,5)是值窗口大小, 0 是指根据窗口大小来计算高斯函数标准差
cr1 = cv2.GaussianBlur(cr, (5, 5), 0) # 对cr通道分量进行高斯滤波
# 根据OTSU算法求图像阈值, 对图像进行二值化
_, skin1 = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 
cv2.imshow("image CR", cr1)
cv2.imshow("Skin Cr+OSTU", skin1 )
cv2.waitKey(0)
# 肤色检测之二: YCrCb中 140<=Cr<=175 100<=Cb<=120
img = cv2.imread(imname, cv2.IMREAD_COLOR)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb) # 把图像转换到YUV色域
(y, cr, cb) = cv2.split(ycrcb) # 图像分割, 分别获取y, cr, br通道分量图像
skin2 = np.zeros(cr.shape, dtype=np.uint8) # 根据源图像的大小创建一个全0的矩阵,用于保存图像数据
(x, y) = cr.shape # 获取源图像数据的长和宽
# 遍历图像, 判断Cr和Br通道的数值, 如果在指定范围中, 则置把新图像的点设为255,否则设为0
for i in  range(0, x): 
    for j in  range(0, y):
        if (cr[i][j] >  140) and (cr[i][j] <  175) and (cb[i][j] >  100) and (cb[i][j] <  120):
            skin2[i][j] =  255
        else:
            skin2[i][j] =  0
cv2.imshow(imname, img)

cv2.waitKey(0)
cv2.imshow(imname +  " Skin2 Cr+Cb", skin2)

cv2.waitKey(0)