from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def generate_recipe(items: list[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Create a simple recipe using the following ingredients:
    {", ".join(items)}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
