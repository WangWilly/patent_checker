from controllers.pkgs.gpt_helper.groq import GptGroq
from fastapi import APIRouter
from pkgs.common import route_ruok
from pkgs.constants import POST

from .config import Config
from .docs import docs_assess_infringement_v1, docs_router
from .members import Members
from .route_assess_infringement_v1 import assess_infringement_v1

################################################################################


class Controller:
    def __init__(self, cfg: Config, gptHelper: GptGroq):
        self.members = Members(cfg=cfg, gptHelper=gptHelper)

        self.router = APIRouter(prefix="/api/gpt", **docs_router)
        self.router.add_api_route(**route_ruok)
        self.router.add_api_route(
            "/v1/assess_infringement",
            assess_infringement_v1(self.members),
            methods=[POST],
            **docs_assess_infringement_v1,
        )

    ############################################################################

    def get_router(self):
        return self.router
