import hashlib
import psycopg2
from shapely import wkb, wkt
import pygeohash as gh
from shapely.geometry import Point

class DatabaseHandler():

    def __init__(self,address):
        self.address=address

    @staticmethod
    def lambert_and_centroid(geom):
        obj = wkb.loads(geom,hex=True)
        return obj,obj.centroid

    @staticmethod
    def get_records(connection,lat,lon):
        cursor = connection.cursor()
        m = hashlib.md5()
        m.update(str.encode("{}{}".format(str(lat),str(lon))))
        md5=m.hexdigest()
        get_all_query = 'select * from public.percelen where {}=\'{}\';'.format('lambert_md5', md5)
        cursor.execute(get_all_query)
        rows = cursor.fetchall()
        print(len(rows),"records found")
        for i in rows:
            print(i)
            yield i[-4]
        cursor.close()

    @staticmethod
    def get_connection():
        try:
            connection = psycopg2.connect(user="techpriest",
                                          password="root",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="techpriest")
            print("Established Connection")
            return connection

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating connection", error)
