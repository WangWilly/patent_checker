from controllers.pkgs.dto.assess_infringement_v1 import (
    CreateAssessInfringementV1Request, CreateAssessInfringementV1Response)
from controllers.pkgs.dto.product_infringement import \
    AssessInfringementV1ProductItem
from pkgs.errors import DbRecordNotCreatedError
from pkgs.logging import get_logger_named
from pkgs.model.assess_infringement import AssessInfringementModel
from pkgs.repo.assess_infringement.create import create

from .members import Members

################################################################################


def create_assess_infringement_v1(
    members: Members,
):
    def _create_assess_infringement_v1(
        req: CreateAssessInfringementV1Request,
    ) -> CreateAssessInfringementV1Response:
        logger = get_logger_named("assess_infringement.create.v1")

        record: AssessInfringementModel = AssessInfringementModel(
            patent_id=req.patent_id,
            company_name=req.company_name,
            analysis_date=req.analysis_date,
            top_infringing_products=AssessInfringementV1ProductItem.models_dump_json(
                req.top_infringing_products
            ),
            overall_risk_assessment=req.overall_risk_assessment,
        )

        if not create(
            db=members.db,
            record=record,
        ):
            msg = "Failed to create assess infringement record"
            logger.error("Failed to create assess infringement record")
            return DbRecordNotCreatedError.to_resp(msg)

        return CreateAssessInfringementV1Response.from_assess_infringement_model(record)

    return _create_assess_infringement_v1
