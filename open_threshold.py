import sys
import skimage
from skimage import data, feature, filters, color, img_as_float
from scipy import misc
from skimage.filters import threshold_yen
from skimage.filters import threshold_otsu
from matplotlib import pyplot as plt
from matplotlib import cm
from skimage.morphology import skeletonize
from skimage.feature import canny
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage import io
from skimage import img_as_uint
import glob
from PIL import Image
###########
##########INPUT AGUMENTS############
##DON'T FORGET TO UPDATE PATH
##INPUT IN THE COMMEND LINE s1 and s2 (i usually do 3 and 5 respectively)
path = "'/Users/alexandralong/Documents/UCSF/Dumont Lab/Analysis/Micromanipulation/Translation Fiji testing/old/Input1/*.tif'"

image_list = []
for filename in glob.glob('%s/testavg_*.tif'%path): #assuming gif
    image_list.append(filename)

#print image_list

for name in image_list:
    index = name.lstrip('%s/test'%path).rstrip('.tif')
    print index


####READ IMAGE, COMMAND LINE PROMPT####
    img = misc.imread(name)


###DIFFERENCE OF GAUSSIAN FILTER###
    s1 = filters.gaussian_filter(img,sys.argv[1])
    s2 = filters.gaussian_filter(img,sys.argv[2])

    dog = s1 - s2

###THRESHOLD YEN###
    global_thresh = threshold_otsu(dog)
    binary_global = dog > global_thresh

###SKELETON###
    skeleton = skeletonize(binary_global)

###HOUGH LINE TRANSFORM###
    lines = probabilistic_hough_line(skeleton, threshold=10, line_length=3,
                                     line_gap=10)


####PLOT TO SAVE HOUGH####
    plt.imshow(img, cmap=cm.gray)
    plt.axis('off')
    plt.savefig('%s/img_%s.png'%(path,index))

    plt.imshow(dog, cmap=cm.gray)
    plt.savefig('%s/DoG_%s.png'%(path,index))

    plt.imshow(binary_global, cmap=cm.gray)
    plt.savefig('%s/threshold_%s.png'%(path,index))

    plt.imshow(skeleton, cmap=cm.gray)
    plt.axis('off')
    plt.savefig('%s/skeleton_%s.png'%(path,index))

    plt.imshow(binary_global * 0)
    for line in lines:
        p0, p1 = line
        plt.plot((p0[0], p1[0]), (p0[1], p1[1]), 'y-')
    plt.xlim((0, img.shape[1]))
    plt.ylim((img.shape[0], 0))
    plt.axis('off')
    plt.savefig('%s/hough_%s.png'%(path,index))
    plt.close()

#lines=[]
#    for line in lines:
#        p0, p1 = line
#        print line
