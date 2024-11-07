# from pkgs.logging import get_logger_named
from sqlalchemy.orm import Session

from .config import Config

################################################################################


class Members:
    def __init__(self, db: Session, cfg: Config):
        # logger = get_logger_named("Infringement.Members.__init__")

        # Config
        self.db = db
