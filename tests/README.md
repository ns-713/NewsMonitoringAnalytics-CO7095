# CO7095 Test Architecture

In strict compliance with the **CO7095 Coursework Specification**, testing packages are structured both by individual team member responsibility and shared cross-cutting scopes:

## 1. Per-Member Test Packages
- **`ns713/test/`**: Nikitha Sarpur (Lead Architect & Ingestion) — Black-box (BVA, Category Partition, Decision Table, Random), White-box (Basis Path, Branch, Statement for models, storage, RSS), Symbolic & Concolic research suites.
- **`sd683/test/`**: Sashi Dommaraju (QA Lead) — Black-box, White-box, Symbolic & Concolic test suites for Search, Categorisation, and Lexical Sentiment.
- **`jb1080/test/`**: Jyothi Bandalapati (Measurement Lead) — Black-box, White-box, Symbolic & Concolic test suites for 4-Tier Deduplication and Temporal Analytics.
- **`pj161/test/`**: Jalakam Prashanth (System Integrator & CMMI) — Black-box, White-box, Symbolic & Concolic test suites for Keyword Alerts, Reporting, Input Handling, and CLI Dashboard.

## 2. Shared Integration & System Suites
- **`tests/shared/integration/`**: Cross-service interaction test suites (Ingestion to Alert pipeline, Deduplication integration, Analytics reporting).
- **`tests/shared/system/`**: End-to-end user journey simulation and data corruption recovery tests.

## 3. Running All Tests
To run all tests with statement coverage tracing:
```bash
python run_tests.py
```
Or via standard unittest / pytest:
```bash
pytest
```
