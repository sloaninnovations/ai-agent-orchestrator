# v1.0 - LLM agent to generate project milestones and architecture
import openai

def plan_project(goal: str, project_id: str):
    system = "You're an expert software architect helping non-technical users build apps."
    user = f"""
    A user wants to build this: "{goal}"

    1. Describe the goal in 1 sentence
    2. List technical components needed
    3. Suggest a tech stack
    4. Break the project into 3–5 milestones
    5. List 1–2 questions to ask the user only if absolutely necessary
    Respond in JSON.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    return content
