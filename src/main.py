import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security.api_key import APIKey
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.orm import load_only
from fastapi_pagination import Page, paginate, add_pagination

from src.models import Artist as ModelArtist
from src.models import Artwork as ModelArtwork
from src.models import User as ModelUser
from src.schema import ArtworkResponse as SchemaArtworkOut
from src.schema import ArtistResponse as SchemaArtistOut

from src.auth import AuthHandler
from src.schema import AuthDetails

# access env variables
load_dotenv(".env")

# create an instance of FastAPI
app = FastAPI(title="Museums API", version="0.0.1")

# create an instance of authhandler
auth_handler = AuthHandler()

# set up db connection
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


# register user
@app.post("/museums-api/register", status_code=201)
def register(auth_details: AuthDetails):
    users = db.session.query(ModelUser).all()
    print(users)
    if any(x.username == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    db_user = ModelUser(username=auth_details.username, password=hashed_password)
    db.session.add(db_user)
    db.session.commit()
    return {"message": f"{auth_details.username} registered successfully"}


# login user - return token (to be used for requests)
@app.post("/museums-api/login")
def login(auth_details: AuthDetails):
    users = db.session.query(ModelUser).all()
    user = None
    for x in users:
        if x.username == auth_details.username:
            user = x
            break

    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")

    token = auth_handler.encode_token(user.username)
    return {"token": token}


# get the museums
@app.get("/museums-api/museums-list")
def get_all_museums(username=Depends(auth_handler.auth_wrapper)):
    museum_list = []
    for museum in db.session.query(ModelArtwork.museum_name).distinct():
        museum_list.append(museum.museum_name)
    return {"museums": museum_list}


# get all records
@app.get("/museums-api/artworks", response_model=Page[SchemaArtworkOut])
def get_all_artworks(username=Depends(auth_handler.auth_wrapper)):
    records = (
        db.session.query(ModelArtwork).filter(ModelArtwork.formatted_date <= 2021).all()
    )
    return paginate(records)


# get records based on year range, race, museum
@app.get("/museums-api/artworks/filter", response_model=Page[SchemaArtworkOut])
def filter_artworks(
    start_year: int = 1950,
    end_year: int = 2021,
    race: str = None,
    museum_name: str = None,
    username=Depends(auth_handler.auth_wrapper),
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


@app.get("/museums-api/artists", response_model=Page[SchemaArtistOut])
async def get_all_artists(username=Depends(auth_handler.auth_wrapper)):
    records = db.session.query(ModelArtist).all()
    return paginate(records)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
