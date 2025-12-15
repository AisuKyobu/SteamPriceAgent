from agent.entity_resolver import GameEntityResolver
from langchain_deepseek import ChatDeepSeek

def main():
    llm = ChatDeepSeek(model="deepseek-chat", temperature=0.2)
    resolver = GameEntityResolver(llm)
    user_input = input("请输入你想查询的游戏： ")
    entity = resolver.resolve(user_input)

    print("识别结果：")
    print(entity.model_dump())


if __name__ == "__main__":
    main()
