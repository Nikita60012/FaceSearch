import logging

from fastapi import FastAPI

from src.workersList_editing.router import router as router_worker
from src.identificate.router import router as router_identify

logging.basicConfig(level=logging.INFO, filename='face_search_log.log', filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(
    title="Биометрическая верификация"
)

app.include_router(router_worker)
app.include_router(router_identify)


