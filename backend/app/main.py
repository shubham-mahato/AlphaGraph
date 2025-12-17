import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import company_router
from app.db.neo4j_client import init_driver,close_driver
from app.config import settings

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

  """
    Application Life-cycle Manager.
    Handles startup (DB connections, model loading) and shutdown (cleanup).
  """

  logger.info("AlphaGraph is starting up ....")
  init_driver()

  yield

  close_driver()

  logger.info("AlphaGraph is shutting down ...")


def get_application()-> FastAPI:

  application =FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Financial Knowledge Graph & Shock Simulator API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
  )
  # Config CORS

  application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials =True,
    allow_methods = ["*"],
    allow_headers =["*"]
  )
  application.include_router(company_router.router)
  
  return application
app = get_application()

@app.get("/health", tags=["System"])
async def health_check():
    """
    Liveness probe to ensure the service is responsive.
    """
    return {
        "status": "active",
        "version": settings.VERSION,
        "environment": "development"
    }

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint for quick connectivity test.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs_url": "/docs"
    }