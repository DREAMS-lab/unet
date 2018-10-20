import sys
import scipy
from scipy import ndimage
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb

areaList = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 6))
print sys.argv[1]

for filepath in glob.iglob(sys.argv[1] + '/*predict*.png'):
    fname = filepath
    print fname
    image = scipy.misc.imread(fname)  # gray-scale image
    # threshold = 1
    #
    # # find connected components
    # labeled, nr_objects = ndimage.label(img > threshold)

    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(3))

    # remove artifacts connected to image border
    cleared = bw.copy()
    clear_border(cleared)

    # label image regions
    label_image = label(cleared)
    borders = np.logical_xor(bw, cleared)
    label_image[borders] = -1
    image_label_overlay = label2rgb(label_image, image=image)
    ax1.imshow(label_image)

    for region in regionprops(label_image):
        if region.area < 1:
            continue
        areaList.append(region.area)
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                   fill=False, edgecolor='red', linewidth=2)
        ax1.add_patch(rect)
    plt.draw()
    #
    # bins = np.arange(0, 4000, 500)  # fixed bin size
    # plt.hist(map(int, areaList), bins=bins, alpha=0.5)
    # plt.draw()
    bins = np.arange(0, 6000, 400)  # fixed bin size
    ax2.hist(map(int, areaList), bins=bins, alpha=0.5)
    plt.pause(0.001)
    ax1.clear()
    ax2.clear()

input("Press Enter to continue...")
sys.exit()