from ai_tool_router import route_request
from tool_executor import execute_tool


def handle_request(user_input):

    decision = route_request(user_input)

    print("\nRouter decision:")
    print(decision)

    if decision.get("action") == "TOOL":

        tool_name = decision.get("tool")
        arguments = decision.get("arguments", {})

        print(f"\n🛠️ Executing: {tool_name}")

        result = execute_tool(
            tool_name,
            arguments
        )

        return result

    return None


if __name__ == "__main__":

    print("================================")
    print("       Agent Tool System")
    print("================================")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        result = handle_request(question)

        if result:
            print(f"\nResult: {result}")

        else:
            print("\nNo tool required.")