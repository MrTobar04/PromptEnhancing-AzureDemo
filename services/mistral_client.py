import os
import base64
import requests
import re
import mimetypes

endpoint = "https://promptenhancing-demo-resource.services.ai.azure.com/providers/mistral/azure/ocr"
api_key = os.environ["AZURE_API_KEY"]


def clean_markdown(markdown: str) -> str:
    """Remove markdown image tags and return clean OCR text."""
    if not markdown:
        return ""
    
    # Remove ![xxx](xxx)
    markdown = re.sub(r'!\[.*?\]\(.*?\)', '', markdown)
    
    # Remove extra whitespace
    return markdown.strip()


def process_document(file_path: str) -> str:
    # Load the file
    with open(file_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    # Detect mime type
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        raise ValueError(f"Cannot detect MIME type for: {file_path}")

    # Determine Mistral's document type field
    doc_type = "document_url" if "pdf" in mime_type else "image_url"

    payload = {
        "model": "mistral-document-ai-2505",
        "document": {
            "type": doc_type,
            doc_type: f"data:{mime_type};base64,{b64_data}"
        },
        "include_image_base64": False  # no need if we only want OCR
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    data = response.json()

    # Extract OCR markdown from first page
    pages = data.get("pages", [])
    if not pages:
        print("⚠️ No OCR pages found.")
        return ""

    markdown = pages[0].get("markdown", "")

    # Convert markdown → clean text
    text = clean_markdown(markdown)

    # Print clean OCR text
    print(f"OCR detected: {text}")
    return text
