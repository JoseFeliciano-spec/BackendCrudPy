from fastapi import FastAPI
from app.api.v1.auth_router import router as auth_router

app = FastAPI(title="BackendCrudPy", version="1.0.0")
app.include_router(auth_router)
