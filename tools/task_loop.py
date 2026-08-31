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


# ==========================================
# Imports
# ==========================================

from brain import AIBrain

from ai_tool_router import route_request
from command_parser import parse_command
from tool_executor import execute_tool


MAX_STEPS = 5


# ==========================================
# Helpers
# ==========================================

def tool_result_failed(result):

    if not isinstance(result, str):
        return False

    failure_words = [
        "failed",
        "blocked",
        "can't",
        "cannot",
        "error",
        "unknown tool"
    ]

    result_lower = result.lower()

    return any(
        word in result_lower
        for word in failure_words
    )


# ==========================================
# Execute a validated plan
# ==========================================

def execute_plan(plan):

    if not plan:
        return []

    # ======================================
    # Validate complete plan BEFORE execution
    # ======================================

    required_fields = {
        "tool",
        "arguments"
    }

    for step in plan:

        if not isinstance(step, dict):

            print(
                "🛑 Invalid action detected."
            )

            return []

        if not required_fields.issubset(
            step.keys()
        ):

            print(
                "🛑 Incomplete action detected."
            )

            return []

        if not isinstance(
            step["arguments"],
            dict
        ):

            print(
                "🛑 Invalid arguments detected."
            )

            return []

    # ======================================
    # Execute actions
    # ======================================

    executed = []

    for index, step in enumerate(
        plan,
        start=1
    ):

        tool_name = step["tool"]

        arguments = step["arguments"]

        print(
            f"\n========== ACTION {index} =========="
        )

        print(
            f"🛠️ Tool: {tool_name}"
        )

        print(
            f"📦 Arguments: {arguments}"
        )

        # ==================================
        # Execute through safety layer
        # ==================================

        result = execute_tool(
            tool_name,
            arguments
        )

        print(
            f"💻 Result: {result}"
        )

        executed.append(
            {
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            }
        )

        # ==================================
        # Stop immediately on failure
        # ==================================

        if tool_result_failed(result):

            print(
                "🛑 Action failed. Stopping."
            )

            break

    return executed


# ==========================================
# Final answer for vision
# ==========================================

def answer_from_vision(
    brain,
    user_request,
    result
):

    prompt = f"""
The user asked:

{user_request}

Information obtained from the user's screen:

{result}

Answer the user's original question directly.

Rules:

- Use the screen information as evidence.
- Do not perform another computer action.
- Do not suggest launching an application.
- Do not mention internal tools.
- If the visual information is uncertain, say so.
"""

    return brain.chat(
        prompt
    )


# ==========================================
# Final answer for web search
# ==========================================

def answer_from_web(
    brain,
    user_request,
    result
):

    prompt = f"""
The user asked:

{user_request}

Internet search results:

{result}

Answer the user's original question using
the search results.

Rules:

- Do not perform another tool action.
- Do not mention internal tools.
- Do not invent unsupported information.
"""

    return brain.chat(
        prompt
    )


# ==========================================
# Main task runner
# ==========================================

def run_task(user_request):

    brain = AIBrain()

    # ======================================
    # STEP 1
    # Deterministic command parser
    # ======================================

    parsed_plan = parse_command(
        user_request
    )

    if parsed_plan:

        print(
            "\n🧩 Deterministic command detected."
        )

        results = execute_plan(
            parsed_plan
        )

        if not results:

            return (
                "I couldn't execute "
                "the requested task."
            )

        # Check last action
        last_result = results[-1]["result"]

        if tool_result_failed(
            last_result
        ):

            return str(last_result)

        return (
            f"Done. Executed "
            f"{len(results)} action(s)."
        )

    # ======================================
    # STEP 2
    # AI router
    # ======================================

    decision = route_request(
        user_request
    )

    print(
        "\n========== ROUTER =========="
    )

    print(
        decision
    )

    # ======================================
    # NORMAL
    # ======================================

    if decision.get(
        "action"
    ) == "NORMAL":

        return brain.chat(
            user_request
        )

    # ======================================
    # TOOL
    # ======================================

    tool_name = decision.get(
        "tool"
    )

    arguments = decision.get(
        "arguments",
        {}
    )

    if not tool_name:

        return (
            "I couldn't determine "
            "which action to perform."
        )

    print(
        f"\n🛠️ Tool: {tool_name}"
    )

    print(
        f"📦 Arguments: {arguments}"
    )

    # ======================================
    # Execute through safety layer
    # ======================================

    result = execute_tool(
        tool_name,
        arguments
    )

    print(
        f"💻 Result: {result}"
    )

    # ======================================
    # Check failure
    # ======================================

    if tool_result_failed(result):

        return str(result)

    # ======================================
    # Vision result
    # ======================================

    if tool_name == "inspect_screen":

        return answer_from_vision(
            brain,
            user_request,
            result
        )

    # ======================================
    # Web result
    # ======================================

    if tool_name == "search_web":

        return answer_from_web(
            brain,
            user_request,
            result
        )

    # ======================================
    # One-shot computer action
    # ======================================

    return str(result)


# ==========================================
# Main
# ==========================================

def main():

    print("================================")
    print("       Personal AI Agent")
    print("================================")

    print(
        "Controlled computer execution"
    )

    print(
        "Type 'exit' to quit."
    )

    while True:

        request = input(
            "\nTask: "
        ).strip()

        if request.lower() == "exit":

            print(
                "Goodbye!"
            )

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


# ==========================================
# Entry point
# ==========================================

if __name__ == "__main__":

    main()