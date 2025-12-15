from langchain_deepseek import ChatDeepSeek

from agent.game_entity_resolver import GameEntityResolver
from agent.decision import PurchaseDecisionAgent
from schemas.price_result import PriceInfo

def main():
    llm = ChatDeepSeek(model="deepseek-chat", temperature=0.2)
    
    resolver = GameEntityResolver(llm)
    decision_agent = PurchaseDecisionAgent(llm)
    
    user_input = input("请输入你想查询的游戏： ")
    entity = resolver.resolve(user_input)

    price_info = PriceInfo(
        current_price=198,
        historical_low=168,
        discount_percent=50,
        store="Steam",
    )

    decision = decision_agent.decide(price_info)

    print("购买建议：")
    print(decision)


if __name__ == "__main__":
    main()
