import json
import ollama

from registry import get_tool_descriptions


def route_request(user_input):

    tools = get_tool_descriptions()

    prompt = f"""
You are the tool router for a personal desktop AI assistant.

Available tools:

{json.dumps(tools, indent=2)}

Your job is ONLY to decide whether the user's request needs
a computer tool.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Never invent a tool.
3. Only use tools from the Available tools list.
4. Ordinary questions must return NORMAL.
5. Questions about what is visible on the screen should use
   inspect_screen.
6. inspect_screen requires a "question" argument.
7. Do NOT use click_at unless the user explicitly asks to click
   a specific location or target.
8. Do not execute any tools yourself.

For a normal conversational question:

{{
    "action": "NORMAL"
}}

For a computer action:

{{
    "action": "TOOL",
    "tool": "tool_name",
    "arguments": {{
        "argument": "value"
    }}
}}

Examples:

User:
"What application am I using?"

Return:

{{
    "action": "TOOL",
    "tool": "inspect_screen",
    "arguments": {{
        "question": "What application is currently visible on the screen?"
    }}
}}

User:
"What is on my screen?"

Return:

{{
    "action": "TOOL",
    "tool": "inspect_screen",
    "arguments": {{
        "question": "What is currently visible on the screen?"
    }}
}}

User:
"What is Python?"

Return:

{{
    "action": "NORMAL"
}}

User request:
{user_input}
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"].strip()

    try:

        decision = json.loads(result)

    except json.JSONDecodeError:

        return {
            "action": "NORMAL"
        }

    # ==============================
    # Validate router output
    # ==============================

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


if __name__ == "__main__":

    print("================================")
    print("       AI Tool Router")
    print("================================")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        result = route_request(question)

        print("\nRouter:")

        print(
            json.dumps(
                result,
                indent=2
            )
        )