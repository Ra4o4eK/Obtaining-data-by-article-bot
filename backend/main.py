import uvicorn
from fastapi import FastAPI

from routers import wilberries
from utils import scheduler


app = FastAPI(debug=True)
app.include_router(wilberries.router)


if __name__ == "__main__":
    uvicorn.run("main:app")
    scheduler.start()
