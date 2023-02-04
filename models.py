from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, nullable=False) 
    artist_name = Column(String)
    artist_race_primary = Column(String)
    artist_race_secondary = Column(String, nullable=True)
    artist_bio = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    artist_dob = Column(String, nullable=True)
    artist_dod = Column(String, nullable=True)
    gender = Column(String, nullable=True)


class Artwork(Base):
    __tablename__ = "artworks"
    artist_id = Column(Integer)
    artist_name = Column(String)
    artist_race_primary = Column(String)
    racial_category = Column(String)
    artist_bio = Column(String, nullable=True)
    museum_name = Column(String)
    artwork_name = Column(String)
    medium = Column(String, nullable=True)
    date_created = Column(String)
    formatted_date = Column(Integer)
    id = Column(Integer, primary_key=True, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

