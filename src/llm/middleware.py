import json
import uuid
from typing import Any

from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain_core.messages import AIMessage


def parse_text_tool_call(text: str, tool_names: set[str]) -> dict[str, Any] | None:
    """Return {"name", "args"} if the text is a tool call written as JSON, otherwise None."""
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or data.get("name") not in tool_names:
        return None
    args = data.get("arguments", data.get("parameters", {}))
    if not isinstance(args, dict):
        return None
    return {"name": data["name"], "args": args}


@wrap_model_call
def fix_text_tool_calls(request: ModelRequest, handler) -> ModelResponse:
    """Small models sometimes write a tool call as JSON text instead of calling the tool. Turn it into a real tool call."""
    response = handler(request)
    tool_names = {tool.name for tool in request.tools if hasattr(tool, "name")}
    fixed = []
    for message in response.result:
        if isinstance(message, AIMessage) and not message.tool_calls and isinstance(message.content, str):
            tool_call = parse_text_tool_call(message.content, tool_names)
            if tool_call:
                message = AIMessage(
                    content="",
                    id=message.id,
                    tool_calls=[{**tool_call, "id": f"call_{uuid.uuid4().hex}", "type": "tool_call"}],
                )
        fixed.append(message)
    return ModelResponse(result=fixed, structured_response=response.structured_response)
