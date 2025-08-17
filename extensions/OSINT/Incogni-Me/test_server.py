"""
Point d'entrée pour l'extension incogni-me.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Incogni-me API")

class UserBase(BaseModel):
    email: str

@app.get("/")
async def root():
    return {"message": "Bienvenue sur Incogni-me"}

@app.get("/test")
async def test_connection():
    return {"status": "ok", "message": "Le serveur fonctionne correctement"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
