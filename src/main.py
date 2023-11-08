from fastapi import FastAPI

from src.workersList_editing.router import router as router_worker
from src.identificate.router import router as router_identify

app = FastAPI(
    title="Биометрическая верификация"
)

app.include_router(router_worker)
app.include_router(router_identify)


