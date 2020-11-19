import numpy as np
import cv2
from mss import mss
from time import time

bounding_box = {'left': 350, 'top': 130, 'width': 1150, 'height': 760}
ratio = 2

sct = mss()

loop_time = time()
while True:
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    cv2.imshow('screen', sct_img)
 
    print('FPS {}'.format(1 /(time() - loop_time)))
    loop_time = time()

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break