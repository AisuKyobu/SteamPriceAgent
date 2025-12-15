from graph.state import SteamPriceState
from tools.itad_search import search_games


def search_candidates(state: SteamPriceState):
    entity = state["game_entity"]

    if not entity or entity.confidence <= 0.2:
        return {"candidates": []}

    candidates = search_games(entity.game_name)
    return {"candidates": candidates}
