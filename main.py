import logging
from multiprocessing import freeze_support

import uvicorn
from fastapi import FastAPI
from src.database.connection.database import migration_check
from src.rest.router.WorkersListRouter import router as router_worker
from src.rest.router.IdentificateRouter import router as router_identify
from src.rest.router.ClientRouter import router as router_client
from src.rest.router.SubscribesRouter import router as router_subscribe

logging.basicConfig(level=logging.INFO, filename='face_identificate_log.log', filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(
    title="Биометрическая верификация"
)

if __name__ == '__main__':
    freeze_support()
    migration_check()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=4)

app.include_router(router_worker)
app.include_router(router_identify)
app.include_router(router_client)
app.include_router(router_subscribe)
