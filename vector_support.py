import sys
import os
import sqlite3
import csv
from osgeo import ogr

# os.system("ogr2ogr -overwrite -progress -f csv {} {}".format(sys.argv[1], sys.argv[2]))
#
# conn = sqlite3.connect("sqlite.db")
# conn.text_factory = str #allow utf-8 data to be stored
# cur = conn.cursor()
#
# file = "{}".format(sys.argv[1])
#
# with open(file,"w+") as f:
#     reader = csv.reader(f)
#     header = True
#     for row in reader:
#         if header:
#             # gather column names from the first row of the csv
#             header = False
#
#             sql = "DROP TABLE IF EXISTS {}".format(self.file_name)
#             cur.execute(sql)
#
#             list = list(str(column) for column in row)
#             separator = ", "
#             head = separator.join(list)
#
#             sql = "CREATE TABLE {} ({})".format(self.file_name, head)
#             cur.execute(sql)
#
#             for column in row:
#                 if column.lower().endswith("_id"):
#                     index = "{}__{}".format(self.file_name, column)
#                     sql = "CREATE INDEX {} on {} ({})".format( index, self.file_name, column )
#                     cur.execute(sql)
#
#             list = list("?" for column in row)
#             separator = ", "
#             head = separator.join(list)
#
#             insertsql = "INSERT INTO {} VALUES ({})".format(self.file_name, head)
#
#             rowlen = len(row)
#
#         else:
#             # skip lines that don't have the right number of columns
#             if len(row) == rowlen:
#                 cur.execute(insertsql, row)
#
# conn.commit()
#
# cur.close()
# conn.close()

ds = ogr.Open('map.shp',0)
print "Layer Count:", ds.GetLayerCount()

shape = ds.GetLayer(0)


# feature = shape.GetFeature(0)

layerdefn = shape.GetLayerDefn()

fields = list()

for i in range(layerdefn.GetFieldCount()):
    fields.append(layerdefn.GetFieldDefn(i).GetName())

field_list = ','.join(fields)

print "Fields:", field_list

# sql_stmt = "SELECT {} from map".format(field_list)
# print(sql_stmt)
#
os.system("ogr2ogr -append -overwrite -f 'sqlite' hi.db /Users/sumitsaha/Desktop/map/map.shp")
