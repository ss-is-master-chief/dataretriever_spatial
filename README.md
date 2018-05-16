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

### Find current user

`postgres=# SELECT current_user;`

### Find list of users and corresponding databases

```
select u.usename,
       (select string_agg(d.datname, ',' order by d.datname)
        from pg_database d
        where has_database_privilege(u.usename, d.datname, 'CONNECT')) as allowed_databases
from pg_user u
order by u.usename
```

### List all schemas

```
postgres=# \dn
      List of schemas
      Name      |   Owner
----------------+-----------
 public         | sumitsaha
 topology       | sumitsaha
 usgs_elevation | sumitsaha
(3 rows)
```

### Find tables in schema "usgs_elevation"

```
postgres=# \dt usgs_elevation.*
                      List of relations
     Schema     |          Name           | Type  |   Owner
----------------+-------------------------+-------+-----------
 usgs_elevation | usgs_ned_13_n40w095_img | table | sumitsaha
 usgs_elevation | usgs_ned_13_n41w095_img | table | sumitsaha
(2 rows)
```

### Find tables in all schemas

```
postgres=# \dt *.*
                        List of relations
       Schema       |          Name           | Type  |   Owner
--------------------+-------------------------+-------+-----------
 information_schema | sql_features            | table | sumitsaha
 information_schema | sql_implementation_info | table | sumitsaha
 information_schema | sql_languages           | table | sumitsaha
 information_schema | sql_packages            | table | sumitsaha
 information_schema | sql_parts               | table | sumitsaha
 information_schema | sql_sizing              | table | sumitsaha
 information_schema | sql_sizing_profiles     | table | sumitsaha
 pg_catalog         | pg_aggregate            | table | sumitsaha
 pg_catalog         | pg_am                   | table | sumitsaha
 pg_catalog         | pg_amop                 | table | sumitsaha
 pg_catalog         | pg_amproc               | table | sumitsaha
 pg_catalog         | pg_attrdef              | table | sumitsaha
 pg_catalog         | pg_attribute            | table | sumitsaha
 pg_catalog         | pg_auth_members         | table | sumitsaha
 pg_catalog         | pg_authid               | table | sumitsaha
 pg_catalog         | pg_cast                 | table | sumitsaha
 pg_catalog         | pg_class                | table | sumitsaha
 pg_catalog         | pg_collation            | table | sumitsaha
 pg_catalog         | pg_constraint           | table | sumitsaha
 pg_catalog         | pg_conversion           | table | sumitsaha
 pg_catalog         | pg_database             | table | sumitsaha
 pg_catalog         | pg_db_role_setting      | table | sumitsaha
 pg_catalog         | pg_default_acl          | table | sumitsaha
 pg_catalog         | pg_depend               | table | sumitsaha
 pg_catalog         | pg_description          | table | sumitsaha
 pg_catalog         | pg_enum                 | table | sumitsaha
 pg_catalog         | pg_event_trigger        | table | sumitsaha
 pg_catalog         | pg_extension            | table | sumitsaha
 pg_catalog         | pg_foreign_data_wrapper | table | sumitsaha
 pg_catalog         | pg_foreign_server       | table | sumitsaha
 pg_catalog         | pg_foreign_table        | table | sumitsaha
 pg_catalog         | pg_index                | table | sumitsaha
 pg_catalog         | pg_inherits             | table | sumitsaha
 pg_catalog         | pg_init_privs           | table | sumitsaha
 pg_catalog         | pg_language             | table | sumitsaha
 pg_catalog         | pg_largeobject          | table | sumitsaha
 pg_catalog         | pg_largeobject_metadata | table | sumitsaha
 pg_catalog         | pg_namespace            | table | sumitsaha
 pg_catalog         | pg_opclass              | table | sumitsaha
 pg_catalog         | pg_operator             | table | sumitsaha
 pg_catalog         | pg_opfamily             | table | sumitsaha
 pg_catalog         | pg_partitioned_table    | table | sumitsaha
 pg_catalog         | pg_pltemplate           | table | sumitsaha
 pg_catalog         | pg_policy               | table | sumitsaha
```
