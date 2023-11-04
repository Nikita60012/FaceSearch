from fastapi import FastAPI

from src.workersList_editing.router import router as router_worker

app = FastAPI(
    title="Биометрическая верификация"
)

app.include_router(router_worker)


