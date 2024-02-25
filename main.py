from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from MovieBaseModel import Movie
from typing import List

from config.database import Session, engine, Base
from models.movie import MovieDbModel

from movies import movies_list
from index import index_html
from jwt_manager import create_token, validate_token


app = FastAPI()
app.title = "My app"
app.version = "1.0.0"


class User(BaseModel):
    email: str
    password: str


Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@mail.com":
            raise HTTPException(status_code=403, detail="Invalid Credentials")


@app.get("/", tags=["home"])
def message():
    return HTMLResponse(index_html)


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
    return JSONResponse(token)


@app.get("/movies", tags=["movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer)])
def get_movies():
    db = Session()
    result = db.query(MovieDbModel).all()
    return JSONResponse(jsonable_encoder(result))


@app.get("/movies/{movie_title}", tags=["movies"], response_model=Movie)
def get_movies_by_name(movie_title: str = Path(min_length=2)):
    db = Session()
    result = db.query(MovieDbModel).filter(
        MovieDbModel.Title == movie_title).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    # filtered_movies = list(filter(
    #     lambda movie: movie['Title'].lower() == movie_title.lower(), movies_list))
    return JSONResponse(jsonable_encoder(result))


@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(genre: str = Query(min_length=4)):
    db = Session()
    result = db.query(MovieDbModel).filter(
        MovieDbModel.Genre == genre).all()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Genre not found"})
    # filtered_movies = [movie for movie in movies_list if genre.lower() in movie['Genre'].lower()]
    # filtered_movies = list(
    #     filter(lambda movie: genre.lower() in movie['Genre'].lower(), movies_list))
    return JSONResponse(jsonable_encoder(result))


@app.post("/add-movie", tags=["movies"])
def add_movie(movie: Movie):
    db = Session()
    new_movie = MovieDbModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    movies_list.append(movie.model_dump())
    return JSONResponse(movies_list)


@app.delete("/delete-movie/", tags=["movies"])
def delete_movie(title: str):
    db = Session()
    movie_to_delete = db.query(MovieDbModel).filter(
        MovieDbModel.Title == title).first()
    if not movie_to_delete:
        return JSONResponse(status_code=404, content={"message": "Movie to delete not found"})
    db.delete(movie_to_delete)
    db.commit()
    # filtered_movies = list(
    #     filter(lambda movie: title.lower() != movie['Title'].lower(), movies_list))
    return JSONResponse(jsonable_encoder(movie_to_delete))


@app.put("/update/movie/{title}", tags=["movies"])
def update_movies(title: str, new_movie: Movie):
    for movie in movies_list:
        db = Session()
        result = db.query(MovieDbModel).filter(
            MovieDbModel.Title == title).first()
        if not result:
            return HTMLResponse(status_code=404, content={"message": "Movie not found"})

        """
        if movie["Title"].lower() == title.lower():
            movie["Title"] = new_movie.Title
            movie["Year"] = new_movie.Year
            movie["Rated"] = new_movie.Rated
            movie["Released"] = new_movie.Released
            movie["Runtime"] = new_movie.Runtime
            movie["Genre"] = new_movie.Genre
            movie["Director"] = new_movie.Director
            movie["Writer"] = new_movie.Writer
            movie["Actors"] = new_movie.Actors
            movie["Plot"] = new_movie.Plot
            movie["Language"] = new_movie.Language
            movie["Country"] = new_movie.Country
            movie["Awards"] = new_movie.Awards
            movie["Poster"] = new_movie.Poster
            movie["Metascore"] = new_movie.Metascore
            movie["imdbRating"] = new_movie.imdbRating
            movie["imdbVotes"] = new_movie.imdbVotes
            movie["imdbID"] = new_movie.imdbID
            movie["Type"] = new_movie.Type
"""

        result.Year = new_movie.Year
        result.Rated = new_movie.Rated
        result.Released = new_movie.Released
        result.Runtime = new_movie.Runtime
        result.Genre = new_movie.Genre
        result.Director = new_movie.Director
        result.Writer = new_movie.Writer
        result.Actors = new_movie.Actors
        result.Plot = new_movie.Plot
        result.Language = new_movie.Language
        result.Country = new_movie.Country
        result.Awards = new_movie.Awards
        result.Poster = new_movie.Poster
        result.Metascore = new_movie.Metascore
        result.imdbRating = new_movie.imdbRating
        result.imdbVotes = new_movie.imdbVotes
        result.imdbID = new_movie.imdbID
        result.Type = new_movie.Type
        db.commit()
        return JSONResponse(jsonable_encoder(result))


# db = Session()
# for movie in movies_list:
#     new_movie = MovieDbModel(**movie)
#     db.add(new_movie)
#     db.commit()
