from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create a SQLite database engine
engine = create_engine("sqlite:///database.db", echo=False)

# Create a base class for declarative models
Base = declarative_base()


# Define the Company model
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    industries = Column(String)

    vacancies = relationship("Vacancy", back_populates="company")
    phones = relationship("Phones", back_populates="company")


# Define the Vacancy model
class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_name = Column(String)
    phone = Column(String)
    url = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="vacancies")


class Phones(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="phones")


# Create the tables in the database
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
