import os
from PIL import Image

files = os.listdir('.')

for f in files:
	if '.png' in f:
		img = Image.open(f)
		img = img.resize((384,384))
		img.save(f)
