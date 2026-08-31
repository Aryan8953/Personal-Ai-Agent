import json
import ollama

from registry import get_tool_descriptions


MODEL = "llama3.2:3b"


# ==========================================
# Helpers
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
# FIRST ROUTER
# ==========================================

def route_request(user_input):

    tools = get_tool_descriptions()

    prompt = f"""
You are the tool router for a personal desktop AI assistant.

Available tools:

{json.dumps(tools, indent=2)}

Decide whether the user's request requires a tool.

Rules:

1. Return ONLY JSON.
2. Never invent a tool.
3. Use only tools from the available tools list.
4. Ordinary knowledge questions must return NORMAL.
5. Questions about the user's screen must use inspect_screen.
6. Current, latest, recent, live, or internet information must use search_web.
7. Do not use computer tools for ordinary knowledge questions.
8. Do not execute tools yourself.

Examples:

"What is Python?"

{{"action":"NORMAL"}}

"What application am I using?"

{{"action":"TOOL","tool":"inspect_screen","arguments":{{"question":"What application is currently visible on the screen?"}}}}

"What is on my screen?"

{{"action":"TOOL","tool":"inspect_screen","arguments":{{"question":"What is currently visible on the screen?"}}}}

"What is the latest Python version?"

{{"action":"TOOL","tool":"search_web","arguments":{{"query":"latest Python version","max_results":5}}}}

"Open Notepad"

{{"action":"TOOL","tool":"launch_application","arguments":{{"application":"notepad"}}}}

"Open Google"

{{"action":"TOOL","tool":"open_website","arguments":{{"url":"https://www.google.com"}}}}

User request:
{user_input}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    decision = extract_json(
        response["message"]["content"].strip()
    )

    if not decision:
        return {
            "action": "NORMAL"
        }

    if decision.get("action") == "NORMAL":
        return {
            "action": "NORMAL"
        }

    if decision.get("action") != "TOOL":
        return {
            "action": "NORMAL"
        }

    tool_name = decision.get("tool")

    if tool_name not in tools:
        return {
            "action": "NORMAL"
        }

    arguments = decision.get(
        "arguments",
        {}
    )

    if not isinstance(arguments, dict):
        return {
            "action": "NORMAL"
        }

    return {
        "action": "TOOL",
        "tool": tool_name,
        "arguments": arguments
    }


# ==========================================
# NEXT ACTION
# ==========================================

def route_next_action(
    original_request,
    tool_name,
    arguments,
    result
):

    # ======================================
    # One-shot tools automatically finish
    # ======================================

    ONE_SHOT_TOOLS = {
        "launch_application",
        "open_website",
        "move_mouse",
        "click_mouse",
        "click_at",
        "type_text",
        "press_key",
    }

    if tool_name in ONE_SHOT_TOOLS:

        return {
            "action": "DONE",
            "response": f"Done. {result}"
        }

    # ======================================
    # Observation tools need AI interpretation
    # ======================================

    tools = get_tool_descriptions()

    prompt = f"""
You are controlling a personal desktop AI assistant.

The user requested:

{original_request}

A tool has just been executed.

Tool:
{tool_name}

Arguments:
{json.dumps(arguments, indent=2)}

Result:
{result}

Available tools:

{json.dumps(tools, indent=2)}

Decide what happens next.

Return ONLY JSON.

If the task is complete:

{{
    "action": "DONE",
    "response": "Short natural answer"
}}

If another tool is genuinely required:

{{
    "action": "TOOL",
    "tool": "tool_name",
    "arguments": {{}}
}}

Rules:

1. Never invent tools.
2. Only use available tools.
3. Do not repeat the tool that just succeeded.
4. Do not use computer tools unnecessarily.
5. If the task is complete, return DONE.
6. Do not explain your reasoning.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    decision = extract_json(
        response["message"]["content"].strip()
    )

    if not decision:

        return {
            "action": "DONE",
            "response": str(result)
        }

    if decision.get("action") == "DONE":

        return {
            "action": "DONE",
            "response": decision.get(
                "response",
                str(result)
            )
        }

    if decision.get("action") != "TOOL":

        return {
            "action": "DONE",
            "response": str(result)
        }

    next_tool = decision.get("tool")

    if next_tool not in tools:

        return {
            "action": "DONE",
            "response": str(result)
        }

    next_arguments = decision.get(
        "arguments",
        {}
    )

    if not isinstance(next_arguments, dict):

        return {
            "action": "DONE",
            "response": str(result)
        }

    return {
        "action": "TOOL",
        "tool": next_tool,
        "arguments": next_arguments
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("================================")
    print("       AI Tool Router")
    print("================================")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        result = route_request(question)

        print("\nRouter:")

        print(
            json.dumps(
                result,
                indent=2
            )
        )