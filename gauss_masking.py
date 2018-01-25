# coding:utf-8
import numpy 
import cv2

#读入图片
im=cv2.imread('')

# 针对不同的检测目标，以其中心为原点，生成蒙版。再将所有蒙版相加



# generate a general masking, centering at the center of a 500*500 image
gen_masking= np.array([500,500])


# 卷积
