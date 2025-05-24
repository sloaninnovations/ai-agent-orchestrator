from fastapi import FastAPI

app = FastAPI()

@app.get("/inspire")
async def inspire():
    return {"message": "The only way to do great work is to love what you do."}

@app.get("/motivate")
async def motivate():
    return {"message": "Believe you can and you're halfway there."}