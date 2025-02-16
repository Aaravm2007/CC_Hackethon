from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Founder(Base):
    __tablename__ = "founders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    linkedin_id = Column(String, unique=True)
    email = Column(String, unique=True)
    linkedin_url = Column(String, unique=True)
    job_title = Column(String)
    skills = Column(JSON)
    experience = Column(JSON)
