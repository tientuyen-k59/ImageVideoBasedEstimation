import cv2
import numpy as np

# img = cv2.imread('testFog.png', 0)
# img = cv2.Canny(img, 10, 100)
# cv2.imshow('Canny', img)
# cv2.waitKey(0)

def get3n(x, y, shape):
    out = []
    maxx = shape[1]-1
    maxy = shape[0]-1

    #top left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    #top center
    outx = min(max(x-1,0),maxx)
    outy = y
    out.append((outx,outy))
    # top right
    outx = min(max(x-1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    return out

def region_growing(img, seed):
    out_img = img
    list = []
    # add [y last, x last]
    list.append((seed[0], seed[1]))
    processed = []
    print img.shape
    print get3n(seed[0], seed[1], img.shape)
    while (len(list)>0):
        pix=list[0]
        out_img[pix[0],pix[1]]=255
        for coord in get3n(pix[0], pix[1], img.shape):
            if (img[coord[0], coord[1]] != 0):
                out_img[coord[0], coord[1]] = 255
                if not coord in processed:
                    list.append(coord)
                processed.append(coord)
        # pop index 0 in list
        list.pop(0)
        cv2.imshow("progress",out_img)
        cv2.waitKey(1)
    return out_img

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Seed: ' + str(x) + ', ' + str(y) + '   Luminance: ' ,img[y,x]
        clicks.append((y,x))
clicks = []

image = cv2.imread('testFog.png', 0)
heigh, width = image.shape[:2]
ret, img = cv2.threshold(image, 188, 255, cv2.THRESH_TRUNC)
# cv2.imshow('img', img)
Ls = img[heigh-1, width/2]
print Ls
i = heigh-1
j = width/2
k = width/2

cv2.namedWindow('Input')
cv2.setMouseCallback('Input', on_mouse, 0,)
cv2.imshow('Input', img)

cv2.waitKey(5000)
seed = clicks[-1]
print seed
out = region_growing(img, seed)
print 'x'
cv2.imshow('Output', out)
cv2.waitKey()

