import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI client
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_OPENAI_API_KEY"]),
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Agent call function
def call_agent(system_prompt, user_message):
    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_message),
        ],
        model=deployment_name,
    )

    print("Agent Response:", response.choices[0].message["content"])
    return response.choices[0].message["content"]


# -------------------------
# Agent 1: Intent Clarifier
# -------------------------
def agent_intent(user_prompt, use_case):
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


# -------------------------
# Agent 2: Prompt Enhancer (Your original logic)
# -------------------------
def agent_enhancer(structured_input, use_case):
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


# -------------------------
# Agent 3: Final Polisher
# -------------------------
def agent_polisher(enhanced_prompt, use_case):
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

def enhance_prompt(user_prompt, use_case):
    """
    Sends the user prompt to Azure OpenAI and returns an enhanced version.
    The enhancement changes depending on the selected use case.
    """

    step1 = agent_intent(user_prompt, use_case)
    step2 = agent_enhancer(step1, use_case)
    final = agent_polisher(step2, use_case)
    return final


# --------------------------
#        GRADIO UI
# --------------------------

custom_css = """
#small-submit-btn, #back-btn {
    padding: 4px 10px !important;
    font-size: 12px !important;
    border-radius: 6px !important;
    height: 28px !important;
}

.label-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: -8px;
}

footer {visibility: hidden}
"""

# --- Backend helpers for UI state ---

def enhance_and_replace(prompt, use_case, stored_original, is_enhanced):
    """Enhance prompt and replace text in-place; store original if needed."""
    # Only store original if this is the first enhancement
    if not is_enhanced:
        stored_original = prompt

    enhanced = enhance_prompt(prompt, use_case)
    return enhanced, stored_original, True, gr.Button(visible=True)


def go_back(stored_original):
    """Return to the original prompt."""
    return stored_original, False, gr.Button(visible=False)


with gr.Blocks(css=custom_css) as app:
    gr.Markdown(
        """
        # ✨ Prompt Enhancer  
        Improve your prompts automatically using GPT-4o via Azure OpenAI.
        """
    )

    with gr.Row():
        use_case_dropdown = gr.Dropdown(
            label="Choose Use Case",
            choices=[
                "ChatGPT",
                "GitHub Copilot",
                "Microsoft Copilot",
                "DeepSeek",
                "Grok (xAI)",
                "Stable Diffusion",
                "Image Generation (generic)",
                "Code Generation",
                "Data Analysis",
                "General Purpose"
            ],
            value="ChatGPT",
            interactive=True
        )

    # -------- Label + Buttons Row --------
    with gr.Row(elem_classes=["label-row"]):
        gr.Markdown("**Enter your prompt**")
        enhance_btn = gr.Button("Enhance ⋆˙⟡", elem_id="small-submit-btn", variant="secondary")
        back_btn = gr.Button("Back ↩", elem_id="back-btn", variant="secondary", visible=False)

    # Single textbox
    input_box = gr.Textbox(
        label="",
        placeholder="Write the prompt you want to enhance...",
        lines=4
    )

    # Hidden state variables
    stored_original = gr.State("")
    is_enhanced = gr.State(False)

    # --- Enhance button → modifies input in place ---
    enhance_btn.click(
        fn=enhance_and_replace,
        inputs=[input_box, use_case_dropdown, stored_original, is_enhanced],
        outputs=[input_box, stored_original, is_enhanced, back_btn]
    )

    # --- Back button → restore original ---
    back_btn.click(
        fn=go_back,
        inputs=[stored_original],
        outputs=[input_box, is_enhanced, back_btn]
    )

app.queue().launch()