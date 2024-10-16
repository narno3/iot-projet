import asyncio
import threading
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from radio_pass_back.calculations import (
    SATELLITES,
    SATELLITES_INFO,
    find_trajectory,
    find_all_passes,
    update_all_sat_positions,
)
from radio_pass_back.models import SatelliteTrajectory

SATELLITE_POSITIONS = [[0, 0] for _ in SATELLITES]


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Executed before and after the FASTAPI app is ran."""
    # Thread that periodically updates all satellite positions.
    update_positions_thread = threading.Thread(
        target=update_all_sat_positions, daemon=True, args=(SATELLITE_POSITIONS,)
    )
    update_positions_thread.start()
    yield


app = FastAPI(lifespan=app_lifespan)

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
async def get_sat_traj(sat: int) -> SatelliteTrajectory:
    """Endpoint to return the trajectory for 1 satellite."""
    t1 = datetime.now(tz=UTC)
    t2 = t1 + timedelta(hours=3)
    test_trajectory = find_trajectory(t1, t2, SATELLITES[sat], 1000)
    return test_trajectory


@app.get("/sat_infos")
async def get_sat_infos() -> list:
    """Satellite infos."""
    return SATELLITES_INFO


@app.get("/passes")
async def get_passes(lat: float, long: float) -> list:
    """Return next passes for this position."""
    return find_all_passes((lat, long))


@app.websocket("/positions")
async def get_all_sat_pos(ws: WebSocket):
    """Continuously returns all satellite positions."""
    await ws.accept()
    while True:
        # data = await websocket.receive_text()
        try:
            await ws.send_json(SATELLITE_POSITIONS)
        except Exception as e:
            print(e)
            return
        await asyncio.sleep(0.5)
