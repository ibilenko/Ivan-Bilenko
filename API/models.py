from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class id(Base):
    __tablename__ = "test_orm"
    __table_args__ = {'schema': 'gogol'}
    id = Column(Integer, primary_key=True, index=True)


