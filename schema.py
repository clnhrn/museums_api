from pydantic import BaseModel
from typing import Optional


class Artist(BaseModel):
    id: int
    artist_name: str
    artist_race_primary: str
    artist_race_secondary: Optional[str] = None
    artist_bio: str
    nationality: Optional[str] = None
    artist_dob: Optional[str] = None
    artist_dod: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        orm_mode = True


class Artwork(BaseModel):
    artist_id: int
    artist_name: str
    artist_race_primary: str
    racial_category: str
    artist_bio: Optional[str] = None
    museum_name: str
    artwork_name: str
    medium: Optional[str] = None
    date_created: str
    formatted_date: int
    id: int

    class Config:
        orm_mode = True


class ArtworkResponse(BaseModel):
    artist_id: int
    artist_name: str
    artist_race_primary: str
    racial_category: str
    artist_bio: Optional[str] = None
    museum_name: str
    artwork_name: str
    medium: Optional[str] = None
    date_created: str
    formatted_date: int
    id: int

    class Config:
        orm_mode = True


class ArtistResponse(BaseModel):
    id: int
    artist_name: str
    artist_race_primary: Optional[str] = None
    artist_race_secondary: Optional[str] = None
    artist_bio: Optional[str] = None
    nationality: Optional[str] = None
    artist_dob: Optional[str] = None
    artist_dod: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        orm_mode = True

