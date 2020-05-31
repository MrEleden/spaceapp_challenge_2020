#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:06:55 2020

@author: eleden
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 13:46:19 2020

@author: eleden
"""
import os
import fnmatch
import geopandas as gpd
import pandas as pd
import rasterio
from shapely.geometry import mapping
from rasterio.mask import mask
import numpy as np
from sklearn import preprocessing


shapefile_paths = "./Shapefiles/North coast states/North-coast-states.shp"
shapefile = gpd.read_file(shapefile_paths)

col1 = ['AOI', 'Date']
col2 = ['no2Mean', 'no2Std', 'no2Min', 'no2Max', 'no2Median']
col3 = ['ozoneMean', 'ozoneStd', 'ozoneMin', 'ozoneMax', 'ozoneMedian']
col4 = ['aerosolMean', 'aerosolStd', 'aerosolMin', 'aerosolMax', 'aerosolMedian']
col5 = ['Gt']

col = col1 + col2 + col3 + col4 + col5

data = pd.DataFrame(columns=col)


df_covid = pd.read_csv("covid19-cases-us-states-east.csv")
df_covid.date = df_covid.date.astype(str)
for no2_tif_file in os.listdir("./no2_tif/"):
  date = no2_tif_file.split('_')[1][:-4]
  with rasterio.open(f'./no2_tif/{no2_tif_file}') as src:
    for i in range(len(shapefile)):
      geometry = shapefile.iloc[i]['geometry']
      Name = shapefile.iloc[i]['STATE_NAME']
    # transform to GeJSON format
      geoms = [mapping(geometry)]
    # extract the raster values values within the polygon
      out_image, out_transform = mask(src, geoms, crop=True, nodata=np.nan)
      out_meta = src.meta
      mean = np.nanmean(out_image[0])
      min_val = np.nanmin(out_image[0])
      max_val = np.nanmax(out_image[0])
      median = np.nanmedian((out_image[0]))
      std = np.nanstd(out_image[0])
      gt = df_covid.loc[(df_covid.date == date)&(df_covid.state == Name)].positive
      if gt.empty:
        gt = 0
      else:
        gt = gt.values[0]
      val = [Name, date]
      val += [mean, std, min_val, max_val, median]
      val += [0,0,0,0,0]
      val += [0,0,0,0,0]
      val += [gt]
      data.loc[len(data)] = val



for ozone_tif_file in os.listdir("./ozone_tif/"):
  date = ozone_tif_file.split('_')[1][:-4]
  with rasterio.open(f'./ozone_tif/{ozone_tif_file}') as src:
    for i in range(len(shapefile)):
      geometry = shapefile.iloc[i]['geometry']
      Name = shapefile.iloc[i]['STATE_NAME']
    # transform to GeJSON format
      geoms = [mapping(geometry)]
    # extract the raster values values within the polygon
      out_image, out_transform = mask(src, geoms, crop=True, nodata=np.nan)
      out_meta = src.meta
      mean = np.nanmean(out_image[0])
      min_val = np.nanmin(out_image[0])
      max_val = np.nanmax(out_image[0])
      median = np.nanmedian((out_image[0]))
      std = np.nanstd(out_image[0])
      gt = df_covid.loc[(df_covid.date == date)&(df_covid.state == Name)].positive
      if gt.empty:
        gt = 0
      else:
        gt = gt.values[0]
      data.loc[(data.AOI == Name) & (data.Date == date), col3] = [mean, std, min_val, max_val, median]



for aerosol_tif_file in os.listdir("./aerosol_tif/"):
  date = aerosol_tif_file.split('_')[1][:-4]
  with rasterio.open(f'./aerosol_tif/{aerosol_tif_file}') as src:
    for i in range(len(shapefile)):
      geometry = shapefile.iloc[i]['geometry']
      Name = shapefile.iloc[i]['STATE_NAME']
    # transform to GeJSON format
      geoms = [mapping(geometry)]
    # extract the raster values values within the polygon
      out_image, out_transform = mask(src, geoms, crop=True, nodata=np.nan)
      out_meta = src.meta
      mean = np.nanmean(out_image[0])
      min_val = np.nanmin(out_image[0])
      max_val = np.nanmax(out_image[0])
      median = np.nanmedian((out_image[0]))
      std = np.nanstd(out_image[0])
      gt = df_covid.loc[(df_covid.date == date)&(df_covid.state == Name)].positive
      if gt.empty:
        gt = 0
      else:
        gt = gt.values[0]
      data.loc[(data.AOI == Name) & (data.Date == date), col4] = [mean, std, min_val, max_val, median]



data.to_csv("dataset.csv",index=False, sep=';')




