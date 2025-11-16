import os
from dotenv import load_dotenv

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

load_dotenv()

# Azure OpenAI Client Setup
client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_OPENAI_API_KEY"]),
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def call_agent(system_prompt: str, user_message: str) -> str:
    """
    Sends a system prompt + user message to Azure OpenAI
    and returns the model's content-only response.
    """
    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_message),
        ],
        model=deployment_name,
    )

    content = response.choices[0].message["content"]
    print("Agent Response:", content)
    return content
