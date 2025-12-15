from langgraph.graph import StateGraph, END

from graph.state import SteamPriceState
from graph.nodes.resolve_entity import resolve_entity
from graph.nodes.search_games import search_candidates
from graph.nodes.select_candidate import select_candidates
from graph.nodes.fetch_price import fetch_prices
from graph.nodes.decide import make_decision

from agent.factory import create_agents


def has_candidates(state: SteamPriceState):
    return "select" if state["candidates"] else "end"


def has_selection(state: SteamPriceState):
    return "price" if state["selection"] and state["selection"].selected_ids else "end"


def build_graph():
    agents = create_agents()

    graph = StateGraph(SteamPriceState)

    graph.add_node("resolve", lambda s: resolve_entity(s, agents))
    graph.add_node("search", search_candidates)
    graph.add_node("select", lambda s: select_candidates(s, agents))
    graph.add_node("price", fetch_prices)
    graph.add_node("decide", lambda s: make_decision(s, agents))

    graph.set_entry_point("resolve")

    graph.add_edge("resolve", "search")

    graph.add_conditional_edges("search", has_candidates, {
        "select": "select",
        "end": END
    })

    graph.add_conditional_edges("select", has_selection, {
        "price": "price",
        "end": END
    })

    graph.add_edge("price", "decide")
    graph.add_edge("decide", END)

    return graph.compile()
