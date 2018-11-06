import os


labels = os.listdir('label')
images = os.listdir('train')


count = 0
for image in images:
    image_name = 'train/' + str(count) + '.png'
    label_name = 'label/' + str(count) + '.png'

    label = 'label_' + image



    if label in labels:
        os.rename('train/'+image, image_name)
        os.rename('label/'+label, label_name)
        if "label_"+image != label:
            print label
            print('\n')

        if image_name.split('/')[1] != label_name.split('/')[1]:
            print image_name
    else:
        print(image)

    count += 1


def add_label():
	for label in labels:
		os.rename('label/'+label, 'label/label_'+label)




