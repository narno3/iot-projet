import csv
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

from skyfield.api import EarthSatellite, Timescale, load, wgs84

from radio_pass_back.models import SatelliteTrajectory


def load_amateur_satellites_tle(ts: Timescale) -> list[EarthSatellite]:
    """Loads amateur satellites data from csv, returns a list of EarthSatellite objects."""
    csv_path = Path(__file__).parent / "amateur_tle.csv"
    with csv_path.open() as f:
        data = list(csv.DictReader(f))
    sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
    print("Loaded", len(sats), "satellites")
    print(*[sat.name for sat in sats][:10])
    return sats


def load_amateur_satellites_info(satellites) -> list:
    """Loads additional info per sat."""
    csv_path = Path(__file__).parent / "amateur_satcat_data.csv"
    sat_indices = {sat.name: i for i, sat in enumerate(satellites)}
    sat_info_dict = {}
    with csv_path.open() as f:
        header = f.readline().split(',')
        while line := f.readline():
            data = line.split(",")
            index = sat_indices[data[0]]
            sat_info_dict[index] = [index] + data
    return [header] + [sat_info_dict[i][1:] for i in range(len(sat_info_dict))]


# generate timescale object
TS = load.timescale()
SATELLITES = load_amateur_satellites_tle(TS)
SATELLITES_INFO = load_amateur_satellites_info(SATELLITES)


def get_sat_position(satellite: EarthSatellite, t: datetime) -> tuple:
    """Returns the satellite's lat and long at time t"""
    # find geocentric position
    geocentric = satellite.at(TS.utc(t))
    # convert to latitude + longitude
    lat, lon = wgs84.latlon_of(geocentric)
    return lat.degrees, lon.degrees


def find_trajectory(
    t_start: datetime, t_end: datetime, satellite: EarthSatellite, n_points: int = 10
) -> SatelliteTrajectory:
    """Gets trajectory data for 'satellite' from t1 to t2."""
    delta = (t_end - t_start) / n_points
    points = []

    for i in range(n_points):
        t = t_start + i * delta
        lat, lon = get_sat_position(satellite, t)
        points.append([t.timestamp(), lat, lon])
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


def update_all_sat_positions(positions: list):
    """Indefinitely update satellite's positions."""
    while True:
        now = datetime.now(tz=UTC)
        for i, sat in enumerate(SATELLITES):
            lat, lon = get_sat_position(sat, now)
            positions[i] = [lat, lon]
        time.sleep(0.25)
