from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Incogni-me API - Test")

@app.get("/")
async def root():
    return {"message": "Bienvenue sur Incogni-me"}

@app.get("/status")
async def status():
    return {
        "status": "ok",
        "version": "0.1.0",
        "service": "Incogni-me"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
