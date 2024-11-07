from pkgs.logging import get_logger_named
from pkgs.model.assess_infringement import AssessInfringementModel
from sqlalchemy.orm import Session

################################################################################


def get(db: Session, id: int) -> AssessInfringementModel | None:
    logger = get_logger_named("assess_infringement.get")

    try:
        record = (
            db.query(AssessInfringementModel)
            .filter(AssessInfringementModel.id == id)
            .first()
        )
    except Exception as e:
        logger.error(f"Failed to get assess infringement: {e}")
        return None

    return record


################################################################################


def get_all(db: Session) -> list[AssessInfringementModel]:
    logger = get_logger_named("assess_infringement.get_all")

    try:
        records = db.query(AssessInfringementModel).all()
    except Exception as e:
        logger.error(f"Failed to get all assess infringements: {e}")
        return []

    return records
