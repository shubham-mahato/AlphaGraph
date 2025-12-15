from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
  PROJECT_NAME: str = "AlphaGraph API"
  API_V1_STR: str = "/api/v1"
  VERSION: str = "0.1.0"

  BACKEND_CORS_ORIGINS: List[str] = [
    "https://localhost/3000",
    "http://localhost:8000",
  ]

  NEO4J_URI: str = "bold://localhost:7687"
  NEO4J_USER:str = "neo4j"
  NEO4J_PASSWORD:str = "password"

  class Config:
    case_sensitive = True
    env_file = ".env"

settings =Settings()
