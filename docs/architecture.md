# AlphaGraph Architecture Reference

**Version:** 1.0.0  
**Status:** Active Development  
**Last Updated:** December 2025

---

## 1. Executive Summary

**AlphaGraph** is a financial knowledge graph platform designed to model the complex interdependencies between market entities. By treating financial news and market events as first-class graph nodes, AlphaGraph enables:
1.  **Contextual Analysis:** Visualization of relationships between Companies, Sectors, and Events.
2.  **Shock Propagation:** Simulation of how impactful events (e.g., regulatory changes, earnings) cascade through the market.
3.  **Future-Ready Querying:** A foundation for GraphRAG (Retrieval-Augmented Generation) to answer natural language financial queries.

The system follows a uni-directional data flow: **Ingestion $\rightarrow$ NLP Processing $\rightarrow$ Graph Storage $\rightarrow$ API $\rightarrow$ Visualization**.

---

## 2. System Architecture

### 2.1 High-Level Component Diagram

The system is composed of five decoupled layers. Communication is handled via strict data contracts (JSON/Pydantic).

```mermaid
graph TD
    subgraph Data_Layer [Data Ingestion Layer]
        NewsAPI[News Sources]
        MarketData[Market Data / yFinance]
        IngestScripts[Ingestion Scripts]
    end

    subgraph NLP_Layer [NLP Service]
        Cleaner[Text Cleaner]
        NER[Entity Recognition (spaCy)]
        Sent[Sentiment Analysis (FinBERT)]
        Mapper[Entity Mapper]
    end

    subgraph Storage_Layer [Graph Store]
        Neo4j[(Neo4j Database)]
    end

    subgraph Backend_Layer [Backend API]
        FastAPI[FastAPI Server]
        GraphService[Graph Service]
        ShockEngine[Shock Simulation Engine]
    end

    subgraph UI_Layer [Frontend]
        NextJS[Next.js Client]
        Viz[Graph Visualization]
    end

    NewsAPI --> IngestScripts
    MarketData --> IngestScripts
    IngestScripts -->|Raw JSON| Cleaner
    Cleaner --> NER --> Sent --> Mapper
    Mapper -->|Structured Events| Neo4j
    
    FastAPI -->|Cypher Queries| Neo4j
    GraphService --> FastAPI
    ShockEngine --> FastAPI
    
    NextJS -->|REST API| FastAPI