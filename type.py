from typing import TypedDict, List, Optional

class MatchData(TypedDict):
    date: str
    hour: Optional[str]
    event_name: Optional[str]
    team_1_name: str
    team_1_img: str
    team_2_name: str
    team_2_img: str
    channels: List[str]