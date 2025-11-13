"""Helper functions for polarstern_mosaic_full_cruise.ipynb"""
from typing import List
import re
import itertools

from shapely.geometry import Point, LineString
import xarray as xr
import geopandas as gpd

def point_to_linestring(ds, group, every):
    """Converts arrays of geographic coordinates to a shapely.LineString

    Arguments:
      ds : xarray.Dataset or xarray.DataTree object
      group : name of group to extract coordinates
      every : sample every point

    Returns:
      shapely.LineString
    """
    line = LineString(
        [
            (lon, lat) 
            for lon, lat in zip(
                ds[f"{group}/freeboard_segment/longitude"][::every], 
                ds[f"{group}/freeboard_segment/latitude"][::every]
                )
            ]
        )
    return line
    
    
def extract_beams(ds: xr.DataTree, every: int=1000) -> List:
    """
    Extract coordinates for strong beams and returns as LineStrings

    Arguments:
      ds : xarray.DataTree object containing ATL10 ICESat-2
      every : sample every N points.  Default 1000.

    Returns:
      List of LinearString geometries
    """

    geometries = []

    p = re.compile(r"/gt.{2}$")
    for group in ds.groups:
        if p.match(group):
            if ds[group].attrs['atlas_beam_type'] == "strong":
                try:
                    line = point_to_linestring(ds, group, every)
                except Exception as err:
                    raise RunTimeError
                    
                geometries.append(line)

    return geometries


def beams_to_geopandas(files):

    features = []
    
    for f in files:
        ds = xr.open_datatree(f, decode_timedelta=False, phony_dims="sort")

        features.append(extract_beams(ds))

    features = list(itertools.chain.from_iterable(features))
    
    return gpd.GeoDataFrame(geometry=features, crs="EPSG:4326")