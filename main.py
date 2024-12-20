from fastapi import FastAPI

from src.database import create_keyspace_and_table
from src.router import router


def lifespan(app: FastAPI):
    create_keyspace_and_table()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
