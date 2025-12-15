from graph.state import SteamPriceState


def select_candidates(state: SteamPriceState, agents):
    selection = agents["selector"].select(
        state["user_query"],
        state["candidates"]
    )
    return {"selection": selection}
