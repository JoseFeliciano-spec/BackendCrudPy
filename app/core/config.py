from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()
class Settings(BaseModel):
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name: str = os.getenv("MONGODB_DB", "crud_db")
    jwt_secret: str = os.getenv("JWT_SECRET", "todo")
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 1440

settings = Settings()
