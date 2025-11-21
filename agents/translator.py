from services.aoai_client import call_agent

language='english'

def agent_translator(input_text: str, target_language: str = 'english') -> str:
    system = f"""
    You are a Language Translation Agent.

    Your task:
    - Translate the given text into {target_language}.
    - Maintain the original meaning and context.
    - Ensure the translation is natural and fluent.
    - Avoid literal translations that may sound awkward.

    Output:
    - Only the translated text.
    - No additional commentary or notes.
    """

    return call_agent(system, input_text)

def agent_language_detector(input_text: str) -> str:
    system = """
    You are a Language Detection Agent.

    Your task:
    - Identify the language of the given text.
    - Provide the name of the language only.

    Output:
    - Only the name of the detected language.
    - No additional commentary or notes.
    """

    return call_agent(system, input_text)