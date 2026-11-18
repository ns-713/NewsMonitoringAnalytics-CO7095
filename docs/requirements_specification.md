# Software Requirements Specification (SRS)
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) establishes the formal functional and non-functional requirements for the **News Monitoring and Analytics Application**, developed for the **CO7095 Software Measurement and Quality Assurance** module at the University of Leicester (Academic Year 2026–2027). The system is an offline-capable, backend-focused Python CLI application designed to automate news article intake, classification, lexical sentiment analysis, duplicate detection, temporal and source trend analytics, and keyword monitoring alerts without reliance on paid APIs or external database services.

### 1.2 Intended Audience
- **Course Assessors & Module Leaders**: Evaluating adherence to software quality assurance standards, verification rigor, and measurement frameworks.
- **Development Team Members (ns713, Sd683, Jb1080, Pj161)**: Implementing, testing, and maintaining core functional modules.
- **Academic Peer Reviewers**: Examining software measurement, symbolic execution, and concolic test generation.

### 1.3 Scope and Objectives
The application fulfills the following core objectives:
1. Automated and manual collection of news articles using standard XML RSS feeds and local input.
2. Robust, atomic local persistence utilizing structured JSON storage.
3. Multi-criteria querying and case-insensitive search across headlines, content, dates, and metadata.
4. Deterministic, rule-based categorisation and lexical sentiment analysis with zero AI/ML marketing exaggeration.
5. Multi-tier duplicate detection combining URL normalisation, headline normalisation, lexical token fingerprinting, and Jaccard similarity metrics.
6. Temporal, source, and topic analytics with formatted tabular CLI dashboards and CSV export capabilities.
7. Continuous keyword monitoring with configurable rules and unread notification tracking.
8. Complete testability under black-box, white-box, symbolic execution, and concolic testing frameworks.

---

## 2. Overall Description

### 2.1 Product Perspective
The system operates as an autonomous, self-contained Python 3 CLI program. It avoids external database servers (e.g., PostgreSQL, MongoDB), commercial cloud APIs, and web frameworks (Django, Flask), fulfilling coursework guidelines that require execution on standard university lab workstations running PyCharm.

```
+-------------------------------------------------------------+
|                  Interactive CLI Menu (menu.py)             |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|                     Service Layer                           |
|  - NewsService        - RssService       - SearchService    |
|  - SentimentService   - Categorisation   - DuplicateService |
|  - TrendService       - SourceAnalytics  - TimeAnalytics    |
|  - AlertService       - ReportService    - DashboardService |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|              Storage & Data Layer (json_storage.py)         |
|  - articles.json      - sources.json                        |
|  - alert_rules.json   - alerts.json    - demo_news.json     |
+-------------------------------------------------------------+
```

### 2.2 User Characteristics
- **Standard User**: Ingests RSS feeds, executes keyword searches, explores sentiment profiles, and exports CSV reports.
- **QA / Test Engineer**: Executes unit test suites, verifies path coverage, assesses symbolic execution constraints, and audits process artifacts.

### 2.3 Operating Environment & Constraints
- **Platform**: Operating System agnostic (Windows 10/11, Linux, macOS).
- **Runtime**: Python 3.10+ (Standard Library preferred).
- **IDE**: PyCharm Community or Professional Edition.
- **Persistence**: Atomic local JSON files with `.bak` recovery support.
- **Cost**: 100% Free and Open Source; zero commercial API dependencies.

---

## 3. Specific Functional Requirements

| Requirement ID | Requirement Name | Description | Traceability / Story |
| :--- | :--- | :--- | :--- |
| **FR01** | **News Article Management** | Manage standard `NewsArticle` models with unique IDs, required field validation (headline, source, URL), update, view, and deletion operations. | US01, US02, US25 |
| **FR02** | **News Source Management** | Register, inspect, validate, and remove RSS news feeds and source metadata with URL scheme validation (`http://`, `https://`, `file://`). | US03 |
| **FR03** | **RSS News Collection** | Resilient XML feed downloading and parsing using `urllib` and `ElementTree`. Isolates network timeouts and malformed XML; provides offline demo fallback. | US13, US14, US15, US26 |
| **FR04** | **News Search & Filter** | Case-insensitive multi-field search across headline, description, content, source, category, sentiment, and publication date intervals. | US04, US05, US18, US29 |
| **FR05** | **Rule-Based Categorisation** | Deterministic keyword dictionary matching across 10 categories + "Other". Reports triggering terms; strictly non-machine-learning. | US06, US17, US28 |
| **FR06** | **Sentiment Analysis** | Lexical sentiment scoring: $\text{Score} = \text{Pos} - \text{Neg}$. Classifies into Positive, Negative, or Neutral with explicit lexical audit trails. | US16, US28 |
| **FR07** | **Duplicate Detection** | Multi-level duplicate screening: Exact URL, Normalised URL, Normalised Headline, Token Fingerprint, and Jaccard Similarity ($\theta \ge 0.70$). | US08, US20, US33 |
| **FR08** | **Trending Analytics** | Token frequency counting excluding configurable stop words; identifies top 10 trending terms and date-to-date topic velocity. | US07, US19, US32 |
| **FR09** | **Source Analytics** | Quantifies source ingestion counts, category distributions, and sentiment profiles. Explicitly disclaims credibility judgments. | US09, US21, US33 |
| **FR10** | **Time-Based Analytics** | Computes daily, weekly (ISO calendar), and monthly news volumes and sentiment evolution across temporal buckets. | US31 |
| **FR11** | **Keyword Monitoring** | User-defined alert rules matching keywords and optional category constraints; triggers notification records. | US10, US22 |
| **FR12** | **Alert Management** | View alert queues, inspect matching headlines, transition status from UNREAD to READ, and prevent repeated duplicate alerts. | US22, US23, US34 |
| **FR13** | **Reporting & CSV Export** | Generates tabular summaries in terminal and exports structured CSV files for articles, categories, sources, trends, alerts, and duplicates. | US24, US35 |
| **FR14** | **Interactive Dashboard** | Consolidated real-time terminal dashboard reporting total articles, active rules, unread alerts, sentiment breakdown, and top categories. | US11, US34, US36 |
| **FR15** | **Data Persistence & Recovery** | Atomic writes using temporary files and atomic renaming; creates `.bak` backups and automatically recovers from corrupted JSON. | US12, US25 |

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Performance & Scalability
- **NFR01**: Cold startup time under 1.5 seconds on university lab hardware.
- **NFR02**: Ingestion of offline demo dataset (105+ articles) completing in under 2.0 seconds.
- **NFR03**: Search queries over 1,000 articles returning results in under 50 milliseconds.

### 4.2 Reliability & Fault Tolerance
- **NFR04**: Network timeouts or malformed XML in one RSS feed must never crash the application or prevent other feeds from processing.
- **NFR05**: Corrupted JSON storage files must automatically trigger recovery from `.bak` backup files.
- **NFR06**: File writing must be atomic (`os.replace`) to prevent zero-byte truncation on power interruption.

### 4.3 Maintainability & Code Quality
- **NFR07**: Standard compliance with PEP 8 style guidelines, full type annotations, and descriptive docstrings.
- **NFR08**: Modular separation of concerns across models, services, storage, and interface packages.
- **NFR09**: Comprehensive testability targeting > 85% statement coverage across core business services.

### 4.4 Usability & Portability
- **NFR10**: Zero third-party runtime package requirements (100% Python Standard Library execution).
- **NFR11**: Clear numbered menu options with keyboard cancellation, back navigation, and formatted ASCII tables.
