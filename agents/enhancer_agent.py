from services.aoai_client import call_agent


def agent_enhancer(structured_input: str, use_case: str) -> str:
    system = f"""
    You are a Prompt Enhancement Agent.

    Your task:
    - Rewrite the structured intent into a single enhanced prompt.
    - The goal is to instruct an AI model for the use case: **{use_case}**.
    - You must NOT produce the final output the user is asking for.
    - Do NOT write a story, code, or analysis.
    - You must output ONLY an improved prompt that tells the AI what to do.

    Improve:
    - clarity
    - structure
    - precision
    - usefulness for the selected AI model or service

    ABSOLUTE RULES:
    - You MUST produce a prompt, not the answer.
    - No storytelling.
    - No fulfilling the task.
    """

    return call_agent(system, structured_input)
