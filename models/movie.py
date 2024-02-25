from config.database import Base
from sqlalchemy import Column, String


class MovieDbModel(Base):

    __tablename__ = "movies"

    Title = Column(String, primary_key=True)
    Year = Column(String)
    Rated = Column(String)
    Released = Column(String)
    Runtime = Column(String)
    Genre = Column(String)
    Director = Column(String)
    Writer = Column(String)
    Actors = Column(String)
    Plot = Column(String)
    Language = Column(String)
    Country = Column(String)
    Awards = Column(String)
    Poster = Column(String)
    Metascore = Column(String)
    imdbRating = Column(String)
    imdbVotes = Column(String)
    imdbID = Column(String)
    Type = Column(String)
