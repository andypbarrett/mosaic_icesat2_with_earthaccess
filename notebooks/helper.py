"""Helper functions for polarstern_mosaic_full_cruise.ipynb"""
from typing import List
import re
import itertools

from shapely.geometry import Point, LineString
import xarray as xr
import geopandas as gpd

def to_linstring(ds):
    
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
                line = LineString(
                    [
                        (lon, lat) 
                        for lon, lat in zip(
                            ds[f"{group}/freeboard_segment/longitude"][::every], 
                            ds[f"{group}/freeboard_segment/latitude"][::every]
                            )
                        ]
                    )
                geometries.append(line)

    return geometries


def beams_to_geopandas(files):

    features = []
    
    for f in files:
        ds = xr.open_datatree(f, decode_timedelta=False, phony_dims="sort")

        features.append(extract_beams(ds))

    features = list(itertools.chain.from_iterable(features))
    
    return gpd.GeoDataFrame(geometry=features, crs="EPSG:4326")