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

col = ['AOI', 'Date', 'Type', 'Mean', 'Std', 'Min', 'Max', 'Median', 'Gt', 'Pred']
data = pd.DataFrame(columns=col)


df_covid = pd.read_csv("covid19-cases-us-states-east.csv")
df_covid.date = df_covid.date.astype(str)
df_covid.date = pd.to_datetime(df_covid.date,format='%Y%m%d')
df_covid = df_covid.sort_values('date')

for state in df_covid.state.unique().tolist():
  df_covid.loc[df_covid.state == state,'dayly'] = df_covid.loc[df_covid.state == state].positive.diff()

df_covid.date = df_covid.date.dt.strftime('%Y%m%d')

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
      gt = df_covid.loc[(df_covid.date == date)&(df_covid.state == Name)].dayly
      if gt.empty:
        gt = 0
      else:
        gt = gt.values[0]
      val = [Name, date, "no2", mean, std, min_val, max_val, median, gt, 0]
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
      gt = df_covid.loc[(df_covid.date == date)&(df_covid.state == Name)].dayly
      if gt.empty:
        gt = 0
      else:
        gt = gt.values[0]
      val = [Name, date, "ozone", mean, std, min_val, max_val, median, gt, 0]
      data.loc[len(data)] = val



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
      gt = df_covid.loc[(df_covid.date == date)&(df_covid.state == Name)].dayly
      if gt.empty:
        gt = 0
      else:
        gt = gt.values[0]
      val = [Name, date, "aerosol", mean, std, min_val, max_val, median ,gt, 0]
      data.loc[len(data)] = val

x = data.loc[data.Type == "no2"].Mean
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "no2","Mean"] = df_norm

x = data.loc[data.Type == "ozone"].Mean
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "ozone","Mean"] = df_norm

x = data.loc[data.Type == "aerosol"].Mean
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "aerosol","Mean"] = df_norm


x = data.loc[data.Type == "no2"].Std
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "no2","Std"] = df_norm

x = data.loc[data.Type == "ozone"].Std
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "ozone","Std"] = df_norm

x = data.loc[data.Type == "aerosol"].Std
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "aerosol","Std"] = df_norm




x = data.loc[data.Type == "no2"].Min
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "no2","Min"] = df_norm

x = data.loc[data.Type == "ozone"].Min
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "ozone","Min"] = df_norm

x = data.loc[data.Type == "aerosol"].Min
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "aerosol","Min"] = df_norm




x = data.loc[data.Type == "no2"].Max
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "no2","Max"] = df_norm

x = data.loc[data.Type == "ozone"].Max
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "ozone","Max"] = df_norm

x = data.loc[data.Type == "aerosol"].Max
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "aerosol","Max"] = df_norm




x = data.loc[data.Type == "no2"].Median
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "no2","Median"] = df_norm

x = data.loc[data.Type == "ozone"].Median
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "ozone","Median"] = df_norm

x = data.loc[data.Type == "aerosol"].Median
df_norm = (x - x.mean()) / (x.max() - x.min())
data.loc[data.Type == "aerosol","Median"] = df_norm

new_col = ['feat1','feat2','feat3','feat4','feat5']
for col_name in new_col:
  data[col_name] =""

df_pred = pd.read_csv('pred.csv',sep=';')


for aoi in df_pred.AOI.unique().tolist():
  for date in df_pred.loc[df_pred.AOI == aoi].date.unique().tolist():
    pred = df_pred.loc[(df_pred.AOI == aoi) & (df_pred.date == date)].pred.values[0]
    data.loc[(data.AOI == aoi) & (data.Date == date),'pred'] = pred



data.to_csv("data.csv",index=False, sep=';')



