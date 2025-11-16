import gradio as gr
from services.enhancer_pipeline import enhance_prompt


def enhance_and_replace(prompt, use_case, stored_original, is_enhanced):
    """Enhance prompt and replace text in-place; store original if needed."""
    # Only store original on first enhancement
    if not is_enhanced:
        stored_original = prompt

    enhanced = enhance_prompt(prompt, use_case)
    return enhanced, stored_original, True, gr.Button(visible=True)


def go_back(stored_original):
    """Restore the user's original prompt."""
    return stored_original, False, gr.Button(visible=False)


def create_app():
    # Load CSS
    try:
        with open("assets/styles.css") as f:
            custom_css = f.read()
    except:
        custom_css = ""

    with gr.Blocks(css=custom_css) as app:
        gr.Markdown(
            """
            # ✨ Prompt Enhancer  
            Improve your prompts automatically using GPT-4o via Azure OpenAI.
            """
        )

        # Use Case Selector
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

        # Label + Buttons
        with gr.Row(elem_classes=["label-row"]):
            gr.Markdown("**Enter your prompt**")
            enhance_btn = gr.Button("Enhance ⋆˙⟡", elem_id="small-submit-btn", variant="secondary")
            back_btn = gr.Button("Back ↩", elem_id="back-btn", variant="secondary", visible=False)

        # Input box
        input_box = gr.Textbox(
            label="",
            placeholder="Write the prompt you want to enhance...",
            lines=4
        )

        # UI state
        stored_original = gr.State("")
        is_enhanced = gr.State(False)

        # Enhance button
        enhance_btn.click(
            fn=enhance_and_replace,
            inputs=[input_box, use_case_dropdown, stored_original, is_enhanced],
            outputs=[input_box, stored_original, is_enhanced, back_btn]
        )

        # Back button
        back_btn.click(
            fn=go_back,
            inputs=[stored_original],
            outputs=[input_box, is_enhanced, back_btn]
        )

    return app
