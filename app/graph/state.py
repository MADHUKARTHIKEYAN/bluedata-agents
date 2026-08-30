from typing import TypedDict


class AgentState(TypedDict):
    user_input: str
    intent: str
    response: str