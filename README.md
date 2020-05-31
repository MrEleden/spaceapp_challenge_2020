# spaceapp_challenge_2020

# get Data

follow instruction to set up wget for Mac/Linux at : https://disc.gsfc.nasa.gov/data-access#mac_linux_wget
then execute :
```
cd ozone
wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -i subset_OMPS_NPP_NMTO3_L3_DAILY_2_20200531_062832.txt
cd ..

cd no2
wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -isubset_OMNO2d_003_20200531_020036.txt
cd ..

cd aerosol
wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -i subset_OMAEROe_003_20200531_062410.txt
```

# Data to tiff files
For each data type a script convert them to a tiff file
```
python3 converter_no2_tif.py
python3 converter_aerosol.py
python3 converter_ozone.py
```
# tiff files to data
Our script will mask a shapefile on the tiff files
this script create the training data used for Machine learning (dataset.csv)
```
python3 training_data.py
```
This script will aglomerate the data obtained from training such as features importances and previous data (data.csv)
It will be the main csv feeded to the website
```
python3 tif_to_csv.py
```

