#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 08:52:09 2020

@author: eleden
"""

import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio as rio
import rasterio
from rasterio.transform import from_origin
import os
import fnmatch


for file_name in fnmatch.filter(os.listdir("./no2"),'*.he5'):
  
  date = file_name.split('_')[2].replace('m','')
  f = h5py.File("./no2/"+file_name, "r")
  data =  f['HDFEOS']['GRIDS']['ColumnAmountNO2']['Data Fields']
  ColumnAmountNO2 = data['ColumnAmountNO2'][()]
  ColumnAmountNO2CloudScreened =  data['ColumnAmountNO2CloudScreened'][()]
  ColumnAmountNO2Trop =  data['ColumnAmountNO2Trop'][()]
  ColumnAmountNO2TropCloudScreened =  data['ColumnAmountNO2TropCloudScreened'][()]
  Weight =  data['Weight'][()]
  Struct_metadata = f["HDFEOS INFORMATION"]["StructMetadata.0"][()].decode('UTF-8')
  f.close()
  arr = ColumnAmountNO2
  path = f'./no2_tif/no2_{date}.tif'
  transform = from_origin(-180, 90, 0.25, 0.25)
  new_dataset = rasterio.open(path, 'w', driver='GTiff',
                              height = arr.shape[0], width = arr.shape[1],
                              count=1, dtype=str(arr.dtype),
  #                            crs='+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs',
                              transform=transform)
  
  new_dataset.write(arr, 1)
  new_dataset.close()

