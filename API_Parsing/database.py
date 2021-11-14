from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://hmxdnwubdttbnz:9e63e8f51fbdaa5a7dfd36e69526ffd277c532dd124debf16f9ef3cebcea5d79@ec2-52-31-233-101.eu-west-1.compute.amazonaws.com:5432/d10gqjnnkpealj"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()