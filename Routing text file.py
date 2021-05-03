print"Importing Libraries"

import numpy 	 
from osgeo import osr
from osgeo import ogr  
import sys, os, glob 	 
from osgeo import gdal 	 
from gdalconst import *

fn1 = r'G:\Test\Full_image\fac.img'                    ##input flow direction (FDR)
ds1 = gdal.Open(fn1, GA_ReadOnly)
if ds1 is None:
    print 'Could not open ' + fn1
    sys.exit(1)
col = ds1.RasterXSize
row = ds1.RasterYSize
driver=ds1.GetDriver()
fac = ds1.ReadAsArray()
arr = numpy.zeros((row*col),numpy.float64)

i=0
for a in range(row):
    for b in range (col):
        arr[i]=fac[a,b]
        i+=1
print "arry done"

text = open("G:\\Thesis\\fac_arr.txt", "w")
with open('G:\\Thesis\\fac_arr.txt', 'w') as f:
    for f1 in arr:
        print >> f,str(f1)        
text.close()
