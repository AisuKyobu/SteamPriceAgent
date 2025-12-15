from graph.state import SteamPriceState

def resolve_entity(state: SteamPriceState, agents):
    entity = agents["resolver"].resolve(state["user_query"])
    return {"game_entity": entity}
