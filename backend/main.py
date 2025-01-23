import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from routers import wilberries, auth


logging.basicConfig(
    filename='backend.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='w'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        scheduler.start()
        logging.error(f"JOBS: {scheduler.get_jobs()}")
    except Exception as e:
        logging.error(f"Ошибка инициализации планировщика: {e}")
    finally:
        yield
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(wilberries.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run("main:app", log_config=None)
