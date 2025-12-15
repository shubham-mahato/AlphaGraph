# AlphaGraph Data Model (Graph Schema)

**Version:** 1.0.0
**Status:** Frozen for v1 Implementation

This document defines the strict ontology for the AlphaGraph Neo4j database. The model follows a **Company-Centric** design, where events act as external modifiers to the market topology.

---

## 1. Visual Schema Overview

This diagram represents the allowable nodes and relationships within the system.

```mermaid
erDiagram
    Event ||--|{ Company : AFFECTS
    Company }|--|| Sector : BELONGS_TO
    Company }|--|| Index : MEMBER_OF
    Company }|--|{ Company : CORRELATED_WITH

    Event {
        string event_id PK
        string title
        float sentiment
        datetime timestamp
        string event_type
        string source
    }

    Company {
        string ticker PK
        string name
        float market_cap
        float beta
        string country
    }

    Sector {
        string name PK
    }

    Index {
        string symbol PK
        string name
    }