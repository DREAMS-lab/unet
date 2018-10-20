import os
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('.')]

count = 0
for file in onlyfiles:
	if 'mask'+file.split('image')[-1] in onlyfiles:
		count += 1
	elif file.startswith('image'):
		print(file)
print(count)
