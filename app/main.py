# FastAPI
from fastapi import FastAPI

# Routers
from app.routers import breeds, users


app = FastAPI()


# Register routers
app.include_router(breeds.router, prefix="/breeds", tags=["Breeds"])
app.include_router(users.router, prefix="/users", tags=["Users"])
