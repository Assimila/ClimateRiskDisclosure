
import os
import sys
import gdal
from osgeo import gdal_array
import numpy as np

import datetime 

variable = sys.argv[1]

#fname = f'../ERA5/Europe/{variable}/Europe_monthly_mean_{variable}_1979_2019.tif'
fname = f'../ERA5/Europe/{variable}/Europe_monthly_mean_{variable}_2002_2019.tif'
d = gdal.Open(fname)
data = d.ReadAsArray()

# Get datadir
datadir = os.path.dirname(fname)

bands, rows, cols = data.shape

driver = gdal.GetDriverByName('GTiff')
driver_options = ["COMPRESS=DEFLATE",
                  "BIGTIFF=YES",
                  "PREDICTOR=1",
                  "TILED=YES",
                  "BLOCKXSIZE=256",
                  "BLOCKYSIZE=256",
                  "INTERLEAVE=BAND"]

# Get projection and geotransform
proj = d.GetProjection()
gt = d.GetGeoTransform()

# Get GDAL datatype from NumPy datatype
dtype = gdal_array.NumericTypeCodeToGDALTypeCode(data.dtype)
# Create dataset
fname = os.path.join(datadir, f'{variable}.tif')
dst_ds = driver.Create(fname, cols, rows, bands, dtype, driver_options)

# Set cartographic projection
dst_ds.SetProjection(proj)
dst_ds.SetGeoTransform(gt)

# Dates
#startyear = 1979                                                                                              
#startmonth = 1
startyear = 2002                                                                                              
startmonth = 7

endyear = 2019                                                                                               
endmonth = 12

dates = [datetime.date(m//12, m%12+1, 1) for m in range(startyear*12+startmonth-1, endyear*12+endmonth)]

if not len(dates) == bands:
    raise "Inconsistent number of bands for date range"

for i in range(bands):
    dst_ds.GetRasterBand(i+1).WriteArray(data[i])

    dst_band = dst_ds.GetRasterBand(i+1)
    dst_band.SetMetadataItem('RANGEBEGINNINGDATE', dates[i].strftime("%Y-%m-%d"))

dst_ds = None

