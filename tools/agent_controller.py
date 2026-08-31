import json
import sys
from pathlib import Path


# ==========================================
# Paths
# ==========================================

TOOLS_PATH = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_PATH.parent

PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"
LLM_PATH = TOOLS_PATH / "llm"

sys.path.insert(0, str(PHASE_01_PATH))
sys.path.insert(0, str(LLM_PATH))
sys.path.insert(0, str(TOOLS_PATH))


# ==========================================
# Imports
# ==========================================

from brain import AIBrain

from ai_tool_router import route_request
from command_parser import parse_command

from factory import get_llm

from registry import get_tool_descriptions
from tool_executor import execute_tool


MAX_STEPS = 5


# ==========================================
# Models
# ==========================================

brain = AIBrain()

llm = get_llm()


# ==========================================
# JSON extraction
# ==========================================

def extract_json(text):

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    try:

        return json.loads(
            text[start:end + 1]
        )

    except json.JSONDecodeError:

        return None


# ==========================================
# Normal request
# ==========================================

def handle_normal_request(
    user_request
):

    return brain.chat(
        user_request
    )


# ==========================================
# Decide next action
# ==========================================

def decide_next_action(
    user_request,
    history
):

    tools = get_tool_descriptions()

    prompt = f"""
You are the decision controller for a
personal desktop AI assistant.

USER REQUEST:

{user_request}

PREVIOUS ACTIONS AND RESULTS:

{json.dumps(history, indent=2)}

AVAILABLE TOOLS:

{json.dumps(tools, indent=2)}

Choose ONLY the next action.

If the task is complete:

{{
    "action": "DONE",
    "response": "Short natural response"
}}

If a tool is required:

{{
    "action": "TOOL",
    "tool": "tool_name",
    "arguments": {{
        "argument": "value"
    }}
}}

RULES:

1. Return ONLY valid JSON.
2. Use only tools from AVAILABLE TOOLS.
3. Choose only ONE tool at a time.
4. Never execute tools yourself.
5. Wait for the result before deciding again.
6. Never repeat a successful action.
7. If a tool successfully completed the
   user's request, return DONE.
8. Do not use tools for ordinary knowledge.
9. Use inspect_screen for screen questions.
10. Use search_web for current information.
11. Do not invent tools.
12. Do not explain reasoning.

Examples:

User request:
Open Notepad

After:
launch_application("notepad")

Return:

{{
    "action": "DONE",
    "response": "Notepad is open."
}}

User request:
Open Notepad and type Hello

After Notepad is opened:

{{
    "action": "TOOL",
    "tool": "type_text",
    "arguments": {{
        "text": "Hello"
    }}
}}

After successful typing:

{{
    "action": "DONE",
    "response": "Done."
}}
"""

    response = llm.chat([
        {
            "role": "system",
            "content": "Return ONLY valid JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ])

    decision = extract_json(
        response.strip()
    )

    if not decision:

        return {
            "action": "DONE",
            "response":
                "I could not determine the next action."
        }

    if decision.get(
        "action"
    ) == "DONE":

        return {
            "action": "DONE",
            "response": decision.get(
                "response",
                "Task completed."
            )
        }

    if decision.get(
        "action"
    ) != "TOOL":

        return {
            "action": "DONE",
            "response":
                "Task completed."
        }

    tool_name = decision.get(
        "tool"
    )

    if tool_name not in tools:

        return {
            "action": "DONE",
            "response":
                "The selected tool is unavailable."
        }

    arguments = decision.get(
        "arguments",
        {}
    )

    if not isinstance(
        arguments,
        dict
    ):

        return {
            "action": "DONE",
            "response":
                "Invalid tool arguments."
        }

    return {
        "action": "TOOL",
        "tool": tool_name,
        "arguments": arguments
    }


# ==========================================
# Agent
# ==========================================

def run_agent(user_request):

    # ======================================
    # STEP 0
    # FAST PARSER
    # ======================================

    parsed_plan = parse_command(
        user_request
    )

    if parsed_plan:

        print(
            "\n========== FAST PATH =========="
        )

        print(
            json.dumps(
                parsed_plan,
                indent=2
            )
        )

        results = []

        for index, step in enumerate(
            parsed_plan,
            start=1
        ):

            tool_name = step["tool"]

            arguments = step["arguments"]

            print(
                f"\n========== FAST ACTION {index} =========="
            )

            print(
                f"🛠️ Tool: {tool_name}"
            )

            print(
                f"📦 Arguments: {arguments}"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            print(
                f"💻 Result: {result}"
            )

            results.append(
                result
            )

            result_text = str(
                result
            ).lower()

            if any(
                word in result_text
                for word in [
                    "blocked:",
                    "unknown tool:",
                    "tool execution failed:",
                    "can't launch"
                ]
            ):

                return str(result)

        return (
            f"Done. Executed "
            f"{len(results)} action(s)."
        )

    # ======================================
    # STEP 1
    # AI ROUTER
    # ======================================

    router_decision = route_request(
        user_request
    )

    print(
        "\n========== ROUTER =========="
    )

    print(
        json.dumps(
            router_decision,
            indent=2
        )
    )

    # ======================================
    # NORMAL
    # ======================================

    if router_decision.get(
        "action"
    ) == "NORMAL":

        print(
            "\n🧠 Normal conversation."
        )

        return handle_normal_request(
            user_request
        )

    # ======================================
    # TOOL
    # ======================================

    first_tool = router_decision.get(
        "tool"
    )

    first_arguments = router_decision.get(
        "arguments",
        {}
    )

    if not first_tool:

        return (
            "I couldn't determine "
            "what action to perform."
        )

    history = []

    executed_actions = set()

    # ======================================
    # AGENT LOOP
    # ======================================

    for step in range(
        1,
        MAX_STEPS + 1
    ):

        print(
            f"\n========== AGENT STEP {step} =========="
        )

        # ==================================
        # FIRST ACTION
        # ==================================

        if step == 1:

            decision = {
                "action": "TOOL",
                "tool": first_tool,
                "arguments": first_arguments
            }

        else:

            decision = decide_next_action(
                user_request,
                history
            )

        print(
            "\nDecision:"
        )

        print(
            json.dumps(
                decision,
                indent=2
            )
        )

        # ==================================
        # DONE
        # ==================================

        if decision.get(
            "action"
        ) == "DONE":

            return decision.get(
                "response",
                "Task completed."
            )

        # ==================================
        # TOOL
        # ==================================

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
                "the next tool."
            )

        # ==================================
        # Duplicate protection
        # ==================================

        action_key = (
            tool_name,
            json.dumps(
                arguments,
                sort_keys=True
            )
        )

        if action_key in executed_actions:

            return (
                "I stopped because the same "
                "successful action was requested "
                "again."
            )

        executed_actions.add(
            action_key
        )

        # ==================================
        # Execute
        # ==================================

        print(
            f"\n🛠️ Executing: {tool_name}"
        )

        print(
            f"📦 Arguments: {arguments}"
        )

        result = execute_tool(
            tool_name,
            arguments
        )

        print(
            f"💻 Result: {result}"
        )

        # ==================================
        # Save result
        # ==================================

        history.append({

            "step": step,

            "tool": tool_name,

            "arguments": arguments,

            "result": str(result)

        })

        # ==================================
        # Failure
        # ==================================

        result_text = str(
            result
        ).lower()

        if any(
            word in result_text
            for word in [
                "blocked:",
                "unknown tool:",
                "tool execution failed:",
                "can't launch"
            ]
        ):

            return str(result)

    return (
        "The task reached the maximum "
        "number of agent steps."
    )


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    print(
        "================================"
    )

    print(
        "       Agent Controller"
    )

    print(
        "================================"
    )

    print(
        "Fast Parser + Router + Agent"
    )

    print(
        "LLM provider: Ollama"
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

            break

        if not request:

            continue

        try:

            result = run_agent(
                request
            )

            print(
                "\n🤖 Agent:"
            )

            print(
                result
            )

        except Exception as error:

            print(
                f"\n❌ Error: {error}"
            )