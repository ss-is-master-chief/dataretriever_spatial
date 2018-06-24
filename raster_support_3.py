import os, sys
import sqlite3

from osgeo import gdal
from osgeo import gdalconst

dest = sqlite3.connect("sqlite.db")
cur = dest.cursor()

path = "/Users/sumitsaha/Desktop/229_HARV_landRGB.tif"

data = gdal.OpenShared(path, gdalconst.GA_ReadOnly)

GeoTrans = data.GetGeoTransform()

ColRange = range(data.RasterXSize)
RowRange = range(data.RasterYSize)

for band in range(1, data.RasterCount+1):

    rBand = data.GetRasterBand(band)
    nData = rBand.GetNoDataValue()

    if nData == None:
        nData = -9999
    else:
        print("NoData Value: {}".format(nData))

    HalfX = GeoTrans[1] / 2
    HalfY = GeoTrans[5] / 2

    sql = "DROP TABLE IF EXISTS {}_band{}".format("HARV_landRGB",band)
    cur.execute(sql)

    print("Creating table {}_band{}".format("HARV_landRGB",band))

    create_stmt = "CREATE TABLE {}_band{} (x INT,y INT,z INT);".format("HARV_landRGB", band)
    cur.execute(create_stmt)

    # sys.exit("Done with a table")

    print("Inserting values to {}_band{}".format("229_HARV_landRGB", band))

    for row in RowRange:
            RowData = rBand.ReadAsArray(0, row, data.RasterXSize, 1)[0]
            for col in ColRange:
                if RowData[col] != nData:
                    if RowData[col] > 0:
                        X = GeoTrans[0] + ( col * GeoTrans[1] )
                        Y = GeoTrans[3] + ( row * GeoTrans[5] )
                        X += HalfX
                        Y += HalfY

                        insert_stmt = """INSERT INTO {}_band{}(x, y, z) VALUES(?, ?, ?);""".format("HARV_landRGB", band)
                        cur.execute(insert_stmt, (int(X), int(Y), int(RowData[col])))

    dest.commit()

    print("End of insertion to {}_band{}".format("HARV_landRGB", band))

    # sys.exit("Done with a table")
