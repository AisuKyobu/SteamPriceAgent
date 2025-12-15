from graph.steam_price_graph import build_graph

from utils.logger import setup_logging,get_logger

logger = get_logger(__name__)


def main():
    setup_logging()
    user_query = input("请输入你想查询的游戏： ")
    graph = build_graph()
    graph.invoke({"user_query": user_query})

if __name__ == "__main__":
    main()

    