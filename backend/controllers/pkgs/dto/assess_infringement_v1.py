from pkgs.model.assess_infringement import AssessInfringementModel
from pydantic import BaseModel

from .product_infringement import AssessInfringementV1Resp

################################################################################


class CreateAssessInfringementV1Request(AssessInfringementV1Resp): ...


class CreateAssessInfringementV1Response(BaseModel):
    id: int
    patent_id: str
    company_name: str
    analysis_date: str
    top_infringing_products: str
    overall_risk_assessment: str
    created_at: int
    updated_at: int

    @classmethod
    def from_assess_infringement_model(
        cls, model: AssessInfringementModel
    ) -> "CreateAssessInfringementV1Response":
        return cls(
            id=model.id,
            patent_id=model.patent_id,
            company_name=model.company_name,
            analysis_date=model.analysis_date.strftime("%Y-%m-%d %H:%M:%S"),
            top_infringing_products=model.top_infringing_products,
            overall_risk_assessment=model.overall_risk_assessment,
            created_at=int(model.created_at.timestamp()),
            updated_at=int(model.updated_at.timestamp()),
        )


################################################################################


class GetAssessInfringementV1Response(CreateAssessInfringementV1Response): ...


################################################################################
