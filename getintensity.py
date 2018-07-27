from pyemd import emd
import numpy as np
from PIL import Image
import skimage.color

im = Image.open("t4.jpg")
pix = im.load()

h1 = [1.0/64] * 64
h2 = [0.0] * 64
hist1 = np.array(h1)

w,h = im.size

for x in xrange(w):
    for y in xrange(h):
        cbin = pix[x,y][0]/64*16 + pix[x,y][1]/64*4 + pix[x,y][2]/64
        h2[cbin]+=1
hist2 = np.array(h2)/w/h

# compute center of cubes
c = np.zeros((64,3))
for i in xrange(64):
    b = (i%4) * 64 + 32
    g = (i%16/4) * 64 + 32
    r = (i/16) * 64 + 32
    c[i]=(r,g,b)

c_luv = skimage.color.rgb2luv(c.reshape(8,8,3)).reshape(64,3)

d = np.zeros((64,64))

for x in xrange(64):
    d[x,x]=0
    for y in xrange(x):
        dist = np.sqrt( np.square(c_luv[x,0]-c_luv[y,0]) +
                   np.square(c_luv[x,1]-c_luv[y,1]) +
                   np.square(c_luv[x,2]-c_luv[y,2]))
        d[x,y] = dist
        d[y,x] = dist


colorfullness = emd(hist1, hist2, d)

print colorfullness