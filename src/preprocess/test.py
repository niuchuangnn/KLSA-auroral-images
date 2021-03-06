import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets                              

img = cv2.imread('../../Data/labeled2003_38044/N20031221G072551.bmp')

sift = cv2.SIFT()
kp = sift.detect(img, None)

# img = cv2.drawKeypoints(img, kp)
img=cv2.drawKeypoints(img,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)                                                                                 

cv2.imwrite('sift_points.jpg', img)

iris = datasets.load_iris()
digits = datasets.load_digits()
a = np.array([1,2,3,4,5])
dd = digits.data[2,:]
plt.imshow(digits.images[0], cmap='gray')
plt.show()