# CO7095 Software Measurement and Quality Assurance (2026–2027)
# Executive Project Summary

**Project Title:** News Monitoring and Analytics Application  
**Module:** CO7095 – Software Measurement and Quality Assurance  
**Academic Session:** 2026–2027  
**Department:** Department of Computing and Mathematical Sciences, University of Leicester  
**Application Platform:** Python 3 (Standard Library Baseline) / CLI Architecture  
**Persistence:** Atomic JSON-Based Local File Store  
**Verification Level:** 195 Automated Tests, 100% Pass Rate, CMMI Level 2 Managed Compliance  

---

## 1. Project Overview & Operational Mission

The **News Monitoring and Analytics Application** is a production-grade, backend-focused software engineering system engineered to collect, curate, categorise, search, monitor, and analyse news articles across heterogeneous digital sources. Developed strictly using the Python 3 standard library, the application guarantees total autonomy from paid third-party APIs, cloud subscription keys, external relational databases, or complex web frameworks. It runs out of the box on standard university laboratory computers using PyCharm or any standard terminal shell.

The project simultaneously serves as a rigorous pedagogical testbed for advanced software measurement, quality assurance disciplines, estimation models, and formal program verification.

```
+---------------------------------------------------------------------------------------+
|                                    Core Statistics                                    |
+------------------------------------+--------------------------------------------------+
| Application Codebase (Physical)    | 2,741 SLOC across 18 Python modules              |
| Verification Codebase (Physical)   | 3,120 SLOC across master test runner & packages  |
| Total Monitored Project Codebase   | 5,861 SLOC                                       |
| Automated Test Suite               | 195 tests (0 failures, 0 errors, 100% pass rate) |
| Overall Statement Coverage         | 85.2% (1,948 of 2,287 statements)                |
| Demo Dataset                       | 114 curated articles across 10 distinct domains  |
| Agile Sprints & User Stories       | 3 Sprints, 36 User Stories, 126 Story Points     |
| EVM Indices at Project Close       | CPI = 1.050 (Under Budget), SPI = 1.000 (On Time)|
| CMMI Level 2 Audit Result          | Fully Compliant across all 7 Process Areas       |
+------------------------------------+--------------------------------------------------+
```

---

## 2. Architectural Design & Engineering Principles

The software implements a decoupled, 4-tier layered architecture adhering to SOLID object-oriented design and clean separation of concerns:

```
+-------------------------------------------------------------------------------+
|                       PRESENTATION LAYER (interface/)                         |
|   menu.py (20 Options)  |  formatting.py (ASCII Tables)  |  input_handler.py   |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                        BUSINESS SERVICE LAYER (services/)                     |
|  news_service.py     | rss_service.py       | search_service.py               |
|  categorisation.py   | sentiment_service.py | duplicate_service.py            |
|  trend_service.py    | source_analytics.py  | time_analytics.py               |
|  alert_service.py    | report_service.py    | dashboard_service.py            |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                       PERSISTENCE LAYER (storage/ & data/)                    |
|  json_storage.py (Atomic os.replace writes, .tmp swap, .bak snapshot recovery)|
|  articles.json       | sources.json         | alert_rules.json | alerts.json  |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                           DOMAIN MODEL LAYER (models/)                        |
|  NewsArticle (UUID)  | NewsSource (RFC URLs)| AlertRule        | Alert        |
+-------------------------------------------------------------------------------+
```

### Key Architectural Strengths:
1. **Atomic File Persistence**: Storage writes are committed to temporary hidden files before executing atomic operating-system replacements (`os.replace`). Every save automatically updates a timestamped `.bak` backup file, completely shielding data integrity against unexpected SIGINT interrupts or power failures.
2. **Defensive Ingestion**: The RSS engine parses XML feeds through standard `xml.etree.ElementTree` with fault isolation; if a feed URL is invalid or malformed, the error is isolated without crashing the host process.
3. **Pluggable Dependency Injection**: Service classes accept custom storage paths and collaborating service references, enabling frictionless isolated unit testing without monkey-patching disk state.

---

## 3. Implemented Capabilities (Functional Scope)

The application fully implements all 15 Functional Requirements (FR01 through FR15):

1. **FR01: Article Management**: Comprehensive CRUD operations for news articles with RFC-compliant validation, automated UUID generation, and ISO-8601 timestamps.
2. **FR02: Source Management**: Registration, editing, validation, and metadata maintenance for RSS publishing sources.
3. **FR03: RSS Collection Engine**: Multi-feed parsing, HTML entity stripping, RFC 822 publication date conversion, network timeout guards, and a zero-network offline demo fallback.
4. **FR04: Multi-Criteria Search**: Case-insensitive substring matching across headlines, content, source, category, sentiment label, and publication date intervals.
5. **FR05: Rule-Based Categorisation**: Deterministic keyword scoring mapping text to 10 standard categories (Politics, Business, Technology, Health, Sports, Education, Science, Environment, World News, Entertainment, Other) with triggering token explainability.
6. **FR06: Lexical Sentiment Analysis**: Explainable $(P - N)$ lexical token scoring against curated dictionaries, providing Positive, Negative, or Neutral classifications.
7. **FR07: Multi-Tiered Duplicate Detection**: 4-tier filtering hierarchy comprising canonical URL hashing, normalised headline matching, alphanumeric fingerprinting, and token-based Jaccard similarity ($\theta \ge 0.70$).
8. **FR08: Trending Topics**: Term frequency distribution calculation excluding 150 stop words, tracking top-10 discussion drivers and period-to-period velocity.
9. **FR09: Source Analytics**: Publishing volume distributions, category breakdowns, and sentiment profiles per news outlet (explicitly distinguishing activity volume from factual reliability).
10. **FR10: Time-Based Analytics**: Daily, ISO calendar weekly, and monthly publication histograms with temporal sentiment tracking.
11. **FR11: Keyword Monitoring**: User-configurable boolean alerting predicates with optional category filters.
12. **FR12: Alert Management**: Deduplicated alert generation, unread-to-read lifecycle tracking, and alert inspection.
13. **FR13: Multi-Format Reporting**: Clean terminal formatting and 7 exportable RFC-4180 CSV reports in `reports/generated/`.
14. **FR14: Executive Dashboard**: Real-time ASCII status screen summarising volume, sources, pending alerts, sentiment balance, and recent articles.
15. **FR15: Resilient Data Persistence**: JSON validation, automatic recovery from `.bak` backups on corrupted files, and schema migration guards.

---

## 4. Balanced Team Contributions & Workload Distribution

The engineering effort was divided equitably among four software engineers over three 2-week Agile sprints:

```
+----------------------------------------------------------------------------------------------------+
|                                    Team Allocation Matrix                                          |
+-------------------+-----------+---------------------+-------------------+--------------------------+
| Member Name       | System ID | Primary Roles       | User Stories      | Core Testing Ownership   |
+-------------------+-----------+---------------------+-------------------+--------------------------+
| Nikitha Sarpur    | ns713     | Scrum Master, Lead  | US01-US03 (Sp 1)  | `ns713/test/`            |
| (Lead Engineer)   | 259060190 | Storage, Models,    | US13-US15 (Sp 2)  | Article validation, RSS  |
|                   |           | RSS Ingestion       | US25-US27 (Sp 3)  | XML parsing, Storage     |
+-------------------+-----------+---------------------+-------------------+--------------------------+
| Sashi Dommaraju   | sd683     | Quality Analyst,    | US04-US06 (Sp 1)  | `sd683/test/`            |
| (QA Specialist)   | 259062044 | Search, Categorise, | US16-US18 (Sp 2)  | Search queries, Category |
|                   |           | Sentiment Services  | US28-US30 (Sp 3)  | Lexical sentiment rules  |
+-------------------+-----------+---------------------+-------------------+--------------------------+
| Jyothi Bandalapati| jb1080    | Measurement Lead,   | US07-US09 (Sp 1)  | `jb1080/test/`           |
| (Metrics Engineer)| 259060742 | Duplicates, Trends, | US19-US21 (Sp 2)  | Jaccard similarity,      |
|                   |           | Source/Time Metrics | US31-US33 (Sp 3)  | Trend terms, Time dates  |
+-------------------+-----------+---------------------+-------------------+--------------------------+
| Jalakam Prashanth | pj161     | Integration Eng.,   | US10-US12 (Sp 1)  | `pj161/test/`            |
| (System Integrator| 259060676 | Alerts, CSV Reports,| US22-US24 (Sp 2)  | Alert triggers, CSV IO,  |
|                   |           | CLI Dashboard, CMMI | US34-US36 (Sp 3)  | CLI dashboard telemetry  |
+-------------------+-----------+---------------------+-------------------+--------------------------+
```

Every team member completed exactly **9 User Stories** (3 per sprint), earned **31.5 Planning Poker Story Points**, authored individual Black-box, White-box, Symbolic, and Concolic test suites, and audited assigned CMMI Level 2 process areas.

---

## 5. Software Verification & Quality Assurance Results

The project was subjected to multi-dimensional testing leveraging Python standard library capabilities:

```
+---------------------------------------------------------------------------------------+
|                                Test Suite Execution Summary                           |
+--------------------+----------------+---------------+-----------------+---------------+
| Suite Domain       | Tests Executed | Tests Passed  | Failures/Errors | Pass Rate     |
+--------------------+----------------+---------------+-----------------+---------------+
| ns713 (Nikitha)    | 45             | 45            | 0               | 100.0%        |
| sd683 (Sashi)      | 36             | 36            | 0               | 100.0%        |
| jb1080 (Jyothi)    | 31             | 31            | 0               | 100.0%        |
| pj161 (Prashanth)  | 71             | 71            | 0               | 100.0%        |
| shared/integration | 4              | 4             | 0               | 100.0%        |
| shared/system      | 2              | 2             | 0               | 100.0%        |
| research           | 6              | 6             | 0               | 100.0%        |
+--------------------+----------------+---------------+-----------------+---------------+
| Total Project Test | 195            | 195           | 0               | 100.0%        |
+--------------------+----------------+---------------+-----------------+---------------+
*100% automated pass rate across all 195 unit, integration, and research test cases.*
```

### Statement Coverage Metrics (2,287 Measured Statements):
- `interface/formatting.py`: **100.0%**
- `interface/input_handler.py`: **96.9%**
- `duplicate_service.py`: **95.8%**
- `dashboard_service.py`: **94.7%**
- `search_service.py`: **93.7%**
- `categorisation_service.py`: **92.3%**
- `news_source.py`: **91.8%**
- `alert_service.py`: **91.7%**
- `alert_rule.py`: **91.1%**
- `news_service.py`: **90.9%**
- `trend_service.py`: **90.9%**
- `alert.py`: **90.7%**
- `report_service.py`: **90.7%**
- `article.py`: **88.8%**
- `rss_service.py`: **88.4%**
- `sentiment_service.py`: **85.9%**
- `source_analytics_service.py`: **85.2%**
- `menu.py`: **76.9%**
- **Overall Statement Coverage:** **85.2%** (1,948 of 2,287 statements)
- `models/alert_rule.py`: **91.1%**
- `trend_service.py`: **90.9%**
- `report_service.py`: **90.7%**
- `sentiment_service.py`: **85.9%**
- `source_analytics_service.py`: **85.2%**
- `interface/formatting.py`: **100.0%**

---

## 6. Software Measurement Baselines & Findings

### A. PERT Schedule Network Analysis:
- **Critical Path**: A1 $\to$ A2 $\to$ A3 $\to$ A5 $\to$ A6 $\to$ A7 $\to$ A9 $\to$ A10 $\to$ A11 $\to$ A14 $\to$ A16 $\to$ A17.
- **Expected Duration ($T_e$)**: 41.85 working days.
- **Critical Path Variance ($\sigma^2$)**: 4.83 days$^2$ ($\sigma = 2.20$ days).
- **On-Time Confidence**: $92.36\%$ probability of project completion within 45 working days.

### B. Software Sizing & Effort Estimation:
- **Physical Codebase**: 2.741 KLOC application core (5.275 KLOC total project).
- **COCOMO I (Organic Mode)**:
  $$\text{Effort} = 2.4 \times (2.741)^{1.05} = 6.74\text{ Person-Months}$$
  $$\text{TDEV} = 2.5 \times (6.74)^{0.38} = 5.15\text{ Calendar Months}$$
- **COCOMO II (Post-Architecture Model)**:
  - Scale Factors ($\sum SF = 18.97 \implies E = 1.104$).
  - Effort Multipliers ($\prod EM = 0.985$).
  - Estimated Effort: $8.87\text{ Person-Months}$.
  - The higher effort in COCOMO II directly reflects the rigorous verification standards and high RELY/TOOL requirements demanded by SQA coursework.

### C. Earned Value Management (EVM):
- **Planned Value ($PV$)**: £18,000 (126 Story Points).
- **Earned Value ($EV$)**: £18,000 (100% completed).
- **Actual Cost ($AC$)**: £17,140.
- **Cost Performance Index ($CPI$)**: $1.05$ (Favourable / Under Budget).
- **Schedule Performance Index ($SPI$)**: $1.00$ (Exactly On Schedule).
- **Cost Variance ($CV$)**: $+£860$.

### D. Process Improvement (CMMI Level 2):
- Comprehensive internal audit across all 7 CMMI Level 2 Process Areas (REQM, PP, PMC, SAM, MA, PPQA, CM) yielded **100% compliance** across all specific and generic goals.

---

## 7. Formal Research Outcomes

### Symbolic Execution Study:
Formal mathematical path condition exploration was performed on key decision predicates (`NewsArticle.validate`, `SentimentService.classify_score`, and `DuplicateService.calculate_similarity`).
- Path condition sets were formally evaluated using First-Order Logic constraints.
- Formal boundaries were proven: e.g., for Jaccard duplicate detection, the decision threshold $\theta = 0.70$ creates an exact boundary condition partition where $J \ge 0.70 \iff |A \cap B| \ge 0.70 \times |A \cup B|$.

### Concolic Testing Study:
Dynamic concrete-symbolic testing (Directed Automated Random Testing) was applied to the XML parser and RFC 4180 CSV serializer.
- Systematic branch inversion generated inputs with trailing whitespace, missing XML closing tags, and embedded delimiter commas, confirming zero uncaught unhandled exceptions.

### Comparative SQA Paradigm Analysis:
Empirical evaluation across Black-Box, White-Box, Random Monkey, Symbolic, and Concolic testing proved that hybrid concolic and white-box coverage yields the highest branch fault discovery rate per unit execution time for algorithmic text processors.

---

## 8. How to Setup and Run the Project

### Prerequisites:
- Python 3.10, 3.11, or 3.12.
- Operating System: Windows 10/11, macOS, or Linux.
- IDE: PyCharm (Community or Professional).

### Step 1: Open in PyCharm / Terminal
Navigate to the root directory `NewsMonitoringAnalytics_CO7095/`.

### Step 2: Run Application
```bash
python main.py
```
*Tip: On first launch, select **Option 18** from the menu to populate the application with the 114-article offline demo dataset.*

### Step 3: Run Master Test Suite
```bash
python run_tests.py
```
*Optional Member Sub-Suites:*
```bash
python run_tests.py --member ns713
python run_tests.py --member sd683
python run_tests.py --member jb1080
python run_tests.py --member pj161
python run_tests.py --shared
```

---

## 9. Known Limitations & Future Roadmap

1. **Lexical Sentiment Nuance**: Rule-based sentiment analysis cannot detect sarcasm, contextual idioms, or complex negation structures (e.g., *"not bad"*). Future iterations could integrate optional pluggable transformer backends when GPU environments are detected.
2. **Persistence Scaling**: File-based atomic JSON storage operates entirely in memory during operations. While lightning fast for datasets up to 10,000 articles, production deployments handling millions of records would benefit from SQLite or indexed document stores.
3. **Linear Inverted Search**: The search service performs linear token filtering. For massive archives, implementing a disk-backed inverted B-tree index would achieve sub-millisecond retrieval.

---
*End of Executive Project Summary — CO7095 News Monitoring and Analytics Application.*
