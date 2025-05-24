# v1.0 - GitHub commit utility
import os
import base64
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # e.g. sloaninnovations/ai-agent-orchestrator
GITHUB_API = "https://api.github.com"

def commit_project_to_github(project_id: str, path: str) -> dict:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    commit_results = {}
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        with open(file_path, "rb") as f:
            content = f.read()

        encoded = base64.b64encode(content).decode("utf-8")
        github_path = f"generated/{project_id}/{filename}"
        url = f"{GITHUB_API}/repos/{GITHUB_REPO}/contents/{github_path}"

        data = {
            "message": f"Add {filename} for project {project_id}",
            "content": encoded,
            "branch": "main"
        }

        r = requests.put(url, json=data, headers=headers)
        commit_results[filename] = r.status_code

    return commit_results
