# spatial_support

## Finding GDAL_DATA path

Write `gdal-config --datadir` in Terminal which will give something like `/Library/Frameworks/GDAL.framework/Versions/2.2/Resources/gdal`

## GDAL import error

Sometimes there are issues with importing GDAL, OGR, etc from OSGEO and the following results are obtained

```
>>> import osgeo
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'osgeo'
```

This can be rectified by initialising the path for the script to look for the GDAL framework

Refer here: https://gis.stackexchange.com/questions/233654/install-gdal-python-binding-on-mac

Solution:

```
>>> import sys
>>> sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')
>>> import osgeo
>>> print(osgeo.__version__)
2.2.3
```

## Installing PostgreSQL

`brew install postgresql`

The above does not install extensions such as `postgis` and `postgis_topology`. It is recommended that `PostGIS` is directly installed using `brew` by running the following command:

`brew install postgis`

`postgresql` is a dependency for `postgis`, and will be installed automatically.

The extensions are located here `/usr/local/share/postgresql/extension`.

## Running postgresql

### Check Version

```
~ $ postgres -V
postgres (PostgreSQL) 10.4
```

### Running postgresql

`psql postgres`

```
~ $ psql postgres
psql (10.4)
Type "help" for help.

postgres=#
```
### Show current users

`postgres=# \du+`

```
postgres=# \du+
                                          List of roles
 Role name |                         Attributes                         | Member of | Description
-----------+------------------------------------------------------------+-----------+-------------
 postgres  |                                                            | {}        |
 sumitsaha | Superuser, Create role, Create DB, Replication, Bypass RLS | {}        |
```

### Set password for user "postgres"

```
postgres=# \password postgres
Enter new password:
Enter it again:
```
