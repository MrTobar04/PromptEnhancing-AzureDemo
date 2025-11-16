from services.aoai_client import call_agent


def agent_intent(user_prompt: str, use_case: str) -> str:
    system = f"""
    You are an Intent Clarification Agent.

    Your task:
    - Rewrite the user's prompt into a short, structured summary.
    - Identify only the essential goal and relevant constraints.
    - Keep it extremely brief (maximum 4 lines).
    - No storytelling, no creativity, no speculation.
    - No asking for missing details.
    - Do NOT propose plot, characters, tone, length, or stylistic elements.

    Focus must be aligned to use case: **{use_case}**.

    Output format (exactly):
    GOAL: <one sentence>
    CONTEXT: <one sentence of relevant context if present>
    CORE REQUEST: <short restatement of what the user wants>
    """

    return call_agent(system, user_prompt)
