import logging
import sys
import traceback

from dbfread import DBF
import shapefile
import geopandas as gpd
from shapely.geometry import Point, Polygon
import re
from rasterio.plot import show
import matplotlib
import time
import glob, os
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import rasterio
import rasterio.features
import rasterio.mask
import shapely
import Helper
from DatabaseHandler import DatabaseHandler

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

def find_containing_shp(lat,lon,folder):
    print("Looking for coordinates:",lat, lon)
    p=Helper.translate_coords(lon,lat,"4326","31370")[0]
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".shp"):
                file_path = os.path.join(root, file)
                # print(file_path)
                shp_file=coords_present_in_shp(file_path,p.x,p.y)
                if shp_file != None:
                    return shp_file
    raise Exception("Appropriate tiff-file has not been found!")

def coords_present_in_shp(file,x,y):
    be_stat = gpd.read_file(file, crs="EPSG:4326")
    be_stat.set_crs(epsg="31370",inplace=True)
    bounds=be_stat.total_bounds
    if bounds[0]<=x and bounds[2]>=x and bounds[1]<=y and bounds[3]>=y:
        print("Hit on",file)
        return file

def extract_corresponding_tiff(name):
    elements=name.split('/')
    pattern = '.*\/'
    result = re.match(pattern, name)[0]
    result=result+'GeoTIFF/'
    for root, dirs, files in os.walk(result):
        return result+files[0]

def read_shp(file):
    be_stat = gpd.read_file(file, crs="EPSG:31370")
    be_stat.set_crs(epsg="31370", inplace=True)
    be_stat.to_crs(epsg="4326", inplace=True)
    # print(be_stat.dtypes)
    # print(be_stat.columns)
    # print(be_stat.head(20))
    return be_stat

def analyse_tiff(tiff_file,lat,lon,shp):
    p=Helper.translate_coords(lon,lat,"4326","31370")[0]
    with rasterio.open(tiff_file) as dataset:
        print("opening ",tiff_file)
        location = dataset.index(p.x,p.y)
        try:
            array=dataset.read()
            out_mask, out_transform,out_win = rasterio.mask.raster_geometry_mask(dataset,shp,crop=True)
            perceel=array[0,out_win.row_off:out_win.row_off+out_win.height,out_win.col_off:out_win.col_off+out_win.width]
            # show(np.multiply(perceel,np.invert(out_mask)))
            print(out_win)
            surface_plot(np.multiply(perceel,np.invert(out_mask)),location)
        except Exception:
            logging.error(traceback.format_exc())


def surface_plot(array,location):
    # offset=100
    # array=array[:, location[0] - offset: location[0] + offset, location[1] - offset: location[1] + offset]
    print(array.shape)
    x_size=array.shape[0]
    y_size = array.shape[1]
    z=array[:,:]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(0,x_size,1)
    Y = np.arange(0,y_size,1)
    X, Y = np.meshgrid(X, Y)
    R = z[X,Y]
    Z = R
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0,)

    ax.set_zlim(np.amin(R)-len(X)/3, np.amax(R)+len(X)/3)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def parse_coords(lat,lon,db):
    conn = DatabaseHandler.get_connection()
    shape=(list(DatabaseHandler.get_records(conn,lat,lon,db)))[0]
    # shape = 'MULTIPOLYGON (((211576.394869812 178026.964925658, 211562.853621803 178012.17132565, 211527.982069783 178045.20825367, 211536.800245792 178055.76134168, 211537.869941786 178057.041469678, 211540.061621793 178059.66444568, 211540.091253787 178059.699901681, 211540.138741791 178059.65714968, 211540.305141792 178059.507133681, 211576.394869812 178026.964925658)))'
    p = shapely.wkt.loads(shape)
    conn.close()

    shp_file = find_containing_shp(lat, lon, "DSM")

    tiff_file = extract_corresponding_tiff(shp_file)
    analyse_tiff(tiff_file,lat,lon,p)