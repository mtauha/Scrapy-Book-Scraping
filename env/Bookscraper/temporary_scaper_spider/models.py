from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv


load_dotenv(".env")
DATABASE_URL = getenv("DATABASE-URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(255))
    title = Column(Text)
    product_type = Column(String(255))
    price_excl_tax = Column(DECIMAL(10, 2))
    price_incl_tax = Column(DECIMAL(10, 2))
    tax = Column(DECIMAL(10, 2))
    availability = Column(Integer)
    num_reviews = Column(Integer)
    stars = Column(Integer)
    category = Column(String(255))
    description = Column(Text)


Base.metadata.create_all(bind=engine)