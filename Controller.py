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
        center=Point(lon,lat)
        for k,v in self.dict.items():
            if v.contains(center):
                print("Need to look into db percelen_{}".format(k))
                dr.parse_coords(lat,lon,k)
                return
        raise Exception("Coordinates are invalid")

    def setup(self):
        prov_niscode_shapes = {}
        for record in dr.read_shp('/home/techpriest/Desktop/becode/SpaceEYE/ADM/Apn_AdPr.shp').to_records():
            prov_niscode_shapes[record[3]] = record[-1]
        return prov_niscode_shapes

