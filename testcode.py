from __future__ import division
from scipy.interpolate import spline
import cv2
import numpy as np
import matplotlib.pyplot as plt

X = 157
Y = 181
in_image = cv2.imread('testFog.png', 0)
image = cv2.resize(in_image, (181, 157))
out_file = cv2.imread('output_file.png', 0)


# Canny and show Edge To dam cac vung canh duoc phat hien
# edges = cv2.Canny(in_image, 8, 100)
#
# indices = np.where(edges == 255)
# print indices
# coordinates = zip(indices[0], indices[1])
# for i in range(0, len(coordinates)):
#     print coordinates[i]
#     y = coordinates[i][0]
#     x = coordinates[i][1]
#     in_image[min(y+1, 360), x] = 0
#     in_image[coordinates[i]] = 0
#
# cv2.imshow('Canny', edges)
#
heigh, width = out_file.shape[:2]
# print("heigh " + str(heigh))
# print("width " + str(width))

# mang B chua cac diem anh mau trang la region_growing
B = []
for i in range(0, heigh-1):
    # print 'line' + str(i)
    dis = 0
    temp = 0
    begin = 0
    end = 0
    for j in range(0,width):
        if (out_file[i, j] == 255):
            # print 'temp' + str(temp)
            temp = temp + 1
        else:
            if (dis < temp):
                dis = temp
                end = j - 1
                begin = j - temp
                temp = 0
            temp = 0
    # print 'dis' + str(dis)
    # print begin
    # print end
    if (begin == 0 and end == 0):
        end = width - 1
        dis = width - 1
    B.append([i, begin, end, end - begin + 1])
# print B
luminance = []
for i in range(0, len(B)):
    tong = 0
    for j in range(B[i][1], B[i][2] + 1):
        tong = tong + in_image[i, j]
    luminance.append([i, tong / B[i][3]])

axisx = []
axisy = []
deriy = []
# print luminance
print luminance
size = len(luminance)

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
for i in range(0, len(luminance)):
    axisx.append(luminance[i][0])
    axisy.append(luminance[i][1])
# mang xnew [0, X, do chia nho nhat la 1]
xnew = np.linspace(axisx[0], axisx[X - 2], X - 1, endpoint=True)
power_smooth = spline(axisx, axisy, xnew)

# tinh dao ham
y_new = []
y_new.append(0)
for j in range(1, size - 1):
    y_new.append((axisy[j+1]-axisy[j-1])/4)
y_new.append(0)
plt.plot(xnew, axisy, color='red'),
plt.plot(xnew, smooth(axisy, 13), 'g-', lw=2)
plt.axis([0, 181, 0, 250])
plt.xlabel('Bandwidth Heigh (Image Heigh)')
plt.ylabel('Intensity Value')
#
# print y_new
plt.plot(xnew, y_new, color='blue')
plt.axis([0,360, -1 , 1])
plt.show()

cv2.waitKey(0)