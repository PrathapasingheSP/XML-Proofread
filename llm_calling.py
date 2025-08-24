import re
import json
from openai import OpenAI,AzureOpenAI
import ast
from functions import load_config
from logger import get_logger


config = load_config()


# Initialize OpenAI client
llm_method = config.get("llm_method", 1)
if llm_method == 1:
    openai_config = config.get("openai", {})
    base_url = openai_config.get("base_url")
    api_key = openai_config.get("api_key")
    model_name = openai_config.get("model_name")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
else:
    azureopenai_config = config.get("azureopenai", {})
    endpoint = azureopenai_config.get("endpoint")
    api_key = azureopenai_config.get("api_key")
    model_name = azureopenai_config.get("model_name")
    api_version = azureopenai_config.get("api_version")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )


with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()


# Chat with GPT function
def chat_with_gpt(input_list,lang,logger): 
    if llm_method==1:
        logger.info(f"Chat with GPT function started... LLM is openrouter OpenAI")   
    else:
        logger.info(f"Chat with GPT function started... LLM is Azure OpenAI")   
    user_content = json.dumps({
    "language": lang,
    "p_tag_list": input_list
    })

    response = client.chat.completions.create(
      extra_body={},
      model=model_name,
      messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": user_content
        }
      ],temperature=0.4
    )

    raw_content = response.choices[0].message.content.strip()

    # 1. Remove ```json ... ``` or ``` fences if they exist
    cleaned = re.sub(r"^```(?:json)?\n?", "", raw_content)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    # 2. Now try to parse as JSON
    try:
        result = ast.literal_eval(cleaned)  # Safely parse Python literals
        logger.info(f"Chat with GPT function completed...")
        return result
    except Exception as e:
        logger.error("Error parsing:", e)
        raise