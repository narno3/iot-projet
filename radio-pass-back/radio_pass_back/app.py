import asyncio
import threading
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from radio_pass_back.calculations import (
    SATELLITES,
    find_trajectory,
    update_all_sat_positions,
)
from radio_pass_back.models import SatelliteTrajectory

satellite_positions = [[0, 0] for _ in SATELLITES]


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Executed before and after the FASTAPI app is ran."""
    # Thread that periodically updates all satellite positions.
    update_positions_thread = threading.Thread(
        target=update_all_sat_positions, daemon=True, args=(satellite_positions,)
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
async def test() -> SatelliteTrajectory:
    t1 = datetime.now(tz=UTC)
    t2 = t1 + timedelta(hours=2)
    test_trajectory = find_trajectory(t1, t2, SATELLITES[0], 1200)
    return test_trajectory


@app.websocket("/ws")
async def get_all_sat_pos(ws: WebSocket):
    # await websocket.accept()
    # while True:
    #     await websocket.send_text(json.dumps(satellite_positions))
    #     await asyncio.sleep(1)
    await ws.accept()
    while True:
        # data = await websocket.receive_text()
        try:
            await ws.send_json(satellite_positions)
        except Exception as e:
            print(e)
            return
        await asyncio.sleep(0.5)
