# v2.2 - Sanitize GPT response and extract code safely
import uuid
import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_code_block(text: str) -> dict:
    try:
        # Find the first python code block
        match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
        raw = match.group(1) if match else text.strip()
        files = eval(raw) if raw.startswith("{") else {"main.py": raw}
        return files
    except Exception:
        return {"main.py": text.strip()}

def generate_code_project(prompt: str) -> dict:
    project_id = str(uuid.uuid4())

    try:
        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate a Python codebase as a dict of {filename: content} for this request."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        content = chat.choices[0].message.content
        files = extract_code_block(content)

        return {
            "project_id": project_id,
            "files": files,
            "message": "Code extracted and cleaned from GPT-4 output"
        }

    except Exception as e:
        return {
            "project_id": project_id,
            "files": {},
            "message": f"Error generating code: {str(e)}"
        }
