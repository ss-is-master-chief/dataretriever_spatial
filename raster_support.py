import os
import sys
import csv

'''Importing SQLite module'''

try:
    import sqlite3
    from sqlite3 import Error
    print("You are running SQLite version:", sqlite3.version)

except:
    sys.exit("ERROR: SQLite not installed... \
    \nDownload from here => https://www.sqlite.org/download.html")

'''Importing GDAL module'''

try:
    #sys.path.insert(0,"/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages")
    from osgeo import gdal, ogr
    print("You are running GDAL version:", gdal.__version__)
    gdal.UseExceptions()

except:
    sys.exit("ERROR: OSGeo not installed... \
    \nDownload from here => http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries")

class sqlite_engine:

    def __init__(self):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        self.create_database()
        self.open_dataset()
        self.get_metadata()
        self.get_raster_bands()
        self.to_csv()
        self.to_sqlite()
        conn.close()

    def create_database(self):
        try:
            os.system("spatialite db.sqlite '.databases'")
        except Error as e:
            print(e)

    def open_dataset(self):
        try:
            global df
            df = gdal.Open("tif_data.tif")

        except RuntimeError, e:
            print("Unable to open raster file")
            print(e)
            sys.exit(1)

    def get_metadata(self):
        return df.GetMetadata()

    def get_raster_bands(self):
        return df.RasterCount

    #def close_connection(self):
        #conn.close()

    def to_csv(self):
        os.system("gdal_translate -b 1 -of XYZ tif_data.tif Raster.csv -co ADD_HEADER_LINE=YES")

    def to_sqlite(self):
        os.system("ogr2ogr -update -append -f SQLite db.sqlite -nln b1 Raster.csv -dsco METADATA=NO -dsco INIT_WITH_EPSG=NO")
        os.system("rm Raster.csv")

if __name__=="__main__":

    obj = sqlite_engine()
    #obj.create_database()
    #os.system("clear")




    #cur.execute("CREATE TABLE t (col1, col2, col3);")

    #with open('data.csv', 'rb') as fin:
        #reader = csv.reader(fin)
        #i = next(reader)
        #print(i)
        #dr = csv.DictReader(fin)
        #to_db = [(i['col1'], i['col2'], i['col3']) for i in dr]

        #cur.executemany("INSERT INTO t (col1, col2, col3) VALUES (?, ?, ?);", to_db)
        #con.commit()

    #print(x.GetMetadata())

    #print(x.RasterCount)

    #srcband = x.GetRasterBand(1)
    #stats = srcband.GetStatistics(True, True)
    #print(srcband)
    #print(stats)

    #print "[ NO DATA VALUE ] = ", srcband.GetNoDataValue()
    #print "[ MIN ] = ", srcband.GetMinimum()
    #print "[ MAX ] = ", srcband.GetMaximum()
    #print "[ SCALE ] = ", srcband.GetScale()
    #print "[ UNIT TYPE ] = ", srcband.GetUnitType()
    #ctable = srcband.GetColorTable()
