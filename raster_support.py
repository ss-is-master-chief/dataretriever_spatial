import os
import sys
import csv
import glob
from tqdm import tqdm
import numpy as np

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

    extensions = [".tif",".jpg",".jpeg",".png"]
    supported_extensions = []
    files = []
    file_name = []
    n_raster_bands = 0
    df = None
    conn = None
    cur = None
    validity = 0

    def __init__(self):
        self.get_raster_files()

        for file in self.file_name:
            self.create_database(file)

        for file in self.file_name:
            self.db_connection(file)
            self.open_raster_dataset(file)
            self.install_into_sqlite(file)
            self.df = None
            self.cur.close()
            self.validity = 0

        '''Add supported extensions only to the operational list'''

        conn = sqlite3.connect("metadata.db")
        cur = conn.cursor()

        for row in list(cur.execute("SELECT file_type FROM metadata"))[0]:
            if row not in self.supported_extensions:
                self.supported_extensions.append(str(row))

        cur.close()

    '''Get paths to available raster files in current directory'''

    def get_raster_files(self):
        for ext in self.extensions:
            for file in glob.glob("*{}".format(ext)):
                self.files.append(os.path.abspath(file))
        self.get_file_names()

    def get_file_names(self):
        for file in self.files:
            self.file_name.append(os.path.basename(file))

    def create_database(self,file_name):
        try:

            '''rsplit removes raster extension from name for DB name'''

            file_name_wo_ext = file_name.rsplit(".",1)[0]
            os.system("spatialite {}.sqlite '.databases'".format(file_name_wo_ext))
        except Error as e:
            print(e)

    def db_connection(self,file_name):
        file_name_wo_ext = file_name.rsplit(".",1)[0]
        self.conn = sqlite3.connect("{}.sqlite".format(file_name_wo_ext))
        self.cur = self.conn.cursor()

    def open_raster_dataset(self,file_name):
        try:
            self.df = gdal.Open(file_name)
        except RuntimeError, e:
            print("Unable to open raster file")
            print(e)
            sys.exit(1)

    '''Count of Raster Bands to iterate through while installing'''

    def get_raster_bands(self,file_name):
        self.n_raster_bands = self.df.RasterCount

    def get_metadata(self):
        return self.df.GetMetadata()

    '''Check if band already exists'''

    def drop_table_statement(self,band):
        self.cur.execute("DROP TABLE IF EXISTS b{};".format(band))

    '''Installing data into SQLite'''

    def install_into_sqlite(self,file_name):
        self.get_raster_bands(file_name)
        file_name_wo_ext = file_name.rsplit(".",1)[0]

        for band in range(1,self.n_raster_bands+1):

            self.drop_table_statement(band)

            print("Installing band {}/{} of {} into {}.sqlite".format(band,

            self.n_raster_bands,file_name,file_name_wo_ext))

            '''gdal_translate generates temporary CSV file'''

            os.system("gdal_translate -b {} -of XYZ {} {}.csv \
            -co ADD_HEADER_LINE=YES".format(band, file_name, file_name_wo_ext))

            self.temp_csv_to_sqlite(file_name_wo_ext,band)

            '''remove temporary CSV'''

            os.system("rm {}.csv".format(file_name_wo_ext))

            self.check_valid_installation(band)

            if(self.validity==self.n_raster_bands):
                self.create_metadata_db(file_name)

    def temp_csv_to_sqlite(self,file_name_wo_ext,band):

        '''ogr2ogr translates temporary CSV into SQLite database'''

        os.system("ogr2ogr -update -append -f SQLite {}.sqlite \
        -nln b{} {}.csv -dsco METADATA=NO \
        -dsco INIT_WITH_EPSG=NO".format(file_name_wo_ext, band, file_name_wo_ext))

    def check_valid_installation(self,band):
        for c in self.cur.execute("SELECT Count(*) FROM b{}".format(band)):
            count = list(c)[0]

        band_data = np.array(self.df.GetRasterBand(band).ReadAsArray().astype(np.float32))
        rows, columns = list(band_data.shape)

        if(count==rows*columns):
            self.validity += 1

    '''Database containing installed raster db information'''

    def create_metadata_db(self,file_name):
        conn = sqlite3.connect("metadata.db")
        cur = conn.cursor()

        statement_create = r"CREATE TABLE IF NOT EXISTS metadata (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, file_type TEXT);"

        cur.execute(statement_create)

        file_name_wo_ext = file_name.rsplit(".",1)[0]
        file_extension = "."+file_name.rsplit(".",1)[1]

        params = (file_name_wo_ext,file_extension)

        statement_insert = r"INSERT INTO metadata VALUES (NULL,?,?);"

        cur.execute(statement_insert,params)
        conn.commit()

        '''
        When running the script the older values are appended again.
        The following SQLite statements take care of it by,
        getting the distinct current data from table
        and replacing the old table with the new values obtained.

        '''

        statement_distinct = r"SELECT DISTINCT file_name, file_type from metadata;"

        insertions = []

        for row in cur.execute(statement_distinct):
            insertions.append([str(list(row)[0]),str(list(row)[1])])

        truncate = r"DELETE FROM metadata"
        cur.execute(truncate)

        reset_autoincrement = r"DELETE FROM sqlite_sequence WHERE name='metadata';"
        cur.execute(reset_autoincrement)

        cur.execute(statement_create)

        statement_insert = r"INSERT INTO metadata VALUES (NULL,?,?);"

        for val in insertions:
            params = (val[0],val[1])
            cur.execute(statement_insert,params)
            conn.commit()

        conn.close()


if __name__=="__main__":

    obj = sqlite_engine()
