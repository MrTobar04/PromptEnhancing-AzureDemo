from services.aoai_client import call_agent


def agent_polisher(enhanced_prompt: str, use_case: str) -> str:
    system = f"""
    You are the Final Prompt Polisher Agent.

    Your job:
    - Ensure the output is ONLY the enhanced prompt.
    - Remove any analysis, commentary, or meta-text.
    - Fix clarity and tighten instructions.
    - Enforce that the prompt must instruct the AI, not perform the task.
    - Ensure it is optimized for the use case: **{use_case}**.

    Output:
    - Only the final enhanced prompt.
    - No bullet points.
    - No labels.
    - No notes.
    """

    return call_agent(system, enhanced_prompt)
