import os
import sys
import gdal
from osgeo import gdal_array
import numpy as np
import numpy.ma as ma

import datetime

variable = 'u_component_of_wind_10m'
fname = f'../ERA5/{variable}/{variable}.tif'
d = gdal.Open(fname)
u = d.ReadAsArray()
u = ma.masked_invalid(u)
u = np.where(u > 11.4, 1.0, u)
u = np.where(u < -11.4, -1.0, u)

variable = 'v_component_of_wind_10m'
fname = f'../ERA5/{variable}/{variable}.tif'
d = gdal.Open(fname)
v = d.ReadAsArray()
v = ma.masked_invalid(v)

# There is something wrong on band 367, replace it
# with previous one
v[366] = v[365]

v = np.where(v > 10.1, 1.0, v)
v = np.where(v < -10.1, -1.0, v)

mask = ma.getmaskarray(v)

# Wind speed is sqrt( u^2 + v^2 )
ws = np.sqrt(np.power(u, 2) + np.power(v, 2))

# Wind power is defined as: (1/2)ρw^3, where
#     w is the daily mean wind speed
#     ρ is the air density (taken to be constant at 1.23 kg/m3).

ro = 1.23
wp = np.divide(ro * np.power(ws, 3), 2.0)
# Apply mask
wp[mask] = np.nan

# Save data
bands, rows, cols = wp.shape

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
dtype = gdal_array.NumericTypeCodeToGDALTypeCode(wp.dtype)
# Create dataset
datadir = '/home/glopez/Projects/ClimateRiskDisclosure/ERA5/wind_power'
fname = os.path.join(datadir, f'wind_power.tif')
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
    dst_ds.GetRasterBand(i+1).WriteArray(wp[i])

    dst_band = dst_ds.GetRasterBand(i+1)
    dst_band.SetMetadataItem('RANGEBEGINNINGDATE', dates[i].strftime("%Y-%m-%d"))

dst_ds = None

# Get stats

wp_mean = np.mean(wp, axis=0)
wp_std = np.std(wp, axis=0)

# Save data
rows, cols = wp_mean.shape
# Get GDAL datatype from NumPy datatype
dtype = gdal_array.NumericTypeCodeToGDALTypeCode(wp.dtype)
# Create dataset
datadir = '/home/glopez/Projects/ClimateRiskDisclosure/ERA5/wind_power'
fname = os.path.join(datadir, f'mean_wind_power.tif')
dst_ds = driver.Create(fname, cols, rows, 1, dtype, driver_options)
# Set cartographic projection
dst_ds.SetProjection(proj)
dst_ds.SetGeoTransform(gt)

dst_ds.GetRasterBand(1).WriteArray(wp_mean)
dst_ds = None

rows, cols = wp_std.shape
# Get GDAL datatype from NumPy datatype
dtype = gdal_array.NumericTypeCodeToGDALTypeCode(wp_std.dtype)
# Create dataset
datadir = '/home/glopez/Projects/ClimateRiskDisclosure/ERA5/wind_power'
fname = os.path.join(datadir, f'std_wind_power.tif')
dst_ds = driver.Create(fname, cols, rows, 1, dtype, driver_options)
# Set cartographic projection
dst_ds.SetProjection(proj)
dst_ds.SetGeoTransform(gt)

dst_ds.GetRasterBand(1).WriteArray(wp_std)
dst_ds = None



