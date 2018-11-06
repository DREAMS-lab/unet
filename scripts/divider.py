import cv2
img = cv2.imread('DJI_0122.JPG')
d = 912*2
i = img.shape[0]/d
j = img.shape[1]/d

for x in range(i):
	for y in range(j):
		cv2.imwrite(str(x)+'_'+str(y)+'.jpg',img[x*d:x*d+d, y*d:y*d+d, :])
