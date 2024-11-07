from controllers.pkgs.gpt_helper.groq import GptGroq
from controllers.pkgs.utils import load_companies, load_patents
from pkgs.dto.companies import Companies
from pkgs.dto.patent import Patents
from pkgs.logging import get_logger_named
from sqlalchemy.orm import Session

from .config import Config

################################################################################


class Members:
    def __init__(self, cfg: Config, gptHelper: GptGroq):
        logger = get_logger_named("Members.__init__")

        # Knowledges
        self.companies: Companies = load_companies(cfg.company_products_path)
        logger.debug(f"Companies: {self.companies}")
        self.patents: Patents = load_patents(cfg.patents_path)
        logger.debug(f"Patents: {self.patents}")

        # GPT Helper
        self.gptHelper = gptHelper
