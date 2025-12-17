import json
import os
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv

# --- Configuration ---
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parents[1]
ENV_PATH = ROOT_DIR / "backend" / ".env"

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

DATA_DIR = CURRENT_DIR.parent
COMPANIES_PATH = DATA_DIR / "companies.json"

def load_companies():
    """Read the JSON file."""
    if not COMPANIES_PATH.exists():
        raise FileNotFoundError(f"Could not find {COMPANIES_PATH}")
    
    with open(COMPANIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def seed_companies_and_sectors(driver, companies):
    """Insert Companies and Sector Nodes."""
    print(f"Seeding {len(companies)} Companies...")

    # Extract Unique Sectors
    sectors = sorted({c["sector"] for c in companies})

    with driver.session() as session:
        # 1. Create Sectors
        for sector in sectors:
            session.run("MERGE (s:Sector {name: $name})", name=sector)

        # 2. Create Companies and link to Sectors
        for company in companies:
            # Create company node
            query_company = """
                MERGE (c:Company {ticker: $ticker})
                SET c.name = $name,
                    c.sector = $sector,
                    c.country = $country,
                    c.exchange = $exchange
            """
            session.run(query_company, **company)

            # Create Relationship: (Company)-[:BELONGS_TO]->(Sector)
            query_rel = """
                MATCH (c:Company {ticker: $ticker})
                MATCH (s:Sector {name: $sector})
                MERGE (c)-[:BELONGS_TO]->(s)
            """
            session.run(
                query_rel,
                ticker=company["ticker"],
                sector=company["sector"]
            )

def seed_dummy_events(driver):
    """Creating fake events to test the API."""
    print("Seeding dummy events...")

    dummy_events = [
        {
            "event_id": "EVT-001",
            "title": "RBI introduces new capital requirements",
            "description": "New norms expected to impact private banks.",
            "timestamp": "2025-12-15T09:00:00",
            "sentiment": -0.7,
            "source": "DummySeed",
            "event_type": "regulation",
            "tickers": ["HDFCBANK", "ICICIBANK"],
        },
        {
            "event_id": "EVT-002",
            "title": "TCS beats Q4 earnings expectations",
            "description": "Revenue up 15% YoY.",
            "timestamp": "2025-12-14T18:30:00",
            "sentiment": 0.8,
            "source": "DummySeed",
            "event_type": "earnings",
            "tickers": ["TCS"],
        },
    ]

    with driver.session() as session:
        for ev in dummy_events:
            # 1. Create Event node
            # We filter out 'tickers' because that's not a property of the event node
            event_props = {k: v for k, v in ev.items() if k != "tickers"}
            
            query_event = """
                MERGE (e:Event {event_id: $event_id})
                SET e += $props,
                    e.timestamp = datetime($timestamp)
            """
            session.run(
                query_event,
                event_id=ev["event_id"],
                timestamp=ev["timestamp"],
                props=event_props
            )

            # 2. Link Event to Companies: (Event)-[:AFFECTS]->(Company)
            for ticker in ev["tickers"]:
                query_link = """
                    MATCH (e:Event {event_id: $event_id})
                    MATCH (c:Company {ticker: $ticker})
                    MERGE (e)-[:AFFECTS]->(c)
                """
                session.run(
                    query_link,
                    event_id=ev["event_id"],
                    ticker=ticker,
                )

def main():
    if NEO4J_PASSWORD == "password" or NEO4J_PASSWORD == "changeme":
        print("⚠️  WARNING: You are using the default password. Ensure Neo4j is set up correctly.")

    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        # Verify connection
        driver.verify_connectivity()
        print(f"✅ Connected to Neo4j at {NEO4J_URI}")
        
        companies = load_companies()
        
        seed_companies_and_sectors(driver, companies)
        seed_dummy_events(driver)
        
        print("\n🎉 Seeding complete! Data is in Neo4j.")  
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # We handle close inside the try/finally to ensure it happens even on error,
        # but only if driver was successfully created.
        if 'driver' in locals():
            driver.close()

if __name__ == "__main__":
    main()