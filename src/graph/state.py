from typing import TypedDict, List, Optional

from schemas.game_entity import GameEntity
from schemas.candidate_selection import CandidateSelection
from schemas.price_result import PriceInfo


class SteamPriceState(TypedDict):
    user_query: str

    game_entity: Optional[GameEntity]
    candidates: List[dict]

    selection: Optional[CandidateSelection]
    price_infos: List[PriceInfo]

    result: Optional[str]
