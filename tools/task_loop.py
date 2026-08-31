import sys
from pathlib import Path


# ==========================================
# Project paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"
TOOLS_PATH = PROJECT_ROOT / "tools"

sys.path.insert(0, str(PHASE_01_PATH))
sys.path.insert(0, str(TOOLS_PATH))


from brain import AIBrain

from ai_tool_router import route_request
from tool_executor import execute_tool


MAX_STEPS = 5


# ==========================================
# Convert tool result into final answer
# ==========================================

def create_final_answer(
    brain,
    user_request,
    tool_name,
    result
):

    if tool_name == "inspect_screen":

        prompt = f"""
The user asked:

{user_request}

Information obtained from the user's screen:

{result}

Answer the user's original question directly.

Important:
- Use the screen information as evidence.
- Do not perform another action.
- Do not suggest opening or launching anything.
- Do not mention internal tools.
- If the screen information is uncertain, say so.
"""

    elif tool_name == "search_web":

        prompt = f"""
The user asked:

{user_request}

Internet search results:

{result}

Answer the user's original question using the
search results.

Important:
- Do not perform another tool action.
- Do not mention internal tools.
- Do not invent unsupported information.
"""

    else:

        return str(result)

    return brain.chat(prompt)


# ==========================================
# Run task
# ==========================================

def run_task(user_request):

    brain = AIBrain()

    decision = route_request(
        user_request
    )

    print("\n========== STEP 1 ==========")

    print("Decision:")
    print(decision)

    # ======================================
    # Normal question
    # ======================================

    if decision.get("action") == "NORMAL":

        return brain.chat(
            user_request
        )

    executed_actions = set()

    current_decision = decision

    # ======================================
    # Controlled tool loop
    # ======================================

    for step in range(1, MAX_STEPS + 1):

        if step > 1:

            print(
                f"\n========== STEP {step} =========="
            )

            print(
                "Decision:"
            )

            print(
                current_decision
            )

        if current_decision.get("action") != "TOOL":

            return current_decision.get(
                "response",
                "Task completed."
            )

        tool_name = current_decision.get(
            "tool"
        )

        arguments = current_decision.get(
            "arguments",
            {}
        )

        print(
            f"🛠️ Tool: {tool_name}"
        )

        print(
            f"📦 Arguments: {arguments}"
        )

        # ==================================
        # Prevent duplicate actions
        # ==================================

        action_key = (
            tool_name,
            str(arguments)
        )

        if action_key in executed_actions:

            print(
                "🛑 Duplicate action blocked."
            )

            return (
                "I stopped because the same "
                "action was requested again."
            )

        executed_actions.add(
            action_key
        )

        # ==================================
        # Execute safely
        # ==================================

        result = execute_tool(
            tool_name,
            arguments
        )

        print(
            f"💻 Result: {result}"
        )

        # ==================================
        # Vision
        # ==================================

        if tool_name == "inspect_screen":

            return create_final_answer(
                brain,
                user_request,
                tool_name,
                result
            )

        # ==================================
        # Web search
        # ==================================

        if tool_name == "search_web":

            return create_final_answer(
                brain,
                user_request,
                tool_name,
                result
            )

        # ==================================
        # One-shot computer actions
        # ==================================

        if tool_name in {
            "launch_application",
            "open_website",
            "move_mouse",
            "click_mouse",
            "click_at",
            "type_text",
            "press_key"
        }:

            return str(result)

        # ==================================
        # Unknown tool
        # ==================================

        return str(result)

    return (
        "The task reached the maximum "
        "number of allowed steps."
    )


# ==========================================
# Main
# ==========================================

def main():

    print("================================")
    print("       Multi-Step Agent")
    print("================================")

    print(
        "Controlled tool execution"
    )

    print(
        "Maximum steps:",
        MAX_STEPS
    )

    print(
        "Type 'exit' to quit."
    )

    while True:

        request = input(
            "\nTask: "
        ).strip()

        if request.lower() == "exit":

            print("Goodbye!")

            break

        if not request:
            continue

        try:

            response = run_task(
                request
            )

            print(
                "\n🤖 AI:"
            )

            print(
                response
            )

        except Exception as error:

            print(
                f"\n❌ Error: {error}"
            )


if __name__ == "__main__":

    main()