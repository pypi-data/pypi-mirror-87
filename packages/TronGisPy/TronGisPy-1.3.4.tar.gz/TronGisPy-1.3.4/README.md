# Introduction
The repo aims to build a geographic information system (GIS) library for Python interface. The library includes the following modules.

# Instlall
## Windows
1. Install preinstall thinktron pypi server
```
pip install -U --index-url http://192.168.0.128:28181/simple --trusted-host 192.168.0.128 GDAL==3.0.4 Fiona==1.8.13 Shapely==1.6.4.post2 geopandas==0.7.0 Rtree==0.9.4 opencv_python==4.1.2
```

2. Install TronGisPy from thinktron pypi server (Windows)
```
pip install -U --extra-index-url http://192.168.0.128:28181/simple --trusted-host 192.168.0.128 TronGisPy
```

## Linux
1. Build GDAL==3.0.4 by yourself
2. Build opencv==4.1.2 by yourself
3. install preinstall from public pypi server
```
pip install GDAL==3.0.4 Fiona==1.8.13 Shapely==1.6.4.post2 geopandas==0.7.0 Rtree==0.9.4
```

3. Install TronGisPy from thinktron pypi server (Windows)
```
pip install -U --extra-index-url http://rd.thinktronltd.com:28181/simple --trusted-host rd.thinktronltd.com TronGisPy
```

# Quick Start
```python
import TronGisPy as tgp
raster = tgp.read_raster(tgp.get_testing_fp('satellite_tif'))
print("raster.data.shape:", raster.data.shape)
print("raster.geo_transform:", raster.geo_transform)
print("raster.projection:", raster.projection)
print("raster.no_data_value:", raster.no_data_value)
raster.plot()
```

# For Developer
## Build
```bash
python setup.py sdist bdist_wheel
```
## Document Generation
0. [Installaion](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/install.html)
```
pip install sphinx
pip install sphinx-rtd-theme
pip install numpydoc
```

1. generatate index.rst (https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)
```
mkdir docs
cd docs
sphinx-quickstart
```

2. modify docs/source/conf.py (https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
```
vim source/conf.py
```
```
base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(base_dir, '..', '..')))

html_theme = "classic"
extensions = ['sphinx.ext.napoleon']
exclude_patterns = ['setup.py', 'req_generator.py', 'test.py']
```

3. generate TronGisPy rst
```
cd ..
python clean_docs_source.py
sphinx-apidoc --force --separate --module-first -o docs\source .
```

4. generate html
```
cd docs
make clean
make html
```

<!-- 
## TronGisPy Main Modules
1. Raster: This module is Main class in this library. A Raster object contains all required information for a gis raster file such as `.tif` file including digital number for each pixel, number of rows, number of cols, number of bands, geo_transform, projection, no_data_value and metadata. 

2. CRS: Converion the indexing system e.g. coordinate & numpy index and wkt & epsg. 

3. TypeCast: Mapping the nearest data type betyween gdal and numpy, and convert the gdal data type from integer to readable string. 

4. ShapeGrid: Interaction between raster and vector data. 

5. Normalizer: Normalize the Image data for model training or plotting.

6. AeroTriangulation: Do the aero-triangulation calculation.

7. Interpolation: Interpolation for raster data on specific cells which are usually nan cells.

8. SplittedImage: Split remote sensing images for machine learning model training.

9. DEMProcessor: General dem processing functions e.g. shadow, slope, TRI, TPI and roughness.

10. GisIO: Some file-based gis functions. -->