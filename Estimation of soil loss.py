print"Importing Libraries"

import numpy 	 
from osgeo import osr
from osgeo import ogr  
import sys, os, glob 	 
from osgeo import gdal 	 
from gdalconst import *



fn1 = r'G:\Test\Full_image\fdr.img'                    ##input flow direction file (FDR) DO NOT CHANGE
ds1 = gdal.Open(fn1, GA_ReadOnly)
if ds1 is None:
    print 'Could not open ' + fn1
    sys.exit(1)
col = ds1.RasterXSize
row = ds1.RasterYSize
driver=ds1.GetDriver()
fdr = ds1.ReadAsArray()

fn2 = r'G:\Test\Full_image\fac1.img'                    ##input FAC DO NOT CHANGE
ds2 = gdal.Open(fn2, GA_ReadOnly)
if ds2 is None:
    print 'Could not open ' + fn2
    sys.exit(2)
fac = ds2.ReadAsArray()
maxf= fac.max()
print "Maximum value of fac map is " +str(maxf)

fn3 = r'G:\Endru\1999\Delivery of detached particles to runoff\g_s.img'                                         ##input G
ds3 = gdal.Open(fn3, GA_ReadOnly)
if ds3 is None:
    print 'Could not open ' + fn3
    sys.exit(2)
SLnew = ds3.ReadAsArray()
SL1new= ds3.ReadAsArray()

fn4 = r'G:\Endru\1996\deposition_factor\dep_s.img' ##input DEP DO NOT CHANGE path, change img only
ds4 = gdal.Open(fn4, GA_ReadOnly)
if ds4 is None:
    print 'Could not open ' + fn4
    sys.exit(2)
DEP = ds4.ReadAsArray()

fn5 = r'G:\Endru\1999\Transport capacity\tc_s.img'                                                              ##input TC
ds5 = gdal.Open(fn5, GA_ReadOnly)
if ds5 is None:
    print 'Could not open ' + fn5
    sys.exit(2)
TCnew = ds5.ReadAsArray()


TC=numpy.zeros((row,col),numpy.float64)
SL=numpy.zeros((row,col),numpy.float64)
SL1=numpy.zeros((row,col),numpy.float64)

for a in range(row):
    for b in range (col):
        SL[a,b]=numpy.float64(SLnew[a,b])
        SL1[a,b]=numpy.float64(SL1new[a,b])
        TC[a,b]=numpy.float64(TCnew[a,b])

mx= 91088                                           ##input flow acc max value
print "new maximum is " +str(mx)

l1 = sum(1 for line in open("G:\\Test\\fac_arr.txt")) ##input txt
arr= numpy.zeros(l1, numpy.int)

n=0
crs = open("G:\\Test\\fac_arr.txt", "r")            ##out txt
for columns in ( raw.strip().split() for raw in crs ):

    arr[n]=int(columns[0])
    n+=1


for v in range(len(arr)):
    for a in range(1,row-2):                                                    #############define row/cols for entire image
        for b in range(1,col-2):

            if fac[a,b]==arr[v] and arr[v]>0.0 and SL[a,b]>=0.0 and DEP[a,b]>=0.0:
            
                if fdr[a,b-1]==1 and DEP[a,b-1]>=0.0 and SL[a,b-1]>=0.0:
                    if TC[a,b-1] >= SL[a,b-1]:
                        SL[a,b]=SL[a,b]+SL[a,b-1]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a,b-1]*DEP[a,b-1])

                if fdr[a-1,b-1]==2 and DEP[a-1,b-1]>=0.0 and SL[a-1,b-1]>=0.0:
                    if TC[a-1,b-1] >= SL[a-1,b-1]:
                        SL[a,b]=SL[a,b]+SL[a-1,b-1]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a-1,b-1]*DEP[a-1,b-1])

                if fdr[a-1,b]==4 and DEP[a-1,b]>=0.0 and SL[a-1,b]>=0.0:
                    if TC[a-1,b] >= SL[a-1,b]:
                        SL[a,b]=SL[a,b]+SL[a-1,b]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a-1,b]*DEP[a-1,b])

                if fdr[a-1,b+1]==8 and DEP[a-1,b+1]>=0.0 and SL[a-1,b+1]>=0.0:
                    if TC[a-1,b+1] >= SL[a-1,b+1]:
                        SL[a,b]=SL[a,b]+SL[a-1,b+1]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a-1,b+1]*DEP[a-1,b+1])

                if fdr[a,b+1]==16 and DEP[a,b+1]>=0.0 and SL[a,b+1]>=0.0:
                    if TC[a,b+1] >= SL[a,b+1]:
                        SL[a,b]=SL[a,b]+SL[a,b+1]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a,b+1]*DEP[a,b+1])

                if fdr[a+1,b+1]==32 and DEP[a+1,b+1]>=0.0 and SL[a+1,b+1]>=0.0:
                    if TC[a+1,b+1] >= SL[a+1,b+1]:
                        SL[a,b]=SL[a,b]+SL[a+1,b+1]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a+1,b+1]*DEP[a+1,b+1])

                if fdr[a+1,b]==64 and DEP[a+1,b]>=0.0 and SL[a+1,b]>=0.0:
                    if TC[a+1,b] >= SL[a+1,b]:
                        SL[a,b]=SL[a,b]+SL[a+1,b]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a+1,b]*DEP[a+1,b])

                if fdr[a+1,b-1]==128 and DEP[a+1,b-1]>=0.0 and SL[a+1,b-1]>=0.0:
                    if TC[a+1,b-1] >= SL[a+1,b-1]:
                        SL[a,b]=SL[a,b]+SL[a+1,b-1]
                    else:
                        SL[a,b]=SL[a,b]+(SL[a+1,b-1]*DEP[a+1,b-1])

                    
    print str(arr[v])+ " FAC done"
    if arr[v]==mx:
        print "Maximum FAC attained"
        break




outDs = driver.Create("G:\\Endru\\1999\\Soil loss\\sl_s.img" , col, row, 1 , GDT_Float64)               ##save output image
if outDs is None:
        print 'Could not create new soil loss map'
        sys.exit(1)
outBand = outDs.GetRasterBand(1)
outData = numpy.zeros((row,col), numpy.float64)
 ##georeference the image and set the projection
outDs.SetGeoTransform(ds1.GetGeoTransform())
outDs.SetProjection(ds1.GetProjection())

outBand.WriteArray(SL, 0, 0)

 ##flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outDs.FlushCache()

outDs = None
del outData
print "Ho gya"
