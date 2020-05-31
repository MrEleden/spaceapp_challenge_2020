#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 15:09:13 2020

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


for file_name in fnmatch.filter(os.listdir("./aerosol"),'*.he5'):
  
  date = file_name.split('_')[2].replace('m','').split('t')[0]

  f = h5py.File("./aerosol/"+file_name, "r")
  data =  f['HDFEOS']['GRIDS']['ColumnAmountAerosol']['Data Fields']

  
  AerosolOpticalThicknessMW = data['AerosolOpticalThicknessMW'][()]
  AerosolOpticalThicknessMW = AerosolOpticalThicknessMW.mean(axis=0)
  f.close()

  arr = AerosolOpticalThicknessMW
  path = f'./aerosol_tif/aerosol_{date}.tif'
  transform = from_origin(-180, 90, 0.25, 0.25)
  new_dataset = rasterio.open(path, 'w', driver='GTiff',
                              height = arr.shape[0], width = arr.shape[1],
                              count=1, dtype=str(arr.dtype),
  #                            crs='+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs',
                              transform=transform)
  
  new_dataset.write(arr, 1)
  new_dataset.close()
