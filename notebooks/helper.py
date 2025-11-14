"""Helper functions for polarstern_mosaic_full_cruise.ipynb"""
from typing import List
import re
import itertools
from pqdm.processes import pqdm

from shapely.geometry import Point, LineString
from shapely.errors import GEOSException

import xarray as xr
import geopandas as gpd
import pandas as pd

def point_to_linestring(ds, group, every):
    """Converts arrays of geographic coordinates to a shapely.LineString

    Arguments:
      ds : xarray.Dataset or xarray.DataTree object
      group : name of group to extract coordinates
      every : sample every point

    Returns:
      shapely.LineString
    """
    longitude = ds[f"{group}/freeboard_segment/longitude"][::every]
    latitude = ds[f"{group}/freeboard_segment/latitude"][::every]
    
    if (longitude.shape[0] == 0):
        raise ValueError("longitude is empty array")
    if (latitude.shape[0] == 0):
        raise ValueError("latitude is empty array")
                         
    return LineString([(lon, lat) for lon, lat in zip(longitude, latitude)])
    
    
def extract_beams(ds, every: int=1000) -> List:
    """
    Extract coordinates for strong beams and returns as LineStrings

    Arguments:
      fn : file-like object containing ATL10 ICESat-2
      every : sample every N points.  Default 1000.

    Returns:
      List of LinearString geometries
    """

    geometries = []
    data = {
        "beam": [],
        # "fileid" [],
        "file_date": []
    }
    
    p = re.compile(r"/gt.{2}$")
    for group in ds.groups:
        if p.match(group):
            if ds[group].attrs['atlas_beam_type'] == "strong":
                try:
                    line = point_to_linestring(ds, group, every)
                except ValueError as err:
                    # print(f"Ground track {group} is empty")
                    print(f"Skipping extracting beam {group}: {err}")
                    continue
                except GEOSException as err:
                    print(f"Skipping extracting beam {group}: {err}")
                    continue
                    
                geometries.append(line)
                data["beam"].append(group)
                data["file_date"].append(ds.attrs["time_coverage_start"])

    # return geometries
    return gpd.GeoDataFrame(data, geometry=geometries, crs="EPSG:4326")

def ground_tracks_from_file(fn, every: int=5000):
    """Extracts coordinates for beams in an ATL10 files

    Arguments:
      fn : file-like object

    Returns:
      list of shapely.LinearStrings
    """
    with xr.open_datatree(fn, decode_timedelta=False, phony_dims="sort") as ds:
        geometries = extract_beams(ds, every)
    
    return geometries
    
    
def beams_to_geopandas(files):
    """Converts beams in ATL10 files to geopandas.GeoDataFrame
    
    Arguments:
      files : list of file-like objects
    
    Returns:
      geopandas.GeoDataFrame
    """

    features = pqdm(files, ground_tracks_from_file, n_jobs=8)
    # features = list(itertools.chain.from_iterable(features))
    # return gpd.GeoDataFrame(geometry=features, crs="EPSG:4326")
    return pd.concat(features, ignore_index=True)