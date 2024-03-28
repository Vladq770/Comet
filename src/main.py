from fastapi import FastAPI
from router import router as repo_router


app = FastAPI()
app.include_router(repo_router)

