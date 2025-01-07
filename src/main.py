import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
#команды для того чтобы обеспечить возможность компилятора доставать файлы из папки src

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)

@app.get("/")
def func():
    return "Hellow orld!"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


