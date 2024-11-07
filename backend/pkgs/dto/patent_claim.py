import json
from typing import List

from pkgs.logging import get_logger_named

################################################################################


class PatentClaimDto:
    def __init__(self, num: str, text: str) -> None:
        self.num = num
        self.text = text

        self.patent_id = None

    def __str__(self):
        if not self.patent_id:
            return f"{self.num}: {self.text}"

        return f"{self.patent_id}: [{self.num}] {self.text}"

    def __repr__(self):
        return self.__str__()

    ############################################################################

    def set_patent_id(self, patent_id: int) -> None:
        self.patent_id = patent_id

    ############################################################################

    @classmethod
    def from_dict(cls, data: dict) -> "PatentClaimDto":
        logger = get_logger_named("PatentClaimDto")

        if not data:
            logger.warning("No data provided")
            return None

        if "num" not in data:
            logger.warning("No num provided")
            return None

        if "text" not in data:
            logger.warning("No text provided")
            return None

        return cls(num=data["num"], text=data["text"])

    @classmethod
    def from_list(cls, data: List[dict]) -> List["PatentClaimDto"]:
        logger = get_logger_named("PatentClaimDto")

        if not data:
            logger.warning("No data provided")
            return None

        claims = []

        for claim_data in data:
            claim = cls.from_dict(claim_data)
            claims.append(claim)

        return claims

    @classmethod
    def from_json_list(cls, data: str) -> List["PatentClaimDto"]:
        logger = get_logger_named("PatentClaimDto")

        if not data:
            logger.warning("No data provided")
            return None

        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return None

        return cls.from_list(data_dict)
