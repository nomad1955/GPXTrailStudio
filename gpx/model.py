from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TrackPoint:
    """GPX Track Point"""

    lat: float
    lon: float

    ele_original: Optional[float] = None
    ele_corrected: Optional[float] = None

    time: Optional[str] = None

    extensions: dict = field(default_factory=dict)

    @property
    def elevation(self):
        """
        현재 사용하는 고도
        """
        if self.ele_corrected is not None:
            return self.ele_corrected
        return self.ele_original


@dataclass
class TrackSegment:
    points: List[TrackPoint] = field(default_factory=list)


@dataclass
class Track:
    name: str = ""
    segments: List[TrackSegment] = field(default_factory=list)


@dataclass
class GPXDocument:
    creator: str = ""
    version: str = "1.1"

    tracks: List[Track] = field(default_factory=list)