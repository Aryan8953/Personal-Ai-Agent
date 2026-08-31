from ai_tool_router import route_request
from tool_executor import execute_tool


def handle_request(user_input):

    decision = route_request(user_input)

    print(f"\n🧠 Decision: {decision}")

    if decision.get("action") != "TOOL":
        return None

    tool_name = decision.get("tool")
    arguments = decision.get("arguments", {})

    print(f"🛠️ Tool: {tool_name}")
    print(f"📦 Arguments: {arguments}")

    result = execute_tool(
        tool_name,
        arguments
    )

    return result


def main():

    print("================================")
    print("       AI Computer Agent")
    print("================================")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break

        result = handle_request(user_input)

        if result:
            print(f"\n💻 Result: {result}")

        else:
            print("\n💬 No computer action required.")


if __name__ == "__main__":
    main()