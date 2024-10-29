import time
import asyncio

@app.get(
    "/sync/{id}",
)
def sync_func(id: int):
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time():.2f}")

@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time():.2f}")