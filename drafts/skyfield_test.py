import csv
from skyfield.api import load, EarthSatellite
import time

# Create a timescale and ask the current time.
ts = load.timescale()
t = ts.now()

# Load the JPL ephemeris DE421 (covers 1900-2050).
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']

# # What's the position of Mars, viewed from Earth?
# astrometric = earth.at(t).observe(mars)
# ra, dec, distance = astrometric.radec()

with load.open('stations.csv', mode="r") as f:
    data = list(csv.DictReader(f))

sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
print('Loaded', len(sats), 'satellites')


geocentric = sats[0].at(t)
print(geocentric.position.m)
for i in range(20):
    time.sleep(0.5)
    print(sats[0].at(ts.now()).position.m)
print(*sats, sep="\n")
