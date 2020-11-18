import shapely
from shapely.geometry import Point

import DataReader as dr
import Helper
from Simplegui import SGUI

class Controller:

    def __init__(self):
        self.dict=self.setup()
        self.gui=SGUI(self)

    def parse_coords(self,lat,lon):
        print("parse")
        # dr.parse_coords(lat,lon)
        # if lat == 0:
        lat = 211552.031768453
        lon = 178035.86512654446
        # print(lat, lon)
        center_wgs=Helper.translate_coords(lat,lon,"31370","4326")[0]
        center=Point(lat,lon)
        print(type(center_wgs),center_wgs)
        for k,v in self.dict.items():
            if v.contains(center_wgs):
                dr.parse_coords(lat,lon,k)
                return

    def setup(self):
        prov_niscode_shapes = {}
        for record in dr.read_shp('/home/techpriest/Desktop/becode/SpaceEYE/ADM/Apn_AdPr.shp').to_records():
            prov_niscode_shapes[record[3]] = record[-1]
        return prov_niscode_shapes

