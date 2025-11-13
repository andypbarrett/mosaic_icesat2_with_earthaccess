# Access MOSAiC ICESat-2 Tracks with `earthaccess`
This tutorial demonstrates how to use `earthaccess` to search for and access ICESat-2 tracks that were near the Polarstern Drift during the MOSAiC project.  The tutorial was originally developed for the NASA ICESat-2 Science Team.  It was updated to use the new developments in `earthaccess` and was presented in it's current form at the Openscapes Community Call: A welcome to NASA Earthdata and earthaccess.

The demonstration was developed to run in the Openscapes 2i2c Hub in AWS region us-west-2.  This allows efficient access to data in the NASA Earthdata Cloud, which is hosted in the same region.  However, the workflow should work from a local machine just a lot more slowly.

To run the demonstration you will need to clone the repo in you hub compute instance.

```
$ git clone https://github.com/andypbarrett/mosaic_icesat2_with_earthaccess.git
```

Navigate to the `mosaic_icesat2_with_earthaccess` folder.  The notebook is in the `notebooks` folder.

If you are working in the Openscapes 2i2c hub, all the Python packages should be installed.  If you are working in a different cloud compute instance or on a local machine, you will need to have the required packages installed.

Required packages:
- earthaccess
- xarray
- pandas
- geopandas
- matplotlib
- cartopy
- shapely
