import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import func
from sqlalchemy.orm import load_only
from fastapi_pagination import Page, paginate, add_pagination

from models import Artist as ModelArtist
from models import Artwork as ModelArtwork
from schema import Artwork as SchemaArtwork
from schema import ArtworkResponse as SchemaArtworkOut
from schema import ArtistResponse as SchemaArtistOut

# access env variables
load_dotenv(".env")

# creating an instance from FastAPI
app = FastAPI(title="Museums API", version="0.0.1")


# setting up db connection
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


# get all records
@app.get("/museums-api/v1/artworks/all", response_model=Page[SchemaArtworkOut])
async def get_all_artworks():
    records = db.session.query(ModelArtwork).all()
    return paginate(records)


# get records based on year range, race, museum
@app.get("/museums-api/v1/artworks/filter", response_model=Page[SchemaArtworkOut])
def filter_artworks(
    start_year: int = 1950,
    end_year: int = 2022,
    race: str = None,
    museum_name: str = None,
):
    if race is None and museum_name is None:
        records = (
            db.session.query(ModelArtwork)
            .filter(
                ModelArtwork.formatted_date >= start_year,
                ModelArtwork.formatted_date <= end_year,
            )
            .all()
        )

    elif race is not None and museum_name is None:
        records = (
            db.session.query(ModelArtwork)
            .filter(
                ModelArtwork.formatted_date >= start_year,
                ModelArtwork.formatted_date <= end_year,
                ModelArtwork.racial_category == race.title(),
            )
            .all()
        )

    elif race is None and museum_name is not None:
        records = (
            db.session.query(ModelArtwork)
            .filter(
                ModelArtwork.formatted_date >= start_year,
                ModelArtwork.formatted_date <= end_year,
                ModelArtwork.museum_name == museum_name.title(),
            )
            .all()
        )

    else:
        records = (
            db.session.query(ModelArtwork)
            .filter(
                ModelArtwork.formatted_date >= start_year,
                ModelArtwork.formatted_date <= end_year,
                ModelArtwork.racial_category == race.title(),
                ModelArtwork.museum_name == museum_name.title(),
            )
            .all()
        )
    return paginate(records)


@app.get("/museums-api/v1/artists/all", response_model=Page[SchemaArtistOut])
async def get_all_artists():
    records = db.session.query(ModelArtist).all()
    return paginate(records)

add_pagination(app)


# @app.post("/add-artwork/", response_model=SchemaArtwork)
# def add_artwork(artwork: SchemaArtwork):
#     db_artwork = ModelArtwork()
#     db.session.add(db_artwork)
#     db.session.commit()
#     return db_artwork


# @app.post("/add-artist/", response_model=SchemaArtist)
# def add_artist(artist: SchemaArtist):
#     db_artist = ModelArtist()
#     db.session.add(db_author)
#     db.session.commit()
#     return db_artist


# @app.post("/user/", response_model=SchemaUser)
# def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
