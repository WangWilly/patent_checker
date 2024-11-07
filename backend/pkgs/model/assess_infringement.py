from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String

from .base import Base

################################################################################


class AssessInfringementModel(Base):
    __tablename__ = "assess_infringement"

    id = Column(Integer, primary_key=True)
    patent_id = Column(String)
    company_name = Column(String)
    analysis_date = Column(DateTime)
    top_infringing_products = Column(JSON)
    overall_risk_assessment = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    ############################################################################

    def __repr__(self):
        return f"id: {self.id}"
