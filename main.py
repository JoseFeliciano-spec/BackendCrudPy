from fastapi import FastAPI
from app.api.v1.auth_router import router as auth_router
from app.api.v1.product_router import router as product_router;
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BackendCrudPy", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Permite cualquier origen
    allow_credentials=True,     # Permite cookies/tokens
    allow_methods=["*"],        # Permite todos los métodos (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],        # Permite todos los headers (Authorization, Content-Type, etc.)
)

app.include_router(product_router)
app.include_router(auth_router)
