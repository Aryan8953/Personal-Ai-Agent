import sys
from pathlib import Path

# Make project modules available
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"

sys.path.insert(0, str(PHASE_01_PATH))
sys.path.insert(0, str(Path(__file__).resolve().parent))


from brain import AIBrain

from ai_tool_router import route_request
from tool_executor import execute_tool


def handle_request(user_input, brain):

    decision = route_request(user_input)

    print(f"\n🧠 Decision: {decision}")

    if decision.get("action") != "TOOL":

        return brain.chat(user_input)

    tool_name = decision.get("tool")

    arguments = decision.get(
        "arguments",
        {}
    )

    print(f"🛠️ Tool: {tool_name}")
    print(f"📦 Arguments: {arguments}")

    result = execute_tool(
        tool_name,
        arguments
    )

    print(f"\n💻 Tool result:\n{result}")

    # ==============================
    # Search → AI
    # ==============================

    if tool_name == "search_web":

        prompt = f"""
The user asked:

{user_input}

Internet search results:

{result}

Answer the user's question naturally.

Rules:

- Use the search results as your source of current information.
- Do not invent facts that are not supported by the results.
- Prefer the most relevant results.
- If the results are insufficient, say that clearly.
- Do not mention internal tools or the search process unless asked.
- Keep the answer concise.
"""

        return brain.chat(prompt)

    # ==============================
    # Vision → AI
    # ==============================

    if tool_name == "inspect_screen":

        prompt = f"""
The user asked:

{user_input}

Information obtained from the user's current screen:

{result}

Answer the user's question naturally and directly.

Do not mention internal tools, screenshots,
or model names unless the user specifically asks.
"""

        return brain.chat(prompt)

    # ==============================
    # Other tools
    # ==============================

    return result


def main():

    brain = AIBrain()

    print("================================")
    print("       Personal AI Agent")
    print("================================")
    print("AI + Vision + Web + Computer")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":

            print("Goodbye!")

            break

        try:

            response = handle_request(
                user_input,
                brain
            )

            if response:

                print(f"\nAI: {response}")

            else:

                print("\nAI: No response.")

        except Exception as error:

            print(
                f"\n❌ Error: {error}"
            )


if __name__ == "__main__":

    main()