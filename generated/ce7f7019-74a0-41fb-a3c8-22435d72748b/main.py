from fastapi import FastAPI
import random

app = FastAPI()

inspirational_quotes = [
    "The best way to get started is to quit talking and begin doing.",
    "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.",
    "Don’t let yesterday take up too much of today.",
    "You learn more from failure than from success. Don’t let it stop you. Failure builds character."
]

motivational_messages = [
    "Believe you can and you're halfway there.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Sometimes later becomes never. Do it now."
]

@app.get("/inspire")
def inspire():
    return {"message": random.choice(inspirational_quotes)}

@app.get("/motivate")
def motivate():
    return {"message": random.choice(motivational_messages)}