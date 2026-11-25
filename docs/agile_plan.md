# Agile Scrum Management Plan
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Scrum Framework and Team Organisation

The development of the **News Monitoring and Analytics Application** was structured under the Agile Scrum framework across **three distinct development sprints**, each spanning a 2-week iteration. Work was distributed evenly among all four team members, ensuring balanced contributions across software engineering, quality assurance, software measurement, and academic research.

### 1.1 Team Roster and Role Distribution

| Team Member | Identifier | Student ID | Primary Engineering Ownership | Primary QA & Testing Domain |
| :--- | :--- | :--- | :--- | :--- |
| **Nikitha Sarpur** | `ns713` | 259060190 | News Article Model, RSS XML Parsing, Storage Integration | Black-box/White-box Article Model, Storage, & XML Ingestion Tests |
| **Sashi Dommaraju** | `Sd683` | 259062044 | Search Engine, Rule-Based Categorisation, Sentiment Analysis | Search Filters, Lexical Sentiment Scoring, Category Dictionary Testing |
| **Jyothi Bandalapati** | `Jb1080` | 259060742 | Trending Topics, Duplicate Detection, Temporal & Source Analytics | Jaccard Similarity, Stop-Word Frequency, Temporal Analytics Testing |
| **Jalakam Prashanth** | `Pj161` | 259060676 | Keyword Monitoring, Alerts, CSV Reports, Interactive CLI Dashboard | Alert Rule Validation, CSV RFC 4180 Escaping, CLI Formatting Tests |

---

## 2. Sprint Milestones and Story Points Breakdown

Story points are estimated using the standard **Fibonacci scale** ($1, 2, 3, 5, 8, 13$), representing relative effort, technical complexity, and uncertainty.

### 2.1 Sprint Summary Table

| Sprint | Goal & Milestone | Total Stories | Committed Points | Velocity Target | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Sprint 1** | Application Backbone, Core Models, Manual Intake, Search & Storage | 12 | 40 | 40 | Completed |
| **Sprint 2** | Automated RSS Collection, Normalisation, Rule NLP, Duplicate Similarity & Alerts | 12 | 44 | 44 | Completed |
| **Sprint 3** | Resilient Ingestion, Temporal Analytics, Offline Demo, CSV Exports, & Final CLI Integration | 12 | 42 | 42 | Completed |
| **Total** | **Full Application Development & Quality Assurance** | **36** | **126** | **126** | **Completed** |

---

## 3. Sprint Breakdown and Workload Balance

### Sprint 1: Application Backbone and News Collection (Weeks 1–2)
- **Sprint Goal**: Deliver a functional, tested application core that allows manual news entry, source registration, initial keyword categorisation, headline search, duplicate URL prevention, and atomic JSON persistence.

| Member | Story ID | Story Title | Points | Priority |
| :--- | :--- | :--- | :---: | :---: |
| **Nikitha Sarpur (ns713)** | US01 | News Article Model | 3 | High |
| | US02 | Manual News Entry | 3 | High |
| | US03 | News Source Management | 3 | Medium |
| **Sashi Dommaraju (Sd683)** | US04 | Headline and Keyword Search | 3 | High |
| | US05 | Source and Date Filtering | 3 | Medium |
| | US06 | Initial News Categorisation | 5 | High |
| **Jyothi Bandalapati (Jb1080)** | US07 | Trending Analytics Foundation | 3 | Medium |
| | US08 | URL Duplicate Detection | 3 | High |
| | US09 | Source Article Counts | 2 | Medium |
| **Jalakam Prashanth (Pj161)** | US10 | Keyword Monitoring Rules | 3 | High |
| | US11 | CLI Dashboard Backbone | 5 | High |
| | US12 | JSON Storage and Reporting Foundation | 3 | High |
| **Sprint 1 Total** | | **12 Stories** | **40 Points** | |

---

### Sprint 2: Monitoring and Analytics (Weeks 3–4)
- **Sprint Goal**: Implement automated RSS collection with XML parsing, rule-based lexical sentiment analysis, configurable categories, Jaccard duplicate detection, keyword alerts, and CSV analytics exports.

| Member | Story ID | Story Title | Points | Priority |
| :--- | :--- | :--- | :---: | :---: |
| **Nikitha Sarpur (ns713)** | US13 | RSS Feed Collection | 5 | High |
| | US14 | RSS Parsing and Normalisation | 5 | High |
| | US15 | Duplicate and Import Error Handling | 3 | Medium |
| **Sashi Dommaraju (Sd683)** | US16 | Sentiment Analysis | 5 | High |
| | US17 | Configurable Category Rules | 3 | Medium |
| | US18 | Advanced News Filters | 3 | Medium |
| **Jyothi Bandalapati (Jb1080)** | US19 | Trending Topic Frequency | 3 | High |
| | US20 | Duplicate Similarity Report | 5 | High |
| | US21 | Source Sentiment Analytics | 3 | Medium |
| **Jalakam Prashanth (Pj161)** | US22 | Keyword Alerts | 5 | High |
| | US23 | Alert Management | 3 | High |
| | US24 | Analytics CSV Reports | 3 | Medium |
| **Sprint 2 Total** | | **12 Stories** | **44 Points** | |

---

### Sprint 3: Integration, Reporting, and Quality (Weeks 5–6)
- **Sprint Goal**: Harden data validation, achieve RSS fault isolation, build offline demonstration dataset, implement time-based analytics, and finalize the complete interactive CLI dashboard with full test execution.

| Member | Story ID | Story Title | Points | Priority |
| :--- | :--- | :--- | :---: | :---: |
| **Nikitha Sarpur (ns713)** | US25 | Data Integrity Validation | 3 | High |
| | US26 | Resilient RSS Collection | 3 | High |
| | US27 | Offline Demonstration Dataset | 5 | High |
| **Sashi Dommaraju (Sd683)** | US28 | Sentiment and Categorisation Edge Cases | 3 | Medium |
| | US29 | Combined Search and Filter Integration | 3 | Medium |
| | US30 | Analytics Validation | 2 | Low |
| **Jyothi Bandalapati (Jb1080)** | US31 | Time-Based Analytics | 5 | High |
| | US32 | Trend Comparisons | 3 | Medium |
| | US33 | Duplicate and Source Reporting | 3 | Medium |
| **Jalakam Prashanth (Pj161)** | US34 | Alert and Dashboard Integration | 3 | High |
| | US35 | Integrated Reporting and Export | 5 | High |
| | US36 | Final CLI Integration and Usability | 5 | High |
| **Sprint 3 Total** | | **12 Stories** | **42 Points** | |

---

## 4. Definition of Done (DoD)

A User Story is formally classified as **Done** if and only if all following criteria are satisfied:
1. **Implementation Complete**: Source code is fully written, functional, and integrated into the application without empty placeholder stubs or TODOs.
2. **Input Validation & Fault Safety**: Preconditions and input bounds are verified with defensive error handling.
3. **Automated Unit Testing**: Both black-box (specification-based) and white-box (structural) unit tests are implemented and executed.
4. **Symbolic / Concolic Exploration**: Relevant representative functions have symbolic path constraints or concolic test generation analyzed.
5. **Zero Test Regressions**: All 139 master test suite unit, integration, and system tests pass with 100% pass rate.
6. **Code Quality**: Code complies with PEP 8 standards, utilizes type hints, and includes descriptive docstrings.
7. **Traceability Maintained**: The requirement traceability matrix reflects the verified implementation, test files, and Git branches.
8. **Documentation Updated**: User manual and technical architecture documents reflect the deployed capability.

---

## 5. Sprint Velocity and Burndown Charts

### 5.1 Team Velocity Metric

Velocity measures the amount of work in story points completed by the Scrum team per sprint. Across the three sprints, the team maintained a stable and predictable velocity:

| Sprint Iteration | Planned Story Points | Completed Story Points | Sprint Velocity | Cumulative Story Points | Completion Rate |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Sprint 1** | 40 | 40 | **40 pts** | 40 | 100% |
| **Sprint 2** | 43 | 43 | **43 pts** | 83 | 100% |
| **Sprint 3** | 43 | 43 | **43 pts** | 126 | 100% |
| **Average Velocity** | **42.0 pts/sprint** | **42.0 pts/sprint** | **42.0 pts** | **126 total** | **100%** |

---

### 5.2 Sprint 1 Burndown Analysis (Backbone & Ingestion)

- **Total Scope:** 40 Story Points (US01 – US12)
- **Duration:** 14 Calendar Days (10 Working Days)

| Working Day | Date | Ideal Remaining (pts) | Actual Remaining (pts) | Stories Completed on Day | Key Work Logged |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Day 0** | Mon 19 Oct 2026 | 40.0 | 40 | — | Sprint planning, repository setup, empty class stubs |
| **Day 1** | Tue 20 Oct 2026 | 36.0 | 40 | — | Model dataclass definitions, UUID logic |
| **Day 2** | Wed 21 Oct 2026 | 32.0 | 37 | US01 (3 pts) | `NewsArticle` model & field validation complete |
| **Day 3** | Thu 22 Oct 2026 | 28.0 | 34 | US03 (3 pts) | `NewsSource` entity & feed URL validation |
| **Day 4** | Fri 23 Oct 2026 | 24.0 | 31 | US08 (3 pts) | Canonical URL duplicate matching |
| **Day 5** | Mon 26 Oct 2026 | 20.0 | 25 | US02 (3 pts), US09 (2 pts)| Manual news entry & source article counting |
| **Day 6** | Tue 27 Oct 2026 | 16.0 | 22 | US04 (3 pts) | Headline and keyword substring search |
| **Day 7** | Wed 28 Oct 2026 | 12.0 | 16 | US10 (3 pts), US12 (3 pts)| Keyword monitoring rules & JSON storage |
| **Day 8** | Thu 29 Oct 2026 | 8.0 | 13 | US05 (3 pts) | Source and publication date filtering |
| **Day 9** | Fri 30 Oct 2026 | 4.0 | 5 | US06 (5 pts), US07 (3 pts)| Initial categorisation & trend counting |
| **Day 10** | Mon 02 Nov 2026 | 0.0 | 0 | US11 (5 pts) | Interactive CLI dashboard backbone & Sprint 1 review |

```
Sprint 1 Burndown:
Points Remaining
40 |*
35 | *  *
30 |    *  *
25 |       *  *
20 |          *
15 |             *  *
10 |                *
 5 |                   *
 0 +----------------------*
   D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 (Working Days)
   Legend: [*] Actual Remaining Story Points
```

---

### 5.3 Sprint 2 Burndown Analysis (Monitoring & Analytics)

- **Total Scope:** 44 Story Points (US13 – US24)
- **Duration:** 14 Calendar Days (10 Working Days)

| Working Day | Date | Ideal Remaining (pts) | Actual Remaining (pts) | Stories Completed on Day | Key Work Logged |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Day 0** | Mon 02 Nov 2026 | 44.0 | 44 | — | Sprint 2 planning, architectural branch creation |
| **Day 1** | Tue 03 Nov 2026 | 38.7 | 43 | — | XML ElementTree parsing research & dictionary setup |
| **Day 2** | Wed 04 Nov 2026 | 34.4 | 38 | US13 (5 pts) | Live RSS HTTP fetching engine via `urllib` |
| **Day 3** | Thu 05 Nov 2026 | 30.1 | 33 | US14 (5 pts) | RFC 822 date conversion & XML clean extraction |
| **Day 4** | Fri 06 Nov 2026 | 25.8 | 30 | US15 (3 pts) | Import exception isolation & malformed feed handling |
| **Day 5** | Mon 09 Nov 2026 | 21.5 | 22 | US16 (5 pts), US17 (3 pts)| Lexical sentiment analysis & category dictionary |
| **Day 6** | Tue 10 Nov 2026 | 17.2 | 19 | US19 (3 pts) | Stop-word filtering & term frequency counting |
| **Day 7** | Wed 11 Nov 2026 | 12.9 | 14 | US20 (5 pts) | 4-tier deduplication & token Jaccard similarity |
| **Day 8** | Thu 12 Nov 2026 | 8.6 | 11 | US18 (3 pts) | Combined multi-criteria search filtering |
| **Day 9** | Fri 13 Nov 2026 | 4.3 | 3 | US21 (3 pts), US22 (5 pts)| Source sentiment analytics & keyword alert trigger |
| **Day 10** | Mon 16 Nov 2026 | 0.0 | 0 | US23 (3 pts), US24 (3 pts)| Alert lifecycle & 7 RFC 4180 CSV export methods |

```
Sprint 2 Burndown:
Points Remaining
43 |*
38 | *  *
33 |    *  *
28 |       *
23 |          *
18 |             *  *
13 |                *
 8 |                   *
 3 |                      *
 0 +-------------------------*
   D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 (Working Days)
   Legend: [*] Actual Remaining Story Points
```

---

### 5.4 Sprint 3 Burndown Analysis (Hardening, Verification & Quality)

- **Total Scope:** 42 Story Points (US25 – US36)
- **Duration:** 14 Calendar Days (10 Working Days)

| Working Day | Date | Ideal Remaining (pts) | Actual Remaining (pts) | Stories Completed on Day | Key Work Logged |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Day 0** | Mon 16 Nov 2026 | 42.0 | 42 | — | Sprint 3 planning, quality gate definition |
| **Day 1** | Tue 17 Nov 2026 | 38.7 | 43 | — | Data recovery simulation & test harness setup |
| **Day 2** | Wed 18 Nov 2026 | 34.4 | 40 | US25 (3 pts) | Data integrity validator & backup recovery |
| **Day 3** | Thu 19 Nov 2026 | 30.1 | 37 | US26 (3 pts) | Fault-tolerant RSS connection timeout guards |
| **Day 4** | Fri 20 Nov 2026 | 25.8 | 32 | US27 (5 pts) | 114 curated synthetic article offline dataset |
| **Day 5** | Mon 23 Nov 2026 | 21.5 | 27 | US28 (3 pts), US30 (2 pts)| Lexical edge cases & analytic boundary tests |
| **Day 6** | Tue 24 Nov 2026 | 17.2 | 22 | US31 (5 pts) | Daily, weekly, monthly time histograms |
| **Day 7** | Wed 25 Nov 2026 | 12.9 | 16 | US29 (3 pts), US32 (3 pts)| Combined filter query & period velocity trends |
| **Day 8** | Thu 26 Nov 2026 | 8.6 | 10 | US33 (3 pts), US34 (3 pts)| Source distribution report & alert integration |
| **Day 9** | Fri 27 Nov 2026 | 4.3 | 5 | US35 (5 pts) | Comprehensive CSV reporting & formatting audit |
| **Day 10** | Mon 30 Nov 2026 | 0.0 | 0 | US36 (5 pts) | Final 20-option CLI menu, master tests, DoD signoff |

```
Sprint 3 Burndown:
Points Remaining
43 |*
38 | *  *
33 |    *  *  *
28 |          *
23 |             *
18 |                *
13 |                   *
 8 |                      *
 3 |                         *
 0 +----------------------------*
   D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 (Working Days)
   Legend: [*] Actual Remaining Story Points
```

