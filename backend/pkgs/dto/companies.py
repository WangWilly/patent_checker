from typing import Dict

from pkgs.logging import get_logger_named

from .company_products import CompanyProductsDto

################################################################################


class Companies:
    def __init__(self) -> None:
        self.companies: Dict[str, CompanyProductsDto] = {}

    def __str__(self) -> str:
        return str(self.companies)

    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################

    def add_company(self, company: CompanyProductsDto) -> None:
        logger = get_logger_named("Companies.add_company")

        if not company:
            logger.warning("No company provided")
            return

        if not company.company_name:
            logger.warning("No company_name provided")
            return

        if company.company_name in self.companies:
            logger.warning(f"Company {company.company_name} already exists")
            return

        self.companies[company.company_name] = company

    def get_company(self, company_name: str) -> CompanyProductsDto:
        logger = get_logger_named("Companies.get_company")
        if company_name not in self.companies:
            logger.warning(f"Company {company_name} not found")
            return None

        return self.companies[company_name]

    ############################################################################

    @classmethod
    def from_dict(cls, data: dict) -> "Companies":
        logger = get_logger_named("Companies")

        if not data:
            logger.warning("No data provided")
            return None

        companies: Companies = cls()

        for company_data in data:
            company = CompanyProductsDto.from_dict(company_data)
            companies.add_company(company)

        return companies
