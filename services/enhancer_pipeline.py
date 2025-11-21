from agents.intent_agent import agent_intent
from agents.enhancer_agent import agent_enhancer
from agents.polisher_agent import agent_polisher
from agents.translator import agent_translator, agent_language_detector


def enhance_prompt(user_prompt: str, use_case: str) -> str:
    """
    Runs all three agents in sequence to generate an optimized prompt.
    """
    detected_language = agent_language_detector(user_prompt)
    translate = detected_language.lower() != 'english'
    if translate:
        user_prompt = agent_translator(user_prompt, target_language='english')

    step1 = agent_intent(user_prompt, use_case)
    step2 = agent_enhancer(step1, use_case)
    final = agent_polisher(step2, use_case)

    if(translate):
        final = agent_translator(final, target_language=detected_language)
    return final
