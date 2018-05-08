# spatial_support
Concept scripts for Spatial Data support module

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
