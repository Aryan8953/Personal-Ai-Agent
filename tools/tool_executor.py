import json

from registry import get_tool
from safety import validate_tool_call


def execute_tool(tool_name, arguments):

    # Convert JSON string to dictionary first
    if isinstance(arguments, str):

        try:
            arguments = json.loads(arguments)

        except json.JSONDecodeError:
            return "Blocked: Invalid JSON arguments."

    # SAFETY CHECK MUST HAPPEN BEFORE THE TOOL IS EXECUTED
    allowed, message = validate_tool_call(
        tool_name,
        arguments
    )

    if not allowed:
        return f"Blocked: {message}"

    # Find the tool
    tool = get_tool(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    # Execute
    try:

        result = tool(**arguments)

        return result

    except Exception as error:

        return f"Tool execution failed: {error}"