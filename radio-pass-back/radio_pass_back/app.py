from datetime import UTC, datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from radio_pass_back.calculations import SATELLITES, find_trajectory
from radio_pass_back.models import SatelliteTrajectory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # List of allowed origins, change this to match your frontend's URL
    allow_credentials=True,  # To allow cookies and other credentials
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/get_trajectory")
def test() -> SatelliteTrajectory:
    t1 = datetime.now(tz=UTC)
    t2 = t1 + timedelta(hours=24)
    test_trajectory = find_trajectory(t1, t2, SATELLITES[0], 1200)
    return test_trajectory
