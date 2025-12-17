import os
from typing import Optional
from neo4j import GraphDatabase, Driver
from app.config import settings

_driver: Optional[Driver] = None
def init_driver()->None:
  """Initializes the Neo4j driver connection."""
  global _driver
  if _driver is None:
    try:
      _driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER,settings.NEO4J_PASSWORD)
      )
      _driver.verify_connectivity()
      print(f"✅ Verified Neo4j connection at {settings.NEO4J_URI}")
    except Exception as e:
      print(f"❌ Failed to connect to Neo4j: {e}")
      raise e
    
def get_driver()->Driver:
  """Return active driver instance"""
  if _driver is None:
    raise RuntimeError("Neo4j driver is not initialized. Call init_driver() first")
  return _driver

def close_driver()-> None:
  """Closes the driver connection."""
  global _driver
  if _driver is not None:
    _driver.close()
    _driver=None
    print("🔒 Neo4j driver closed.")