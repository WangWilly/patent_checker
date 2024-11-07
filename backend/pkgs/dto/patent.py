from typing import Dict, List

from pkgs.logging import get_logger_named

from .patent_claim import PatentClaimDto

################################################################################


class PatentDto:
    def __init__(
        self,
        id: int,
        publication_number: str,
        title: str,
        abstract: str,
        description: str,
    ) -> None:
        self.id: int = id
        self.publication_number: str = publication_number
        self.title: str = title
        self.abstract: str = abstract
        self.description: str = description

        self.claims: List[PatentClaimDto] = []

    def __str__(self) -> str:
        return f"{self.publication_number}: {self.title}"

    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################

    def add_claim(self, claim: PatentClaimDto) -> None:
        self.claims.append(claim)

    def str_for_gpt(self) -> str:
        return f"The patent '{self.title}' is about {self.abstract}. Description: {self.description}, Claims: [{', '.join([claim.text for claim in self.claims])}]"

    ############################################################################

    @classmethod
    def from_dict(cls, data: dict) -> "PatentDto":
        logger = get_logger_named("PatentDto")

        if not data:
            logger.warning("No data provided")
            return None

        if "id" not in data:
            logger.warning("No id provided")
            return None

        if "publication_number" not in data:
            logger.warning("No publication_number provided")
            return None

        if "title" not in data:
            logger.warning("No title provided")
            return None

        if "abstract" not in data:
            logger.warning("No abstract provided")
            return None

        if "description" not in data:
            logger.warning("No description provided")
            return None

        patent: PatentDto = cls(
            id=data["id"],
            publication_number=data["publication_number"],
            title=data["title"],
            abstract=data["abstract"],
            description=data["description"],
        )

        if "claims" in data:
            claims = PatentClaimDto.from_json_list(data["claims"])
            patent.claims = claims

        return patent


################################################################################


class Patents:
    def __init__(self) -> None:
        self.pub_patent_map: Dict[str, PatentDto] = {}

    def __str__(self) -> str:
        return str(self.pub_patent_map)

    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################

    def add_patent(self, patent: PatentDto) -> None:
        logger = get_logger_named("Patents.add_patent")

        if not patent:
            logger.warning("No patent provided")
            return

        if not patent.publication_number:
            logger.warning("No publication_number provided")
            return

        if patent.publication_number in self.pub_patent_map:
            logger.warning(f"Patent {patent.publication_number} already exists")
            return

        self.pub_patent_map[patent.publication_number] = patent

    def get_patent(self, publication_number: str) -> PatentDto:
        logger = get_logger_named("Patents.get_patent")
        if publication_number not in self.pub_patent_map:
            logger.warning(f"Patent {publication_number} not found")
            return None

        return self.pub_patent_map[publication_number]

    ############################################################################

    @classmethod
    def from_dict(cls, data: dict) -> "Patents":
        logger = get_logger_named("Patents")

        if not data:
            logger.warning("No data provided")
            return None

        patents: Patents = cls()

        for patent_data in data:
            patent = PatentDto.from_dict(patent_data)
            patents.add_patent(patent)

        return patents
