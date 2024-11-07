from pkgs.logging import get_logger_named
from pkgs.model.assess_infringement import AssessInfringementModel
from sqlalchemy.orm import Session

################################################################################


def create(
    db: Session,
    patent_id: str,
    company_name: str,
    analysis_date: str,
    top_infringing_products: str,
    overall_risk_assessment: str,
) -> bool:
    logger = get_logger_named("assess_infringement.create")

    try:
        record = AssessInfringementModel(
            patent_id=patent_id,
            company_name=company_name,
            analysis_date=analysis_date,
            top_infringing_products=top_infringing_products,
            overall_risk_assessment=overall_risk_assessment,
        )
        db.add(record)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to create assess infringement: {e}")
        return False

    return True


################################################################################


def create(db: Session, record: AssessInfringementModel) -> bool:
    logger = get_logger_named("assess_infringement.create")

    try:
        db.add(record)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to create assess infringement: {e}")
        return False

    return True
