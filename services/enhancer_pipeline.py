from agents.intent_agent import agent_intent
from agents.enhancer_agent import agent_enhancer
from agents.polisher_agent import agent_polisher


def enhance_prompt(user_prompt: str, use_case: str) -> str:
    """
    Runs all three agents in sequence to generate an optimized prompt.
    """
    step1 = agent_intent(user_prompt, use_case)
    step2 = agent_enhancer(step1, use_case)
    final = agent_polisher(step2, use_case)
    return final
