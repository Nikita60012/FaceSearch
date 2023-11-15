import logging

import uvicorn
from fastapi import FastAPI

from src.workersList_editing.router import router as router_worker
from src.identificate.router import router as router_identify

logging.basicConfig(level=logging.INFO, filename='face_search_log.log', filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(
    title="Биометрическая верификация"
)
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)

app.include_router(router_worker)
app.include_router(router_identify)


