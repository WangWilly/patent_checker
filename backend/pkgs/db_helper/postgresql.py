from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import Config

################################################################################

__engine = None


def get_db(cfg: Config = Config()) -> Session:
    global __engine
    if __engine is None:
        __engine = create_engine(
            f"postgresql://{cfg.user}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.name}"
        )

    _Session = sessionmaker(bind=__engine)
    db = _Session()
    return db
