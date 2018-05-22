import os
import sys
import csv
import numpy as np
import glob

'''Importing SQLite module'''

try:
    import sqlite3
    from sqlite3 import Error
    #print("You are running SQLite version:", sqlite3.version)

except:
    sys.exit("ERROR: SQLite not installed... \
    \nDownload from here => https://www.sqlite.org/download.html")

'''Importing GDAL module'''

try:
    #sys.path.insert(0,"/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages")
    from osgeo import gdal, ogr
    #print("You are running GDAL version:", gdal.__version__)
    gdal.UseExceptions()

except:
    sys.exit("ERROR: OSGeo not installed... \
    \nDownload from here => http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries")


try:
    os.system("spatialite db.sqlite '.databases'")
except Error as e:
    print(e)

class engine:

    extensions = [".tif"]
    files = []
    file_name = []
    all_bands = []
    n_bands = 0
    conn = None
    cur = None

    def __init__(self):
        pass

    def get_raster_files(self):
        for ext in self.extensions:
            for file in glob.glob("*{}".format(ext)):
                files.append(os.path.abspath(file))
        return files

    def get_file_names(self):
        for file in self.files:
            file_name.append(os.path.basename(file))
        return file_name

    def establish_connection(self,file_name):
        self.conn = sqlite3.connect("{}.sqlite".format(file_name))
        self.cur = conn.cursor()

    def open_dataset(self,file_name):
        ds = gdal.Open(file_name)
        self.n_bands = ds.RasterCount

    def create_table(self,):
        for band in range(1,self.n_bands+1):
            stmt = "CREATE TABLE b{} (x{} INTEGER);".format(band,str(1))
            self.cur.execute(stmt)
            for i in range(2,rows+1):
                stmt = "ALTER TABLE b{} ADD COLUMN x{} INTEGER;".format(band,str(i))
                self.cur.execute(stmt)

        for band in range(self.n_bands):
            band_data = np.array(ds.GetRasterBand(1).ReadAsArray().astype(np.float32))
            rows, columns = list(band_data.shape)

            self.all_bands.append(band_data)

            print "No. of rows:", rows
            print "No. of columns:", columns

        print "No. of bands:", self.n_bands

if __name__ == "__main__":
    obj = engine()
