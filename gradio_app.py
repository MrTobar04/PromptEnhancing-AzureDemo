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

def enhance_prompt(user_prompt, use_case):
    """
    Sends the user prompt to Azure OpenAI and returns an enhanced version.
    The enhancement changes depending on the selected use case.
    """

    system_instruction = f"""
    You are a professional prompt-enhancing assistant.
    Your task is to rewrite and enhance the user's prompt specifically for the selected use case: **{use_case}**.

    Improve:
    - clarity
    - structure
    - creativity
    - precision
    - usefulness for the selected AI model or service

    Output ONLY the enhanced prompt — no explanations, no notes, no formatting outside the prompt.
    """

    response = client.complete(
        messages=[
            SystemMessage(content=system_instruction),
            UserMessage(content=user_prompt),
        ],
        model=deployment_name,
    )

    return response.choices[0].message.content


# --------------------------
#        GRADIO UI
# --------------------------

with gr.Blocks(css="footer {visibility: hidden}") as app:
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

    with gr.Row():
        input_box = gr.Textbox(
            label="Enter your prompt",
            placeholder="Write the prompt you want to enhance...",
            lines=4
        )

    submit_btn = gr.Button("Enhance Prompt", variant="primary")

    output_box = gr.Textbox(
        label="Enhanced Prompt",
        lines=6
    )

    submit_btn.click(
        fn=enhance_prompt,
        inputs=[input_box, use_case_dropdown],
        outputs=output_box
    )

# Run the app
app.queue().launch()
