import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# Load Env
load_dotenv(ROOT_DIR / "backend" / ".env")

def print_status(component, status, message=""):
    icon = "✅" if status else "❌"
    print(f"{icon} [{component}] {message}")

def check_env_vars():
    required = ["NEO4J_URI", "NEO4J_PASSWORD", "NEWS_API_KEY"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        print_status("Environment", False, f"Missing keys: {missing}")
    else:
        print_status("Environment", True, "All keys present")

def check_docker_container():
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if "alphagraph-neo4j" in result.stdout:
            print_status("Docker", True, "Neo4j container is running")
            return True
        else:
            print_status("Docker", False, "Container 'alphagraph-neo4j' not found in running list")
            return False
    except Exception:
        print_status("Docker", False, "Could not run 'docker ps'. Is Docker installed?")
        return False

def check_neo4j_connection():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print_status("Neo4j DB", True, f"Connected to {uri}")
        driver.close()
    except Exception as e:
        print_status("Neo4j DB", False, f"Connection failed: {e}")

def check_nlp_pipeline():
    try:
        from nlp_services.pipelines.news_event_pipeline import NewsEventPipeline  
        pipeline = NewsEventPipeline()
        
        # Test Data
        dummy_article = {
            "title": "TCS announces strong Q4 results",
            "description": "Revenue up 10%, beating estimates.",
            "publishedAt": "2025-01-01T10:00:00Z",
            "content": "Tata Consultancy Services (TCS) performed well."
        }
        
        event = pipeline.process_article(dummy_article)
        
        if "TCS" in event.mentioned_entities and event.event_type == "earnings":
            print_status("NLP Service", True, "Pipeline correctly processed dummy article")
        else:
            print_status("NLP Service", False, f"Unexpected output: {event}")
            
    except ImportError as e:
        print_status("NLP Service", False, f"Import Error (Check folder structure): {e}")
    except Exception as e:
        print_status("NLP Service", False, f"Pipeline crashed: {e}")

def check_files():
    # Check if raw news exists
    raw_dir = ROOT_DIR / "data_ingestion" / "raw" / "news"
    files = list(raw_dir.glob("*.json"))
    if files:
        print_status("Data Ingestion", True, f"Found {len(files)} raw news files")
    else:
        print_status("Data Ingestion", False, "No raw news files found (Run ingestor!)")

if __name__ == "__main__":
    print(f"🔍 Starting AlphaGraph System Diagnostic...\nRoot: {ROOT_DIR}\n")
    
    check_env_vars()
    if check_docker_container():
        check_neo4j_connection()
    check_files()
    check_nlp_pipeline()
    
    print("\nDiagnostic Complete.")