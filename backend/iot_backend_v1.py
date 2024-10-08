from skyfield.api import EarthSatellite, load
import csv
from skyfield.api import wgs84
from pydantic import BaseModel


# we need amateur satellite data :

with load.open('amateur.csv', mode="r") as f:
    data = list(csv.DictReader(f))
ts = load.timescale() # why do we do this ?
sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
# print('Loaded', len(sats), 'satellites')
# print(*[sat.name for sat in sats][:10], sep=" | ", end=f" ... (+{len(sats) - 10} others)\n ")

user_location = wgs84.latlon(+40.8939, -83.8917)

satellite = sats[0]

t0 = ts.utc(2014, 1, 23) # this should be "now"
t1 = ts.utc(2014, 1, 24) # this should be "now + 24h"

t, events = satellite.find_events(user_location, t0, t1, altitude_degrees=10.0)
event_names = 'rise above 10°', 'culminate', 'set below 10°'
for ti, event in zip(t, events):
    name = event_names[event]
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
    if event == 2:
        break


# our first need is to find when satellites rise and set:
# https://rhodesmill.org/skyfield/earth-satellites.html#finding-when-a-satellite-rises-and-sets

# we might want to get the satellite's longitude and latitude to print it on some map :
# https://rhodesmill.org/skyfield/earth-satellites.html#satellite-longitude-latitude-and-height
# my API:

class SatPass(BaseModel):
    """describes the pass of one satellite."""
    t_start: object = None
    t_end: object = None
    trajectory:list[float] = []


def get_traj(t1, t2, satellite) -> list[list]:
    """returns 10 points of a trajectory for 1 satellite, from t1 to t2"""
    n_points = 10
    delta = (t2 - t1) / n_points
    points = []
    for i in range(n_points):
        geocentric = satellite.at(t1 + i*delta)
        lat, lon = wgs84.latlon_of(geocentric)
        points.append([lat.degrees, lon.degrees])
    return points

def get_passes(time, satellite) -> list[SatPass]:
    """returns all passes between time and (time+24h) for this satellite."""
    passes = []
    t, events = satellite.find_events(user_location, t0, t1, altitude_degrees=10.0)
    current_pass = SatPass()
    for ti, event in zip(t, events):
        print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
        if event == 0:
            current_pass = SatPass(t_start = ti)
        if event == 2:
            current_pass.t_end = ti
            current_pass.trajectory = get_traj(current_pass.t_start, current_pass.t_end, satellite)
            passes.append(current_pass)
    return passes

# get_traj(t0, t1, sats[0])
passes = get_passes(t1, sats[0])
print(passes[0])