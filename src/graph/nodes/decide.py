from graph.state import SteamPriceState


def make_decision(state: SteamPriceState, agents):
    if not state["price_infos"]:
        return {"result": "暂无价格信息"}

    result = agents["decision"].decide(state["price_infos"])
    return {"result": result}
