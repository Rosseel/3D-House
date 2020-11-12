# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import glob, os
import zipfile

import rasterio
import rasterio.features
from rasterio._warp import Resampling
from rasterio.warp import reproject
from dbfread import DBF
import shapefile
import geopandas as gpd
from shapely.geometry import Point, Polygon
import re
from rasterio.plot import show
import matplotlib

matplotlib.use('Qt5Agg')

def process_tiff(file):
    ds=rasterio.open(file)
    print(ds.crs)
    print(ds.bounds)

def process_dbf(file):
    for record in DBF(file):
        print(record)

def read_tiff():
    for root, dirs, files in os.walk("DSM"):
        for file in files:
            if file.endswith(".tif"):
                file_path=os.path.join(root, file)
                process_tiff(file_path)

def read_dbf():
    for root, dirs, files in os.walk("DSM"):
        for file in files:
            if file.endswith(".dbf"):
                file_path = os.path.join(root, file)
                process_dbf(file_path)

def find_containing_shp(x,y,folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".shp"):
                file_path = os.path.join(root, file)
                # print(file_path)
                shp_file=coords_present_in_shp(file_path,x,y)
                if shp_file != None:
                    return shp_file

def coords_present_in_shp(file,x,y):
    be_stat = gpd.read_file(file, crs="EPSG:31370")
    be_stat.set_crs(epsg="31370",inplace=True)
    be_stat.to_crs(epsg="4326", inplace=True)
    bounds=be_stat.total_bounds
    if bounds[0]<=x and bounds[2]>=x and bounds[1]<=y and bounds[3]>=y:
        return file
    else:
        print("No hit on ",file)

def extract_corresponding_tiff(name):
    elements=name.split('/')
    pattern = '.*\/'
    result = re.match(pattern, name)[0]
    result=result+'GeoTIFF/'
    for root, dirs, files in os.walk(result):
        return result+files[0]

def translate_coords(coords_x,coords_y,crs_input,crs_output):
    location=gpd.GeoSeries([Point(x,y)])
    location.set_crs(epsg=crs_input,inplace=True)
    return location.to_crs(epsg=crs_output)

def read_shp(file):
    be_stat = gpd.read_file(file, crs="EPSG:31370")
    be_stat.set_crs(epsg="31370", inplace=True)
    be_stat.to_crs(epsg="4326", inplace=True)

    # gpd.('display.max_columns', 500)
    # gpd.set_option('display.width', 1000)
    print(be_stat.dtypes)
    print(be_stat.columns)

if __name__ == '__main__':
    x = 3.237619
    y = 51.207930
    # print(find_containing_shp(x, y,"DSM"))
    # print(find_containing_shp(x, y,"ADM"))
    # tiff_file=extract_corresponding_tiff('DSM/DHMVIIDSMRAS1m_k13/DHMVII_vdc_k13.shp')
    read_shp('ADM/Adp_20201108_04000_Shapefile/Shapefile/Adp04000.shp')

    # brugge_crs_31370=translate_coords(x,y,"4326","31370")
    #
    # with rasterio.open(tiff_file) as dataset:
    #     print("opening ",tiff_file)
    #     location= dataset.index(brugge_crs_31370.x,brugge_crs_31370.y)
    #     location_x=location[0][0]
    #     location_y = location[1][0]
    #     print(location_x,location_y)
    #     # print(dataset.count)
    #     # print(dataset.crs)
    #     # Read the dataset's valid data mask as a ndarray.
    #     # mask = dataset.dataset_mask()
    #     print(dataset.meta)
    #     print(dataset.bounds)
    #     print(dataset.indexes)
    #     array=dataset.read()
    #     # print(type(location_x),location_x)
    #     print(array.shape)
    #     offset=100
    #     show(array[:,location_x-offset:location_x+offset,location_y-offset:location_y+offset])
    #     # print(type(array))
    #     # print(array)
        # while array != None:
        #     array = dataset.read()
        #     print(type(array))



