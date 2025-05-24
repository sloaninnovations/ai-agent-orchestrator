# v1.0 - Mocked code generation service
import uuid

def generate_code_project(prompt: str) -> dict:
    # In future: Call OpenAI GPT to generate code here
    project_id = str(uuid.uuid4())
    print(f"[MockGen] Prompt received: {prompt}")

    return {
        "project_id": project_id,
        "files": {
            "main.py": "# This is a generated Flask app\nfrom flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return 'Hello, World!'"
        },
        "message": "Code mock generated successfully"
    }
