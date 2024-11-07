from typing import List

from pkgs.logging import get_logger_named

from .product import ProductDto

################################################################################


class CompanyProductsDto:
    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

        self.products: List[ProductDto] = []

    def __str__(self) -> str:
        return f"{self.company_name}: {self.products}"

    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################

    def add_product(self, product: ProductDto) -> None:
        self.products.append(product)

    ############################################################################

    @classmethod
    def from_dict(cls, data: dict) -> "CompanyProductsDto":
        logger = get_logger_named("CompanyProductsDto")

        if not data:
            logger.warning("No data provided")
            return None

        if "name" not in data:
            logger.warning("No name provided")
            return None

        company_products: CompanyProductsDto = cls(company_name=data["name"])

        if "products" in data:
            for product_data in data["products"]:
                product = ProductDto.from_dict(product_data)
                company_products.add_product(product)

        return company_products
