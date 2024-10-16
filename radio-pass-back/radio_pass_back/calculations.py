import csv
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

from skyfield.api import EarthSatellite, Timescale, load, wgs84, Time

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
        header = f.readline().split(",")
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
        points.append([t.strftime("%d/%m %H:%M"), lat, lon])
    return SatelliteTrajectory(points=points, name=satellite.name)


def get_passes(
    user_coords: tuple, satellite: EarthSatellite, t_start: Time, t_end: Time
) -> list[SatelliteTrajectory]:
    """Returns passes between time and (time+24h) for this satellite."""
    # our first need is to find when satellites rise and set:
    # https://rhodesmill.org/skyfield/earth-satellites.html#finding-when-a-satellite-rises-and-sets
    user_location = wgs84.latlon(user_coords[0], user_coords[1])
    # t0, t1 = TS.now(), TS.now() + timedelta(days=1)
    passes = []
    pass_start, pass_end = None, None
    t, events = satellite.find_events(
        user_location, t_start, t_end, altitude_degrees=10.0
    )
    ti: Time
    for ti, event in zip(t, events):
        # print(ti.utc_strftime("%Y %b %d %H:%M:%S"), event)
        if event == 0:
            pass_start = ti.utc_datetime()
        elif event == 2 and pass_start:
            pass_end = ti.utc_datetime()
            traj = find_trajectory(pass_start, pass_end, satellite, n_points=20)
            passes.append(traj)
    return passes


def find_all_passes(user_coords: tuple) -> list:
    """Returns all passes, for this location, within one day."""
    all_passes: list = []
    # t_start, t_end = TS.now(), TS.now() + timedelta(days=1)
    t_start = TS.utc(datetime.now(tz=UTC))
    t_end = t_start + timedelta(hours=3)
    # step 1: get all of the next passes
    for i, sat in enumerate(SATELLITES):
        if sat_passes := get_passes(user_coords, sat, t_start, t_end):
            all_passes.extend([i, p.points] for p in sat_passes)

    # step 2: sort by time
    def key_function(element):
        return element[1][0][0]  # <-- the date of the first point

    all_passes.sort(key=key_function)
    return all_passes


def update_all_sat_positions(positions: list):
    """Indefinitely update satellite's positions."""
    while True:
        now = datetime.now(tz=UTC)
        for i, sat in enumerate(SATELLITES):
            lat, lon = get_sat_position(sat, now)
            positions[i] = [lat, lon]
        time.sleep(0.25)
