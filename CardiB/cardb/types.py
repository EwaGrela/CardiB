from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (CheckConstraint, Column, ForeignKey,
                        Index, Integer, LargeBinary,
                        Numeric, SmallInteger, String, Table, Text, text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine
import os

Base = declarative_base()
metadata = Base.metadata


class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True)
    brand = Column(ForeignKey('brand.name'), index=True)
    model = Column(String, nullable=False)
    info = Column(JSONB, nullable=False)

    def jsonize(self):
        return {"id": self.id, "brand": self.brand,
                "model": self.model, "info": self.info}


class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def jsonize(self):
        return {"id": self.id, "name": self.name}


# creating tables
if __name__ == '__main__':
    engine = create_engine(os.environ['DATABASE_URL'])
    Base.metadata.create_all(engine)
