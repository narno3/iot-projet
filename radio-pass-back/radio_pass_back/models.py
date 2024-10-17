from pydantic import BaseModel


class SatelliteTrajectory(BaseModel):
    """Data class for satellite data."""

    name: str = "unknown"
    points: list[list] = []
