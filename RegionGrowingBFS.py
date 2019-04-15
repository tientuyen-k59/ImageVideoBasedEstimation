import cv2
import numpy as np

image = cv2.imread('fog_new.png', 0)
he, wi = image.shape[:2]
Y = wi
X = he
print("cao: " + str(he))
print("rong: " + str(wi))


class coor:
    x = 0
    y = 0


d1 = [-1, -1, -1]
d2 = [-1, 0, 1]


def BFS(root, m):
    q = [root]
    m[root.x][root.y] = 255
    while q:
        n = q.pop()
        for i in range(3):
            next = coor()
            next.x = n.x + d1[i]
            next.y = n.y + d2[i]
            x1 = next.x
            y1 = next.y
            if (x1 >= 0 and x1 <= (X - 1) and y1 >= 0 and y1 <= (Y - 1) and m[x1][y1] != 0 and m[x1][y1] != 255):
                m[x1][y1] = 255;
                q.insert(0, next)


def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Seed: ' + str(x) + ', ' + str(y) + '   Luminance: ', img[y, x]
        clicks.append((x, y))


clicks = []

image = cv2.resize(image, (Y, X))
heigh, width = image.shape[:2]

ret, img = cv2.threshold(image, 188, 255, cv2.THRESH_TRUNC)
edges = cv2.Canny(img, 20, 100)

cv2.imshow('edges', edges)

indices = np.where(edges == 255)
coordinates = zip(indices[0], indices[1])
print coordinates
# To den cac vung canh
for i in range(0, len(coordinates)):
    # print coordinates[i]
    y = coordinates[i][0]
    x = coordinates[i][1]
    # cho nhung diem canh thanh mau den
    # nhung diem tren diem canh cung chuyen thanh mau den de tao thanh duong lien
    img[coordinates[i]] = 0
    img[min(y + 1, heigh - 1), x] = 0
#     # img[min(y+1, Y/2-1), x] = 0


cv2.namedWindow('Input')
cv2.setMouseCallback('Input', on_mouse, 0, )
cv2.imshow('Input', img)

cv2.waitKey(5000)
seed = clicks[-1]
print seed


def region_growing(img, seed):
    m = img
    list = []

    # add [x last, y last]
    list.append((seed[0], seed[1]))

    # # Them cac pixel tu giua sang trai
    i = seed[0]
    while (img[seed[1], i] != 0):
        list.append((max(i - 1, 1), seed[1]))
        i = i - 1
        # print i
    # Them cac pixel tu giua sang phai
    j = seed[0]
    while (img[seed[1], j] != 0):
        list.append((max(j + 1, 1), seed[1]))
        j = j + 1

    # print max(y), max(x)
    print img.shape
    # get 3 zone above
    print len(list)

    # root = coor()
    # root.x = seed[0]
    # root.y = seed[1]
    # BFS(root, m)
    #
    # list.pop(0)
    # cv2.imshow("progress",m)
    # cv2.waitKey(1)
    while (len(list) > 0):
        pix = list[0]
        root = coor()
        root.x = pix[1]
        root.y = pix[0]
        BFS(root, m)

        list.pop(0)
        cv2.imshow("progress", m)
        cv2.waitKey(1)
    return m


out = region_growing(img, seed)
cv2.imwrite('output_file.png', out)

cv2.imshow('Output', out)
cv2.waitKey()
