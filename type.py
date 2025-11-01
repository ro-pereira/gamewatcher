from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class MatchData:
    date: str
    hour: Optional[str]
    event_name: Optional[str]
    team_1_name: str
    team_1_img: str
    team_2_name: str
    team_2_img: str
    channels: List[str]


@dataclass
class GameInfo:
    datetime_formatted: datetime
    championship: str
    team_1_id: int
    team_2_id: int
