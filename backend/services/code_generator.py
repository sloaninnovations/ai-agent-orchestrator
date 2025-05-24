# v2.1 - Updated for OpenAI Python SDK v1.x+
import uuid
import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code_project(prompt: str) -> dict:
    project_id = str(uuid.uuid4())

    try:
        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior Python developer. Generate full Python code files as a dictionary of filename: content pairs."},
                {"role": "user", "content": f"Generate a complete small project for this prompt:\n\n{prompt}"}
            ],
            temperature=0.4
        )

        raw = chat.choices[0].message.content.strip()
        files = eval(raw) if raw.startswith("{") else {"main.py": raw}

        return {
            "project_id": project_id,
            "files": files,
            "message": "Code generated using OpenAI SDK v1.x"
        }

    except Exception as e:
        return {
            "project_id": project_id,
            "files": {},
            "message": f"Error generating code: {str(e)}"
        }
