import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.misc
import os

blue = (255, 50, 50) # BGR
red = (20, 20, 120)

def apply_mask(image, mask, color, alpha=0.3):
    """Apply the given mask to the image. Note the intensity should range in [0,255]
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 255,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c],
                                  image[:, :, c])
    return image

if __name__=='__main__':
    files = os.listdir('.')
    files.remove('visualize.py')
    for file in files:
        if 'predict' not in file:
            if 'mask' not in file:
                img = cv2.imread(file)
                prd_file = file.split('.')[0]+"_predict.png"
                mask = cv2.imread(prd_file)
                mask = cv2.resize(mask, dsize=(400, 400), interpolation=cv2.INTER_LINEAR)[:,:,0]
                mask = (mask>60)*255

                img_ = apply_mask(img, mask, red)
                cv2.imwrite(file.split('.')[0]+"_mask.png", img_)
