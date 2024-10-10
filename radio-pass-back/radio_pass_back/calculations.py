import csv
from datetime import datetime, timedelta
from pathlib import Path

from skyfield.api import EarthSatellite, Timescale, load, wgs84

from radio_pass_back.models import SatelliteTrajectory


def load_amateur_satellites_data(ts: Timescale) -> list[EarthSatellite]:
    """Loads amateur satellites data from csv, returns a list of EarthSatellite objects."""
    csv_path = Path(__file__).parent / "amateur.csv"
    with csv_path.open() as f:
        data = list(csv.DictReader(f))
    sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
    print("Loaded", len(sats), "satellites")
    print(*[sat.name for sat in sats][:10])
    return sats


# generate timescale object
TS = load.timescale()
SATELLITES = load_amateur_satellites_data(TS)


def find_trajectory(
    t1: datetime, t2: datetime, satellite, n_points: int = 10
) -> SatelliteTrajectory:
    """Gets trajectory data for 'satellite' from t1 to t2."""
    t_start, t_end = TS.utc(t1), TS.utc(t2)
    delta = (t2 - t1) / n_points
    points = []

    for i in range(n_points):
        # find geocentric position
        t = t_start + i * delta
        geocentric = satellite.at(t)
        # convert to latitude + longitude
        lat, lon = wgs84.latlon_of(geocentric)
        points.append([t.utc_datetime().timestamp(), lat.degrees, lon.degrees])
    return SatelliteTrajectory(points=points, name=satellite.name)


def get_passes(
    user_coords: tuple, satellite: EarthSatellite
) -> list[SatelliteTrajectory]:
    """returns passes between time and (time+24h) for this satellite. WIP"""
    # our first need is to find when satellites rise and set:
    # https://rhodesmill.org/skyfield/earth-satellites.html#finding-when-a-satellite-rises-and-sets
    user_location = wgs84.latlon(user_coords[0], user_coords[1])
    t0, t1 = TS.now(), TS.now() + timedelta(days=1)
    passes = []

    t, events = satellite.find_events(user_location, t0, t1, altitude_degrees=10.0)
    for ti, event in zip(t, events):
        print(ti.utc_strftime("%Y %b %d %H:%M:%S"), event)
        if event == 0:
            ...
        elif event == 2:
            ...
    return passes
