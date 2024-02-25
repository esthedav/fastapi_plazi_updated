from pydantic import BaseModel, Field

class Movie(BaseModel):
    Title: str
    Year: str  = Field(min_length=4, max_length=4)
    Rated: str
    Released: str
    Runtime: str
    Genre: str
    Director: str
    Writer: str
    Actors: str
    Plot: str
    Language: str
    Country: str
    Awards: str
    Poster: str
    Metascore: str
    imdbRating: str
    imdbVotes: str
    imdbID: str
    Type: str
    
    class Config:
        json_schema_extra = {
            "example" : {
                "Title": "Movie Title",
                "Year": "1900",
                "Rated": "PG",
                "Released": "18 Dec 1900",
                "Runtime": "162 min",
                "Genre": "null, null, null",
                "Director": "Director",
                "Writer": "Writer",
                "Actors": "Actor, Actor, Actor",
                "Plot": "A Movie Plot",
                "Language": "Language, Language",
                "Country": "CTRY, CTRY",
                "Awards": "Awards",
                "Poster": "Poster Link",
                "Metascore": "88",
                "imdbRating": "8.8",
                "imdbVotes": "888,888",
                "imdbID": "default",
                "Type": "movie",
                }
            }
