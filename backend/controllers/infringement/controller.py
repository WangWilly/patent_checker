from fastapi import APIRouter, Response
from pkgs.common import route_ruok
from pkgs.constants import GET, POST
from sqlalchemy.orm import Session

from .config import Config
from .docs import docs_create_v1, docs_get_v1, docs_router
from .members import Members
from .route_create_assess_infringement_v1 import create_assess_infringement_v1
from .route_get_assess_infringement_v1 import get_assess_infringement_v1

################################################################################


class Controller:
    def __init__(self, db: Session, cfg: Config):
        self.members = Members(db=db, cfg=cfg)

        self.router = APIRouter(prefix="/api/infringement", **docs_router)
        self.router.add_api_route(**route_ruok)
        self.router.add_api_route(
            "/v1",
            create_assess_infringement_v1(self.members),
            methods=[POST],
            **docs_create_v1,
        )
        self.router.add_api_route(
            "/v1/{assess_infringement_id}",
            get_assess_infringement_v1(self.members),
            methods=[GET],
            **docs_get_v1,
        )

    ############################################################################

    def get_router(self):
        return self.router
