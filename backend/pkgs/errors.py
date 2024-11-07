from fastapi.responses import JSONResponse
from pydantic import BaseModel


################################################################################
# Basic Errors
class ErrorMsg(BaseModel):
    message: str


################################################################################
# 2XX Errors
class NoContentError:
    @classmethod
    def to_resp(cls) -> JSONResponse:
        return JSONResponse(status_code=204)


################################################################################
# 4XX Errors
class RecordNotFoundError:
    prefix = "[Not found] "
    model = ErrorMsg

    @classmethod
    def to_resp(cls, message: str = "") -> JSONResponse:
        message = cls.prefix + message
        return JSONResponse(
            content=cls.model(message=message).model_dump(), status_code=404
        )


################################################################################
# 5XX Errors
class GptNotWorkingError:
    prefix = "[GPT not working] "
    model = ErrorMsg

    @classmethod
    def to_resp(cls, message: str = "") -> JSONResponse:
        message = cls.prefix + message
        return JSONResponse(
            content=cls.model(message=message).model_dump(), status_code=500
        )


class DbRecordNotCreatedError:
    prefix = "[Record not created] "
    model = ErrorMsg

    @classmethod
    def to_resp(cls, message: str = "") -> JSONResponse:
        message = cls.prefix + message
        return JSONResponse(
            content=cls.model(message=message).model_dump(), status_code=500
        )
