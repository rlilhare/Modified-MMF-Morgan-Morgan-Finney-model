print"Importing Libraries"

import numpy 	 
from osgeo import osr
from osgeo import ogr  
import sys, os, glob 	 
from osgeo import gdal 	 
from gdalconst import *
import math

fn1 = r'G:\Test\Full_image\fdr.img'                    ##input flow direction file (FDR) ##"DO NOT CHANGE"
ds1 = gdal.Open(fn1, GA_ReadOnly)
if ds1 is None:
    print 'Could not open ' + fn1
    sys.exit(1)
col = ds1.RasterXSize
row = ds1.RasterYSize
driver=ds1.GetDriver()
fdr = ds1.ReadAsArray()

fn2 = r'G:\Test\Full_image\fac1.img'                    ##input flow accumulation file (FAC) ###"DO NOT CHANGE"
ds2 = gdal.Open(fn2, GA_ReadOnly)
if ds2 is None:
    print 'Could not open ' + fn2
    sys.exit(2)
fac = ds2.ReadAsArray()
maxf= fac.max()
print "Maximum value of fac map is " +str(maxf)

fn3 = r'G:\Endru\1998\Estimation of rainfall energy\rf1.img'                                                ##input Rf (effective rainfall map)
ds3 = gdal.Open(fn3, GA_ReadOnly)
if ds3 is None:
    print 'Could not open ' + fn3
    sys.exit(2)
rf = ds3.ReadAsArray()

fn4 = r'G:\Endru\1998\Estimation of runoff\rc.img'      ##input rc "DO NOT CHANGE"
ds4 = gdal.Open(fn4, GA_ReadOnly)
if ds4 is None:
    print 'Could not open ' + fn4
    sys.exit(2)
rc = ds4.ReadAsArray()

fn5 = r'G:\Endru\1998\Input Parameters\ro.img'                                                              ##input ro (refer the main paper to produce the ro map)
ds5 = gdal.Open(fn5, GA_ReadOnly)
if ds5 is None:
    print 'Could not open ' + fn5
    sys.exit(2)
ro = ds5.ReadAsArray()



fn6 = r'G:\Endru\1998\Input Parameters\rain_98.img'                                                         ##input Rainfall map
ds6 = gdal.Open(fn6, GA_ReadOnly)
if ds6 is None:
    print 'Could not open ' + fn6
    sys.exit(2)
R = ds6.ReadAsArray()


fn7 = r'G:\Endru\1998\Estimation of runoff\E.img'                                                           ##input E (refer the main paper to produce the ro map)
ds7 = gdal.Open(fn7, GA_ReadOnly)
if ds7 is None:
    print 'Could not open ' + fn7
    sys.exit(2)
E = ds7.ReadAsArray()


fn8 = r'G:\Endru\1998\Estimation of runoff\LP1.img'         ##input LP "DO NOT CHANGE" (refer the main paper to produce the ro map)
ds8 = gdal.Open(fn8, GA_ReadOnly)
if ds8 is None:
    print 'Could not open ' + fn8
    sys.exit(2)
LP = ds8.ReadAsArray()


fn9 = r'G:\Endru\1998\Estimation of runoff\sins.img'        ##input sins "DO NOT CHANGE" (refer the main paper to produce the ro map)
ds9 = gdal.Open(fn9, GA_ReadOnly)
if ds9 is None:
    print 'Could not open ' + fn9
    sys.exit(2)
sins = ds9.ReadAsArray()


Q=numpy.zeros((row,col),numpy.float)
Qe=numpy.zeros((row,col),numpy.float)
IF=numpy.zeros((row,col),numpy.float)

mx= 91088                                           ##input flow acc max value (users can calculate this value in any GIS software for their study area)
print "new maximum is " +str(mx)

l1 = sum(1 for line in open("G:\\Test\\fac_arr.txt")) ##input txt
arr= numpy.zeros(l1, numpy.int)

n=0
crs = open("G:\\Test\\fac_arr.txt", "r")            ##out txt
for columns in ( raw.strip().split() for raw in crs ):

    arr[n]=int(columns[0])
    n+=1

value=0

for v in range(len(arr)):
    for a in range(1,row-2):
        for b in range (1,col-2):
            
            if rf[a,b]>0.0 and rc[a,b]>=0.0 and ro[a,b]>=0.0:
                if fac[a,b]==arr[v] and arr[v]==0:
                    Qe[a,b]=rf[a,b]*(math.exp((-rc[a,b])/(ro[a,b])))
                    Q[a,b]=rf[a,b]*(math.exp(-rc[a,b]/ro[a,b]))
                    IF[a,b]=IF[a,b]+((((R[a,b])-(E[a,b])-(Qe[a,b]))*(LP[a,b])*(sins[a,b]))/365)
                    if IF[a,b]<0:
                        IF[a,b]=0.0
            
                elif fac[a,b]==arr[v] and arr[v]>0:
                    

                    if fdr[a,b-1]==1:
                        if rf[a,b-1]>0.0 and ro[a,b-1]>=0.0 and rc[a,b-1]>=0.0:
                            if IF[a,b-1]<0:
                                IF[a,b-1]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a,b-1]
                            IF[a,b]=IF[a,b]+ IF[a,b-1]

                    if fdr[a-1,b-1]==2:
                        if rf[a-1,b-1]>0.0 and ro[a-1,b-1]>=0.0 and rc[a-1,b-1]>=0.0:
                            if IF[a-1,b-1]<0:
                                IF[a-1,b-1]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a-1,b-1]
                            IF[a,b]=IF[a,b]+ IF[a-1,b-1]

                    if fdr[a-1,b]==4:
                        if rf[a-1,b]>0.0 and ro[a-1,b]>=0.0 and rc[a-1,b]>=0.0:
                            if IF[a-1,b]<0:
                                IF[a-1,b]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a-1,b]
                            IF[a,b]=IF[a,b]+ IF[a-1,b]

                    if fdr[a-1,b+1]==8:
                        if rf[a-1,b+1]>0.0 and ro[a-1,b+1]>=0.0 and rc[a-1,b+1]>=0.0 :
                            if IF[a-1,b+1]<0:
                                IF[a-1,b+1]=0.0
                                
                            Q[a,b]=Q[a,b]+Q[a-1,b+1]
                            IF[a,b]=IF[a,b]+ IF[a-1,b+1]

                    if fdr[a,b+1]==16:
                        if rf[a,b+1]>0.0 and ro[a,b+1]>=0.0 and rc[a,b+1]>=0.0:
                            if IF[a,b+1]<0:
                                IF[a,b+1]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a,b+1]
                            IF[a,b]=IF[a,b]+ IF[a,b+1]

                    if fdr[a+1,b+1]==32:
                        if rf[a+1,b+1]>0.0 and ro[a+1,b+1]>=0.0 and rc[a+1,b+1]>=0.0:
                            if IF[a+1,b+1]<0:
                                IF[a+1,b+1]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a+1,b+1]
                            IF[a,b]=IF[a,b]+ IF[a+1,b+1]

                    if fdr[a+1,b]==64:
                        if rf[a+1,b]>0.0 and ro[a+1,b]>=0.0 and rc[a+1,b]>=0.0:
                            if IF[a+1,b]<0:
                                IF[a+1,b]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a+1,b]
                            IF[a,b]=IF[a,b]+ IF[a+1,b]

                    if fdr[a+1,b-1]==128:
                        if rf[a+1,b-1]>0.0 and ro[a+1,b-1]>=0.0 and rc[a+1,b-1]>=0.0:
                            if IF[a+1,b-1]<0:
                                IF[a+1,b-1]=0.0
                                  
                            Q[a,b]=Q[a,b]+Q[a+1,b-1]
                            IF[a,b]=IF[a,b]+ IF[a+1,b-1]

                    rc[a,b]=rc[a,b]-IF[a,b]
                    if rc[a,b]<0.0:
                        rc[a,b]=0.0
                    
                    Qe[a,b]=rf[a,b]*(math.exp((-rc[a,b])/(ro[a,b])))
                    
                    Q[a,b]=((rf[a,b]+Q[a,b])*((math.exp((-rc[a,b])/(ro[a,b]))))*1.006)

                    IF[a,b]=((((R[a,b])-(E[a,b])-(Qe[a,b]))*(LP[a,b])*(sins[a,b]))/365) ###### check
                    if IF[a,b]<=0:
                        IF[a,b]=0.0
                    


    print str(arr[v])+ " FAC done"
    if arr[v]==mx:
        print "Maximum FAC attained"
        break    


                                      

outDs = driver.Create("G:\\Endru\\1998\\Estimation of runoff\\qtotal_ppt.img" , col, row, 1 , GDT_Float64)             ## SAVE OUTPUT IMAGE
if outDs is None:
        print 'Could not create new daily data image'
        sys.exit(1)
outBand = outDs.GetRasterBand(1)
outData = numpy.zeros((row,col), numpy.float)
 ##georeference the image and set the projection
outDs.SetGeoTransform(ds1.GetGeoTransform())
outDs.SetProjection(ds1.GetProjection())

outBand.WriteArray(Q, 0, 0)

 ##flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outDs.FlushCache()

outDs = None
del outData



outDs = driver.Create("G:\\Endru\\1998\\Estimation of runoff\\IF_ppt.img" , col, row, 1 , GDT_Float64)
if outDs is None:
        print 'Could not create new daily data image'
        sys.exit(1)
outBand = outDs.GetRasterBand(1)
outData = numpy.zeros((row,col), numpy.float)
 ##georeference the image and set the projection
outDs.SetGeoTransform(ds1.GetGeoTransform())
outDs.SetProjection(ds1.GetProjection())

outBand.WriteArray(IF, 0, 0)

 ##flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outDs.FlushCache()

outDs = None
del outData

outDs = driver.Create("G:\\Endru\\1998\\Estimation of runoff\\Qe_ppt.img" , col, row, 1 , GDT_Float64)
if outDs is None:
        print 'Could not create new daily data image'
        sys.exit(1)
outBand = outDs.GetRasterBand(1)
outData = numpy.zeros((row,col), numpy.float)
 ##georeference the image and set the projection
outDs.SetGeoTransform(ds1.GetGeoTransform())
outDs.SetProjection(ds1.GetProjection())

outBand.WriteArray(Qe, 0, 0)

 ##flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outDs.FlushCache()

outDs = None
del outData




