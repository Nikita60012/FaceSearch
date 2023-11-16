import src
from src.dao import IdentificateDAO, WorkersListModelsDAO
from src.database.connection import database, db_config
from src.dto.request import AddWorkerDTO, UpdateWorkerDTO
from src.rest.router import IdentificateRouter, WorkersListRouter
from src.service.detector import DetectorService
from src.service.Image import ImageService
