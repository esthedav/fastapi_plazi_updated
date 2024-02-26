from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# Database imports
from config.database import engine, Base
# Middlewares
from middlewares.error_handler import ErrorHandler
# Routers
from routers.movies_route import movies_router
from routers.user_route import user_route

from index import index_html


app = FastAPI()
app.title = "My app"
app.version = "1.0.0"
app.add_middleware(ErrorHandler)
app.include_router(movies_router)
app.include_router(user_route)


Base.metadata.create_all(bind=engine)


@app.get("/", tags=["home"])
def message():
    return HTMLResponse(index_html)


# db = Session()
# for movie in movies_list:
#     new_movie = MovieDbModel(**movie)
#     db.add(new_movie)
#     db.commit()
