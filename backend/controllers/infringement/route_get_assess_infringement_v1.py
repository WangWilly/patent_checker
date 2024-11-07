from typing import Annotated

from controllers.pkgs.dto.assess_infringement_v1 import \
    GetAssessInfringementV1Response
from fastapi import Path
from pkgs.errors import RecordNotFoundError
from pkgs.logging import get_logger_named
from pkgs.model.assess_infringement import AssessInfringementModel
from pkgs.repo.assess_infringement.get import get

from .members import Members

################################################################################


def get_assess_infringement_v1(
    members: Members,
):
    def _get_assess_infringement_v1(
        assess_infringement_id: Annotated[int, Path()],
    ) -> GetAssessInfringementV1Response:
        logger = get_logger_named("assess_infringement.get.v1")

        record: AssessInfringementModel = get(
            db=members.db,
            id=assess_infringement_id,
        )

        if not record:
            msg = "assess infringement record not found"
            logger.error("assess infringement record not found")
            return RecordNotFoundError.to_resp(msg)

        return GetAssessInfringementV1Response.from_assess_infringement_model(record)

    return _get_assess_infringement_v1
