from typing import List

from controllers.pkgs.dto.product_infringement import (
    AssessInfringementV1Req, AssessInfringementV1Resp, ProductInfringementDto)
from pkgs.errors import GptNotWorkingError, NoContentError, RecordNotFoundError
from pkgs.logging import get_logger_named

from .members import Members

################################################################################


def assess_infringement_v1(
    members: Members,
):
    def _assess_infringement_v1(
        req: AssessInfringementV1Req,
    ) -> AssessInfringementV1Resp:
        logger = get_logger_named("assess_infringement_v1")
        logger.info(f"input: {req.patent_pub_id}, {req.company_name}")

        # Validation
        patent = members.patents.get_patent(req.patent_pub_id)
        if not patent:
            msg = f"Patent '{req.patent_pub_id}' not found"
            logger.error(msg)
            return RecordNotFoundError.to_resp(msg)

        company = members.companies.get_company(req.company_name)
        if not company:
            msg = f"Company '{req.company_name}' not found"
            logger.error(msg)
            return RecordNotFoundError.to_resp(msg)

        infringements: List[ProductInfringementDto] = (
            members.gptHelper.assess_company_v1(patent, company)
        )

        top_infringements = sorted(
            [
                infringement
                for infringement in infringements
                if infringement.infringement_likelihood > 0.3
            ],
            key=lambda x: x.infringement_likelihood,
        )

        if not top_infringements or len(top_infringements) == 0:
            msg = "No infringements found"
            logger.warning(msg)
            return NoContentError.to_resp()

        summary, ok = members.gptHelper.summarize_v1(patent, company, top_infringements)
        if not ok:
            msg = "Failed to summarize"
            logger.error(msg)
            return GptNotWorkingError.to_resp(msg)

        resp = AssessInfringementV1Resp.from_product_infringement_dto_list(
            patent=patent,
            company=company,
            infringement_dtos=top_infringements,
            summary=summary,
        )

        logger.info(f"output: {resp}")
        return resp

    return _assess_infringement_v1
