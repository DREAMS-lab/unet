import os
from lxml import etree
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


class polygonReader(object):
    def __init__(self):
        self.data = self.__getData__()

    def __getData__(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        data = dict()
        for file in files:
            if ".xml" in file:
                f = open(file, 'r')
                doc = etree.parse(f)
                data[str(file)] = []  # [ [[2,3],[4,5]..] ,  [[2,3],[4,5]..]   ]
                for record in doc.xpath('/annotation/object'):
                    if record.xpath("deleted")[0].text == "0":
                        polygon = []
                        for pt in record.xpath("polygon/pt"):
                            polygon.append((int(pt.xpath("x")[0].text), int(pt.xpath("y")[0].text)))
                        data[file].append(tuple(polygon))
        return data

    def generateMask(self, (width, height)=(400, 400)):
        masks = dict()
        for obj, polygons in self.data.iteritems():
            img = Image.new('L', (width, height), 0)
            for poly in polygons:
                ImageDraw.Draw(img).polygon(poly, outline=1, fill=1)
            mask = np.array(img)
            masks[obj] = mask*255 # for visualization purpose
        return masks

    def saveMask(self, (width, height)=(400, 400)):
        masks = self.generateMask()
        for file, mask in masks.iteritems():
            plt.imsave(file.split('.')[0]+'.jpg', mask, cmap="gray")


if __name__ == "__main__":
    key = "1_2.xml"
    polygon = polygonReader()
    print(polygon.data[key])
    print(len(polygon.data[key]))
    masks = polygon.generateMask()
    polygon.saveMask()
