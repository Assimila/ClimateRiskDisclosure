
import os
import sys
import gdal
from osgeo import gdal_array
import numpy as np

import datetime 

variable = sys.argv[1]

fname1 = f'../ERA5/{variable}/US_REGIONS_monthly_mean_{variable}_1979_1999.tif'
d1 = gdal.Open(fname1)
data1 = d1.ReadAsArray()
print(data1.shape)

fname2 = f'../ERA5/{variable}/US_REGIONS_monthly_mean_{variable}_2000_2019.tif'
d2 = gdal.Open(fname2)
data2 = d2.ReadAsArray()
print(data2.shape)

# Get datadir
datadir = os.path.dirname(fname2)

full_array = np.concatenate((data1, data2), axis=0)
bands, rows, cols = full_array.shape

driver = gdal.GetDriverByName('GTiff')
driver_options = ["COMPRESS=DEFLATE",
                  "BIGTIFF=YES",
                  "PREDICTOR=1",
                  "TILED=YES",
                  "BLOCKXSIZE=256",
                  "BLOCKYSIZE=256",
                  "INTERLEAVE=BAND"]

# Get projection and geotransform
proj = d1.GetProjection()
gt = d1.GetGeoTransform()

# Get GDAL datatype from NumPy datatype
dtype = gdal_array.NumericTypeCodeToGDALTypeCode(full_array.dtype)
# Create dataset
fname = os.path.join(datadir, f'{variable}.tif')
dst_ds = driver.Create(fname, cols, rows, bands, dtype, driver_options)

# Set cartographic projection
dst_ds.SetProjection(proj)
dst_ds.SetGeoTransform(gt)

# Dates
startyear = 1979                                                                                              
startmonth = 1                                                                                                

endyear = 2019                                                                                               
endmonth = 8                                                                                                 

dates = [datetime.date(m//12, m%12+1, 1) for m in range(startyear*12+startmonth-1, endyear*12+endmonth)]

if not len(dates) == bands:
    raise "Inconsistent number of bands for date range"

for i in range(bands):
    dst_ds.GetRasterBand(i+1).WriteArray(full_array[i])

    dst_band = dst_ds.GetRasterBand(i+1)
    dst_band.SetMetadataItem('RANGEBEGINNINGDATE', dates[i].strftime("%Y-%m-%d"))

dst_ds = None

