from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.movie import MovieDbModel
from config.database import Session


class MovieService():
    def __init__(self) -> None:
        self.db = Session()

    def get_all_movies(self):
        result = self.db.query(MovieDbModel).all()
        return JSONResponse(jsonable_encoder(result))

    def get_movie_by_title(self, title):
        result = self.db.query(MovieDbModel).filter(
            MovieDbModel.Title == title).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "Movie not found"})
        return JSONResponse(jsonable_encoder(result))

    def get_movies_by_genre(self, genre):
        result = self.db.query(MovieDbModel).filter(
            MovieDbModel.Genre.ilike(f"%{genre}"))
        if not result:
            return JSONResponse(status_code=404, content={"message": "There no movie with that genre"})
        return JSONResponse(jsonable_encoder(result))
