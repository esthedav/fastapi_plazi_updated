from fastapi import Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from MovieBaseModel import Movie
from typing import List
# Database imports
from config.database import Session
from models.movie import MovieDbModel
# Middlewares
from middlewares.jwt_bearer import JWTBearer
# Services
from services.movies import MovieService

from movies import movies_list


movies_router = APIRouter()


@movies_router.get("/movies", tags=["movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer)])
def get_all_movies():
    return MovieService().get_all_movies()


@movies_router.get("/movies/{movie_title}", tags=["movies"], response_model=Movie)
def get_movies_by_title(movie_title: str = Path(min_length=2)):
    return MovieService().get_movie_by_title(movie_title)


@movies_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_genre(genre: str = Query(min_length=4)):
    return MovieService().get_movies_by_genre(genre)


@movies_router.post("/add-movie", tags=["movies"])
def add_movie(movie: Movie):
    db = Session()
    new_movie = MovieDbModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    movies_list.append(movie.model_dump())
    return JSONResponse(movies_list)


@movies_router.delete("/delete-movie/", tags=["movies"])
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


@movies_router.put("/update/movie/{title}", tags=["movies"])
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
