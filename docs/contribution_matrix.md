# Team Contribution and Responsibility Matrix
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Balanced Team Responsibility Overview

All four group members contributed across the entire development lifecycle:
- Python Core Engineering
- Agile User Story Design
- Black-Box Specification Testing
- White-Box Structural Testing
- Symbolic Execution & Concolic Research
- Code Reviews, Documentation, and Process Audits

*No member was allocated solely to documentation or solely to testing.*

---

## 2. Four-Member Detailed Contribution Matrix

| Dimension | Member 1: Nikitha Sarpur (`ns713`) | Member 2: Sashi Dommaraju (`Sd683`) | Member 3: Jyothi Bandalapati (`Jb1080`) | Member 4: Jalakam Prashanth (`Pj161`) |
| :--- | :--- | :--- | :--- | :--- |
| **University Identifier** | `ns713` (ID: 259060190) | `Sd683` (ID: 259062044) | `Jb1080` (ID: 259060742) | `Pj161` (ID: 259060676) |
| **Email Address** | `ns713@student.le.ac.uk` | `Sd683@student.le.ac.uk` | `JB1080@student.le.ac.uk` | `Pj161@student.le.ac.uk` |
| **Assigned User Stories** | **US01, US02, US03** (Sprint 1)<br>**US13, US14, US15** (Sprint 2)<br>**US25, US26, US27** (Sprint 3) | **US04, US05, US06** (Sprint 1)<br>**US16, US17, US18** (Sprint 2)<br>**US28, US29, US30** (Sprint 3) | **US07, US08, US09** (Sprint 1)<br>**US19, US20, US21** (Sprint 2)<br>**US31, US32, US33** (Sprint 3) | **US10, US11, US12** (Sprint 1)<br>**US22, US23, US24** (Sprint 2)<br>**US34, US35, US36** (Sprint 3) |
| **Story Points Delivered** | **33 Story Points** | **30 Story Points** | **30 Story Points** | **33 Story Points** |
| **Assigned Core Modules** | `models/article.py`<br>`models/news_source.py`<br>`services/rss_service.py`<br>`storage/json_storage.py`<br>`dataset/demo_news.json` | `services/search_service.py`<br>`services/categorisation_service.py`<br>`services/sentiment_service.py`<br>`config/category_keywords.json`<br>`config/positive_words.json`<br>`config/negative_words.json` | `services/duplicate_service.py`<br>`services/trend_service.py`<br>`services/source_analytics_service.py`<br>`services/time_analytics_service.py`<br>`config/stop_words.json` | `models/alert_rule.py`<br>`models/alert.py`<br>`services/alert_service.py`<br>`services/report_service.py`<br>`services/dashboard_service.py`<br>`interface/menu.py`<br>`interface/formatting.py`<br>`interface/input_handler.py` |
| **Test Suites Authored** | `tests/ns713/blackbox/`<br>`tests/ns713/whitebox/`<br>`tests/ns713/symbolic/`<br>`tests/ns713/concolic/` | `tests/sd683/blackbox/`<br>`tests/sd683/whitebox/`<br>`tests/sd683/symbolic/`<br>`tests/sd683/concolic/` | `tests/jb1080/blackbox/`<br>`tests/jb1080/whitebox/`<br>`tests/jb1080/symbolic/`<br>`tests/jb1080/concolic/` | `tests/pj161/blackbox/`<br>`tests/pj161/whitebox/`<br>`tests/pj161/symbolic/`<br>`tests/pj161/concolic/`<br>`tests/shared/` |
| **Testing Techniques Applied**| Boundary Value Analysis, Equivalence Partitioning, Fault Injection, Atomic File Testing | Decision Tables, Combinatorial Conjunction, Lexical Polarity Testing | Jaccard Similarity Bounds, Token Frequency Analysis, Date Bucketing | State Transition Testing, RFC 4180 CSV Escaping, ANSI Layout |
| **Symbolic Execution Case** | `NewsArticle.validate()` (6 constraint paths solved) | `SentimentService.classify_score()` (Algebraic $S = P - N$ solved) | `DuplicateService.calculate_similarity()` (Jaccard boundary solved) | `AlertRule.matches()` (5 first-order logic paths solved) |
| **Concolic Testing Case** | `RssService.parse_rss_xml()` (XML node inversion) | `CategorisationService.categorise_text()` (Category negation) | `TrendService.extract_keywords()` (Token length/digit inversion) | `ReportService.export_articles_csv()` (Delimiter escaping inversion) |
| **Tests Authored & Executed** | **45 Unit Tests** (100% Pass) | **36 Unit Tests** (100% Pass) | **31 Unit Tests** (100% Pass) | **65 Unit Tests** + 6 Shared System/Integration Tests + 3 Research SMT Tests (**74 Total**, 100% Pass) |
| **Coverage Contribution** | `article.py`: **95.2%**<br>`storage`: **80.7%**<br>`rss_service`: **80.8%** | `search_service`: **93.7%**<br>`categorisation`: **92.3%**<br>`sentiment`: **85.9%** | `duplicate_service`: **95.7%**<br>`trend_service`: **90.9%**<br>`source_analytics`: **85.2%** | `dashboard`: **94.7%**<br>`alert_service`: **91.7%**<br>`report_service`: **90.7%**<br>`formatting`: **100%** |
| **Process & Audit Roles** | Requirements Management (REQM), Supplier Agreement Management (SAM) | Process & Product Quality Assurance (PPQA), Ground-Truth Evals | Measurement & Analysis (MA), Sizing & Historical Data | Project Planning (PP), Project Monitoring & Control (PMC), Configuration Management (CM) |
| **GitHub Artifacts** | `feature/US01`, `feature/US02`, `feature/US13`, `feature/US25` | `feature/US04`, `feature/US06`, `feature/US16`, `feature/US28` | `feature/US07`, `feature/US08`, `feature/US19`, `feature/US31` | `feature/US10`, `feature/US11`, `feature/US22`, `feature/US36` |

---

## 3. Collaborative Review and Cross-Verification

To enforce quality across boundaries:
1. **Peer Review Protocol**: Every pull request merged into `develop` required an independent code review and sign-off by a different team member.
2. **Cross-Testing**:
   - `Sd683` verified `ns713`'s article model by executing the search and categorisation engines on parsed feeds.
   - `Jb1080` tested `Sd683`'s sentiment scoring during source sentiment aggregation.
   - `Pj161` integrated all analytical services into the master CLI dashboard and CSV export pipelines.
   - `ns713` generated the 105+ synthetic offline articles used across all analytical stress tests.
