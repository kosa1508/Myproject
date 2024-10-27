import uvicorn
from fastapi import FastAPI
import json

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)

@app.get("/")
def func():
    return "Специально для Яночки не hello world)!!! Очень тебя люблю!"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


