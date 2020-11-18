import os
import zipfile
import geopandas as gpd
from shapely.geometry import Point

def unzip():
    for folder, dirs, files in os.walk("/home/techpriest/Desktop/becode/SpaceEYE/DSM", topdown=False):
        for name in files:
            print(name)
            if name.endswith(".zip"):
                # print(os.path.join(folder, name))
                # unzip to folder and delete the zip file
                os.chdir(folder)
                print("folder",folder)
                print("name",name)
                zip_file = zipfile.ZipFile(os.path.join(folder, name))
                zip_file.extractall()
                zip_file.close()
                os.remove(os.path.join(folder, name))

def translate_coords(coords_x,coords_y,crs_input,crs_output):
    location=gpd.GeoSeries([Point(coords_x,coords_y)])
    location.set_crs(epsg=crs_input,inplace=True)
    return location.to_crs(epsg=crs_output)
