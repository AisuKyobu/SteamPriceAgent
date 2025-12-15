from graph.state import SteamPriceState
from tools.itad_price import game_price


def fetch_prices(state: SteamPriceState):
    selection = state["selection"]

    if not selection or not selection.selected_ids:
        return {"price_infos": []}

    prices = game_price(selection.selected_ids)
    return {"price_infos": prices}
