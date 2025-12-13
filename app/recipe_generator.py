import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_recipe(items: list[str]) -> str:
    prompt = f"""
    Create a simple recipe using the following ingredients:
    {", ".join(items)}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful cooking assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
