#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 15:56:42 2020

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


for file_name in fnmatch.filter(os.listdir("./ozone"),'*.h5'):
  
  date = file_name.split('_')[3].replace('m','')
  
  f = h5py.File("./ozone/"+file_name, "r")
  ColumnAmountO3 = f['ColumnAmountO3'][()]

  f.close()
  arr = ColumnAmountO3
  path = f'./ozone_tif/ozone_{date}.tif'
  transform = from_origin(-180, 90, 1.0, 1.0)
  new_dataset = rasterio.open(path, 'w', driver='GTiff',
                              height = arr.shape[0], width = arr.shape[1],
                              count=1, dtype=str(arr.dtype),
  #                            crs='+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs',
                              transform=transform)
  
  new_dataset.write(arr, 1)
  new_dataset.close()

