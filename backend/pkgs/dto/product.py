from pkgs.logging import get_logger_named

################################################################################


class ProductDto:
    def __init__(self, name: str, description: str) -> None:
        self.name: str = name
        self.description: str = description

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################

    def str_for_gpt(self) -> str:
        return f"The product '{self.name}' is about {self.description}"

    ############################################################################

    @classmethod
    def from_dict(cls, data: dict) -> "ProductDto":
        logger = get_logger_named("ProductDto")

        if not data:
            logger.warning("No data provided")
            return None

        if "name" not in data:
            logger.warning("No name provided")
            return None

        if "description" not in data:
            logger.warning("No description provided")
            return None

        return cls(name=data["name"], description=data["description"])
