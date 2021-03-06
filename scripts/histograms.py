import sys
import scipy
from scipy import ndimage
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb

areaList = []
orientationList = []
N = int(sys.argv[1])

fig, (ax1, ax3,ax2) = plt.subplots(1, 3, figsize=(6, 6))

for i in range(1,N):
    fname = sys.argv[2] + '/' + str(i) + '_predict.png'
    image = scipy.misc.imread(fname)  # gray-scale image
    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(2))
    cleared = bw.copy()
    clear_border(cleared)

    label_image = label(bw)
    borders = np.logical_xor(bw, cleared)
    image_label_overlay = label2rgb(label_image, image=image)
    ax1.imshow(image_label_overlay)
    ax3.imshow(image)

    for region in regionprops(label_image):
        if region.area < 50:
            continue
        areaList.append(region.equivalent_diameter)
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                   fill=False, edgecolor='red', linewidth=2)
        ax1.add_patch(rect)
        props = region
        y0, x0 = props.centroid
        orientation = props.orientation
        orientationList.append(orientation)
        x1 = x0 + math.cos(orientation) * 0.5 * props.major_axis_length
        y1 = y0 - math.sin(orientation) * 0.5 * props.major_axis_length
        x2 = x0 - math.sin(orientation) * 0.5 * props.minor_axis_length
        y2 = y0 - math.cos(orientation) * 0.5 * props.minor_axis_length

        ax1.plot((x0, x1), (y0, y1), '-r', linewidth=2.5)
        ax1.plot((x0, x2), (y0, y2), '-r', linewidth=2.5)
        ax1.plot(x0, y0, '.g', markersize=15)

        minr, minc, maxr, maxc = props.bbox
        bx = (minc, maxc, maxc, minc, minc)
        by = (minr, minr, maxr, maxr, minr)
        ax1.plot(bx, by, '-b', linewidth=2.5)

    plt.draw()

    bins = np.arange(0, 100, 10)  # fixed bin size
    ax2.hist(map(int, areaList), bins=bins, alpha=0.5)
    ax2.set_title(str(len(areaList)))
    #ax2.hist(map(float, orientationList),bins=np.arange(-2, 2, 0.8))
    plt.pause(0.001)
    ax1.clear()
    ax2.clear()
print orientationList
input("Press Enter to continue...")
sys.exit()