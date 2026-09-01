
from fastapi import FastAPI
from routers.users import router as user_router
from database import engine, Base
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
    )

