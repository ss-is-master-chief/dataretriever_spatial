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
        pass

    def create_database(self):
        try:
            os.system("spatialite db.sqlite '.databases'")
        except Error as e:
            print(e)


'''
    def to_csv(self):
        os.system("gdal_translate -b 1 -of XYZ tif_data.tif data.csv -co ADD_HEADER_LINE=YES")'''


if __name__=="__main__":

    obj = sqlite_engine()
    obj.create_database()
    os.system("clear")

    try:
        df = gdal.Open("tif_data.tif")

    except RuntimeError, e:
        print("Unable to open raster file")
        print(e)
        sys.exit(1)

    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    #cur.execute("CREATE TABLE t (col1, col2, col3);")

    with open('data.csv', 'rb') as fin:
        #reader = csv.reader(fin)
        #i = next(reader)
        #print(i)
        #dr = csv.DictReader(fin)
        #to_db = [(i['col1'], i['col2'], i['col3']) for i in dr]

#cur.executemany("INSERT INTO t (col1, col2, col3) VALUES (?, ?, ?);", to_db)
#con.commit()
conn.close()

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
