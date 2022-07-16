from fastapi import FastAPI

from src.main.routes.users_routes import users_router

from src.main.routes.courses_routes import courses_router
from src.main.routes.sections_routes import sections_router


# user.Base.metadata.create_all(bind=engine)
# course.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API LMS",
    description="LMS for managing students and courses.",
    version="0.0.1",
    contact={
        "name": "Paulo",
        "email": "paulosilvadosreis2057@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)


app.include_router(users_router)
app.include_router(courses_router)
app.include_router(sections_router)
