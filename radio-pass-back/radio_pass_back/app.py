from datetime import UTC, datetime, timedelta

from fastapi import FastAPI

from radio_pass_back.calculations import SATELLITES, find_trajectory
from radio_pass_back.models import SatelliteTrajectory

app = FastAPI()


@app.get("/get_trajectory")
def test() -> SatelliteTrajectory:
    t1 = datetime.now(tz=UTC)
    t2 = t1 + timedelta(days=1)
    test_trajectory = find_trajectory(t1, t2, SATELLITES[0])
    return test_trajectory
