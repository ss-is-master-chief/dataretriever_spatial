import os
import sys
import csv
import glob
from tqdm import tqdm
import numpy as np
#import subprocess
import zipfile

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

class sqlite_engine:

    extensions = [".tif",".jpg",".jpeg",".png"]
    supported_extensions = []
    files = []
    zip_files = []
    dir_files = {}
    file_name = []
    n_raster_bands = 0
    df = None
    conn = None
    cur = None
    validity = 0

    def __init__(self):
        self.get_raster_files()

        print("AVAILABLE DATAFILES")
        print(len(max(self.file_name,key=len))*'-')
        for files in self.file_name:
            print(files)
        print(len(max(self.file_name,key=len))*'-')

        self.ask_input()

        '''Add supported extensions only to the operational list'''

        conn = sqlite3.connect("metadata.db")
        cur = conn.cursor()

        for row in list(cur.execute("SELECT file_type FROM metadata"))[0]:
            if row not in self.supported_extensions:
                self.supported_extensions.append(str(row))

        cur.close()

    def ask_input(self):
        choice = raw_input("Enter dataset to install: ")

        if(len(choice)<1):
            for file in self.file_name:
                self.function_flow(file_name)
                
        elif choice not in self.file_name:
            print("Requested dataset not available. Enter valid dataset..")
            self.ask_input()

        else:
            self.function_flow(choice)

    def function_flow(self,file_name):
        self.db_connection(file_name)
        self.open_raster_dataset(file_name)
        self.install_into_sqlite(file_name)
        self.df = None
        self.cur.close()
        self.validity = 0

    '''Get paths to available raster files in current directory'''

    def get_raster_files(self):
        for ext in self.extensions:
            for file in glob.glob("*{}".format(ext)):
                self.files.append(os.path.abspath(file))

        self.get_zip_files()
        self.get_file_names()
        self.list_dir_files()
        #print(self.dir_files)


    '''Determining ZIP files containing EHdr datasets'''

    def get_zip_files(self):
        for file in glob.glob("*{}".format(".zip")):
            self.zip_files.append(os.path.abspath(file))
            self.extract_zip_files(file)

    '''Extracting from ZIP files containing EHdr datasets'''

    def extract_zip_files(self,file_path):
        for zf in self.zip_files:
            zip_dir = zipfile.ZipFile(zf)
            zip_dir.extractall(os.path.basename(zf).rstrip(".zip"))
            os.system("rm -rf {}/__MACOSX".format(os.path.basename(zf).rstrip(".zip")))
            zip_dir.close()

    def list_dir_files(self):
        for zf in self.file_name:
            if(zf.rsplit(".",1)[1]=="zip"):
                self.dir_files[zf.rsplit(".",1)[0]] = list(os.listdir(zf.rsplit(".",1)[0]))

    def get_file_names(self):
        for file in self.files:
            self.file_name.append(os.path.basename(file))

        for zf in self.zip_files:
            self.file_name.append(os.path.basename(zf))

    def db_connection(self,file_name):
        file_name_wo_ext = file_name.rsplit(".",1)[0]
        self.conn = sqlite3.connect("{}.sqlite".format(file_name_wo_ext))
        self.cur = self.conn.cursor()

    def open_raster_dataset(self,file_name):
        if(file_name.rsplit(".",1)[1]=="zip"):
            pre_text = file_name.rsplit(".",1)[0]

            for item in self.dir_files[file_name.rsplit(".",1)[0]]:
                if(item.rsplit(".",1)[1]=="bil"):
                    file_name = pre_text + "/" + item
                    try:
                        self.df = gdal.Open(file_name)
                    except RuntimeError, e:
                        print("Unable to open raster file")
                        print(e)
                        sys.exit(1)
        else:

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
        if(file_name.rsplit(".",1)[1]=="zip"):
            pre_text = file_name.rsplit(".",1)[0]

            for item in self.dir_files[file_name.rsplit(".",1)[0]]:
                if(item.rsplit(".",1)[1]=="bil"):
                    file_name = pre_text + "/" + item

        b = raw_input("Enter bounding box for {}: ".format(file_name))
        bb = [float(x) for x in b.split(" ")]

        self.get_raster_bands(file_name)
        file_name_wo_ext = file_name.rsplit(".",1)[0]

        for band in range(1,self.n_raster_bands+1):

            self.drop_table_statement(band)

            print("Installing band {}/{} of {} into {}.sqlite".format(band,

            self.n_raster_bands,file_name,file_name_wo_ext))

            '''gdal_translate generates temporary CSV file'''

            if(len(bb)!=4):
                os.system("gdal_translate -b {} -of XYZ {} {}.csv \
                -co ADD_HEADER_LINE=YES".format(band, file_name, file_name_wo_ext))
            else:
                os.system("gdal_translate -projwin {} {} {} {} \
                -b {} -of XYZ {} {}.csv \
                -co ADD_HEADER_LINE=YES".format(bb[0], bb[1], bb[2], bb[3], band, file_name, file_name_wo_ext))

            self.temp_csv_to_sqlite(file_name_wo_ext,band)

            '''remove temporary CSV'''

            os.system("rm {}.csv".format(file_name_wo_ext))

            #self.check_valid_installation(band)

            #if(self.validity==self.n_raster_bands):
            #    self.create_metadata_db(file_name)

    def temp_csv_to_sqlite(self,file_name_wo_ext,band):

        '''ogr2ogr translates temporary CSV into SQLite database'''

        os.system("ogr2ogr -update -append -f SQLite {}.sqlite \
        -nln b{} {}.csv -dsco METADATA=NO \
        -dsco INIT_WITH_EPSG=NO".format(file_name_wo_ext, band, file_name_wo_ext))

#    def check_valid_installation(self,band):
#        for c in self.cur.execute("SELECT Count(*) FROM b{}".format(band)):
#            count = list(c)[0]

#        if(count==self.df.RasterXSize * self.df.RasterYSize):
#            self.validity += 1

    '''Database containing installed raster db information'''

    def create_metadata_db(self,file_name):
        conn = sqlite3.connect("metadata.db")
        cur = conn.cursor()

        statement_create = r"""CREATE TABLE IF NOT EXISTS metadata
        (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT,
        file_type TEXT, no_bands INTEGER,
        rows INTEGER, columns INTEGER);"""

        cur.execute(statement_create)

        file_name_wo_ext = file_name.rsplit(".",1)[0]
        file_extension = "."+file_name.rsplit(".",1)[1]

        params = (file_name_wo_ext, file_extension,
        self.df.RasterCount, self.df.RasterXSize, self.df.RasterYSize)

        statement_insert = r"INSERT INTO metadata VALUES (NULL,?,?,?,?,?);"

        cur.execute(statement_insert,params)
        conn.commit()

        '''
        When running the script the older values are appended again.
        The following SQLite statements take care of it by,
        getting the distinct current data from table
        and replacing the old table with the new values obtained.

        '''

        statement_distinct = r"SELECT DISTINCT file_name,file_type,no_bands,rows,columns from metadata;"

        insertions = []

        for row in cur.execute(statement_distinct):
            insertions.append([str(list(row)[0]),str(list(row)[1]),
            str(list(row)[2]),str(list(row)[3]),str(list(row)[4])])

        truncate = r"DELETE FROM metadata"
        cur.execute(truncate)

        reset_autoincrement = r"DELETE FROM sqlite_sequence WHERE name='metadata';"
        cur.execute(reset_autoincrement)

        cur.execute(statement_create)

        statement_insert = r"INSERT INTO metadata VALUES (NULL,?,?,?,?,?);"

        for val in insertions:
            params = (val[0],val[1],val[2],val[3],val[4])
            cur.execute(statement_insert,params)
            conn.commit()

        #os.system("gdalinfo {} > info.txt".format(file_name))

        conn.close()



if __name__=="__main__":

    obj = sqlite_engine()
