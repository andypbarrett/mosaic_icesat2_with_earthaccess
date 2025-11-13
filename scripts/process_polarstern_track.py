"""Processes Polarstern track file for demonstration"""
from pathlib import Path
from collections import namedtuple
import datetime as dt

import pandas as pd
import geopandas as gpd

# Define on-floe periods
MosaicFloe = namedtuple("FloeDates", ['start', 'end'])
floe1 = MosaicFloe(dt.datetime(2019, 10, 4), dt.datetime(2020, 5, 17))
floe2 = MosaicFloe(dt.datetime(2020, 6, 19), dt.datetime(2020, 7, 31))
floe3 = MosaicFloe(dt.datetime(2020, 8, 21), dt.datetime(2020, 9, 20))

POLARSTERN_DRIFT_FILE = Path("../data/polarstern_track_full_cruise.txt")


def process_polarstern_track():
    """Processes Polarstern track file: removes transit points to retain on-floe points only;
    samples midday locations.

    Returns:
      Geopandas DataFrame
    """
    df = pd.read_csv(POLARSTERN_DRIFT_FILE, sep="\t", index_col=0, parse_dates=True)

    # Sample only midday UTC locations
    df = df[(df.index.hour == 12) & (df.index.minute == 0)]

    # Assign floe identifiers
    df["Floe"] = 0
    df.loc[(df.index >= floe1.start) & (df.index <= floe1.end), "Floe"] = 1
    df.loc[(df.index >= floe2.start) & (df.index <= floe2.end), "Floe"] = 2
    df.loc[(df.index >= floe3.start) & (df.index <= floe3.end), "Floe"] = 3
    df = df[df["Floe"] > 0]

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")

    # Write to file
    gdf.to_file(Path("../data/polarstern_track_full_cruise_processed.geojson"), driver='GeoJSON')

                
if __name__ == "__main__":
    process_polarstern_track()