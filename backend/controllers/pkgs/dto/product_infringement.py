import datetime
from typing import List

from pkgs.dto.company_products import CompanyProductsDto
from pkgs.dto.patent import PatentDto
from pkgs.dto.product import ProductDto
from pydantic import BaseModel

################################################################################


class ProductInfringementDto:
    def __init__(
        self,
        patent_pub_id: str,
        product_name: str,
        infringement_likelihood: float,
        relevant_claims: List[str],
        explanation: str,
        specific_features: List[str],
    ) -> None:
        self.patent_pub_id: str = patent_pub_id
        self.product_name: str = product_name
        self.infringement_likelihood: float = infringement_likelihood
        self.relevant_claims: List[str] = relevant_claims
        self.explanation: str = explanation
        self.specific_features: List[str] = specific_features

    ############################################################################

    def __str__(self) -> str:
        return f"[{self.patent_pub_id}] {self.product_name}: {self.infringement_likelihood}"

    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################

    def str_for_gpt(self) -> str:
        return f"The evidence suggests that the product '{self.product_name}' infringes on the patent '{self.patent_pub_id}' with a likelihood of {self.infringement_likelihood}. The explanation is: {self.explanation}. The specific features are {', '.join(self.specific_features)}"

    ############################################################################

    @classmethod
    def from_gpt_response(
        cls, patent: PatentDto, product: ProductDto, response: str
    ) -> "ProductInfringementDto":
        lines = response.split("\n")
        relevant_claims = []
        explanation = ""
        specific_features = []

        for line in lines:
            if line.startswith("relevant_claims:"):
                relevant_claims = line.split(":")[1].strip().split(",")
            elif line.startswith("explanation:"):
                explanation = line.split(":")[1].strip()
            elif line.startswith("specific_features:"):
                specific_features = line.split(":")[1].strip().split(",")

        likelihood = len(relevant_claims) / len(patent.claims)

        return cls(
            patent_pub_id=patent.publication_number,
            product_name=product.name,
            infringement_likelihood=likelihood,
            relevant_claims=relevant_claims,
            explanation=explanation,
            specific_features=specific_features,
        )


################################################################################


class AssessInfringementV1ProductItem(BaseModel):
    product_name: str
    infringement_likelihood: str
    relevant_claims: List[str]
    explanation: str
    specific_features: List[str]

    ############################################################################

    @classmethod
    def from_product_infringement_dto(
        cls, dto: ProductInfringementDto
    ) -> "AssessInfringementV1ProductItem":
        infringement_likelihood = "High" if dto.infringement_likelihood > 0.5 else "Low"

        return cls(
            product_name=dto.product_name,
            infringement_likelihood=infringement_likelihood,
            relevant_claims=dto.relevant_claims,
            explanation=dto.explanation,
            specific_features=dto.specific_features,
        )

    @classmethod
    def models_dump_json(cls, models: List["AssessInfringementV1ProductItem"]) -> str:
        return "[" + ",".join([model.model_dump_json() for model in models]) + "]"


################################################################################


class AssessInfringementV1Req(BaseModel):
    patent_pub_id: str
    company_name: str


class AssessInfringementV1Resp(BaseModel):
    patent_id: str
    company_name: str
    analysis_date: str
    top_infringing_products: List[AssessInfringementV1ProductItem]
    overall_risk_assessment: str

    ############################################################################

    @classmethod
    def from_product_infringement_dto_list(
        cls,
        patent: PatentDto,
        company: CompanyProductsDto,
        infringement_dtos: List[ProductInfringementDto],
        summary: str,
    ) -> "AssessInfringementV1Resp":
        return cls(
            patent_id=patent.publication_number,
            company_name=company.company_name,
            analysis_date=datetime.datetime.now().isoformat(),
            top_infringing_products=[
                AssessInfringementV1ProductItem.from_product_infringement_dto(item)
                for item in infringement_dtos
            ],
            overall_risk_assessment=summary,
        )
