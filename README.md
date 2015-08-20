# gdal2tiles-tilemaker

This a couple of convenience scripts wrapping around GDAL and ImageMagick for quick and dirty TMS tiles generation.

## Prerequisites

The scripts has been tested with:

- __Python 2.7.6;__
- __GDAL 1.11.2, released 2015/02/10;__
- __ImageMagick 6.9.2-0;__
- __Wand (ImageMagick Python bindings) 0.4.1.__

## Scripts

Two very basic scripts are present: __tilemaker.py__ and __tilemaker_composite.py__. The former is for tiling ortophotos using GDAL VRT mosaics, and the latter is for compositing tile sets, so incremental tiling can be made of a large area (and is a crude, primitive way to multicore tiling, by the way).

To tile a set of ortos, put them in a folder. Please note that due to image homogenity requirements of GDAL VRT in terms of layers, data sizes and such, those ortos must share internal structure and maybe format. Then create a folder for the generated tiles and run:

```Shell
python tilemaker.py <source folder> <target folder> <Source EPSG code> <Start zoom> <End zoom>
```

To compose two tile sets, use __tilemaker_composite.py__:

```Shell
python tilemaker_composite.py <source folder> <target folder> <keep originals>
```

where __<keep originals>__ is either __true__ or __false__. Keep in mind that the tiles in __<target folder>__ will be modified. A backup of the originals will be made if __<keep originals>__ is true.
