import gradio as gr
from services.enhancer_pipeline import enhance_prompt
from services.mistral_client import process_document   
from agents.execute_agent import agent_execute


def enhance_and_replace(prompt, use_case, stored_original, is_enhanced, document=None):
    if not is_enhanced:
        stored_original = prompt

    enhanced = enhance_prompt(prompt, use_case, document=document)
    return enhanced, stored_original, True, gr.Button(visible=True)


def go_back(stored_original):
    return stored_original, False, gr.Button(visible=False)


def load_document(file):
    """Reads an uploaded file and processes it with your OCR pipeline."""
    if file is None:
        return gr.update()

    text = process_document(file.name)  # your function receives file path
    return text  # goes into input_box

def submit_prompt(prompt):
    """Handles the final submission of the prompt."""
    # Here you would implement whatever needs to be done with the final prompt.
    print("Final Prompt Submitted:")
    print(prompt)
    
    return agent_execute(prompt)

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
            placeholder="Write the prompt you want to enhance or upload a document...",
            lines=4
        )

        # Output box
        output_box = gr.Textbox(
            label="Result",
            lines=4
        )

         # ====== FILE UPLOAD SECTION ======  ← ADDED
        with gr.Row():
            file_upload = gr.File(
                label="Upload a PDF or image (optional)",
                file_types=[".pdf", ".jpg", ".jpeg", ".png"],
                interactive=True
            )

        with gr.Row():
            submit_btn = gr.Button("Submit", elem_id="medium-submit-btn", variant="primary")

        # UI state
        stored_original = gr.State("")
        is_enhanced = gr.State(False)

        # Enhance button
        enhance_btn.click(
            fn=enhance_and_replace,
            inputs=[input_box, use_case_dropdown, stored_original, is_enhanced, file_upload],
            outputs=[input_box, stored_original, is_enhanced, back_btn]
        )

        # Back button
        back_btn.click(
            fn=go_back,
            inputs=[stored_original],
            outputs=[input_box, is_enhanced, back_btn]
        )

        # Submit 
        submit_btn.click(
            fn=submit_prompt,
            inputs=[input_box],
            outputs=[output_box]
        )

    return app
