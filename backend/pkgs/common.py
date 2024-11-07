from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .constants import GET, POST


################################################################################
# Basic
class Msg(BaseModel):
    message: str


################################################################################

route_ruok = {
    "path": "/ruok",
    "endpoint": lambda: JSONResponse(
        content=Msg(message="ok").model_dump(), status_code=200
    ),
    "methods": [GET, POST],
    "summary": "Check if the controller is working",
    "description": "Returns 200 if the controller is working.",
    "responses": {200: {"model": Msg}},
}
