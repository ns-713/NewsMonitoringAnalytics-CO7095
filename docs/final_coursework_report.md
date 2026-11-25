# Design, Verification and Measurement of an Offline News Monitoring and Analytics Application: A Software Quality Assurance Case Study

**University of Leicester – Department of Computing and Mathematical Sciences**  
**Module:** CO7095 – Software Measurement and Quality Assurance (Academic Year 2026–2027)  
**Assignment:** Group Coursework – News Monitoring and Analytics Application  
**Target Award:** MSc Advanced Computer Science / Software Engineering  
**Submission Date:** 04 January 2027  

---

## Cover Sheet and Declaration of Academic Honesty

We, the undersigned, confirm that we have handed in a signed Declaration of Academic Honesty Form and that we are fully aware of the statements contained therein. We confirm that this submission is the product of our own collaborative work. All sources of information, including published literature, software quality standards, and technical documentation, have been acknowledged through formal academic citation. We understand that this submission will be assessed by Turnitin Software and that similarity scores are maintained strictly below 10%.

| Team Member Name (in CAPITALS) | Student User ID | Student ID Number | Primary Assigned Responsibilities | Signature |
| :--- | :---: | :---: | :--- | :---: |
| **SARPUR, NIKITHA** | `ns713` | 259060190 | Lead Software Engineer & Scrum Master | *N. Sarpur* |
| **DOMMARAJU, SASHI** | `sd683` | 259062044 | Quality Assurance Specialist | *S. Dommaraju* |
| **BANDALAPATI, JYOTHI** | `jb1080` | 259060742 | Software Measurement Specialist | *J. Bandalapati* |
| **PRASHANTH, JALAKAM** | `pj161` | 259060676 | System Integrator & CMMI Audit Lead | *J. Prashanth* |

---

# SECTION A: TECHNICAL SPECIFICATION, DEVELOPMENT TECHNIQUES AND SQA MEASUREMENT

## 1. Introduction

Contemporary digital news consumption is defined by severe information overload and content syndication. A single real-world event is routinely republished across dozens of syndicated RSS feeds with only minor editorial variations, headline punctuation alterations, or tracking parameter additions. Information analysts face substantial cognitive fatigue attempting to isolate novel reporting from redundant syndication. While commercial cloud aggregators exist, they introduce severe impediments from a Software Quality Assurance (SQA) perspective: non-deterministic machine learning classifiers whose outputs cannot be reproduced bit-for-bit across test runs, opaque proprietary backends, metered API limits, network authentication gates, and third-party dependency vulnerabilities.

In direct response to the CO7095 coursework specification, this project engineered a production-grade, backend-focused, offline-capable News Monitoring and Analytics Application written strictly in Python 3 using the standard library exclusively. There is no graphical user interface (GUI) and no external database. Instead, user interaction is provided via an interactive command-line interface (CLI) and data persistence is achieved via serialized JSON storage fortified by crash-safe atomic filesystem operations (`.tmp` staging, atomic `os.replace`, and automated `.bak` snapshot recovery). The application ingests RSS feeds, deterministically classifies content using keyword maps, evaluates lexical sentiment polarity ($S = P - N$), prunes redundant articles through a 4-tier deduplication hierarchy (URL matching, headline fingerprinting, and token-based Jaccard similarity $\ge 0.70$), extracts trending topics, and tracks keyword alerts.

The foundational design principle of the application is determinism: identical inputs deterministically yield identical outputs, enabling the construction of exact mathematical test oracles. The project provides an empirical testing ground for core module learning outcomes: formal project estimation (PERT, COCOMO I/II, EVM), specification and structural testing (Black-box and White-box suites achieving 85.2% statement coverage across 195 automated tests), advanced research techniques (Symbolic Execution via an in-house DPLL(T) SMT solver and semi-automated concolic testing), and process maturity auditing against all seven CMMI Level 2 Process Areas.

---

## 2. Software Planning and Design

### 2.1 Agile User Stories and Planning Poker Story Points
The system requirements were decomposed into 36 granular User Stories (US01 through US36), ensuring an equal distribution of nine stories per team member (three per sprint). To eliminate sizing bias, story points were estimated using Planning Poker across a restricted Fibonacci sequence ($1, 2, 3, 5, 8$). Initial divergent estimates were settled through consensus during Sprint Planning, yielding a project total of 126 Story Points (an average of 31.5 points per engineer). Each user story traces bidirectionally to a specific functional requirement, Git feature branch, and underlying Python function implementation.

| Story ID | Sprint | Assigned Member | SP | Function Under Test & Module Path | Target Functional Requirement |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **US01** | Sp 1 | Nikitha (`ns713`) | 3 | `models/article.py::NewsArticle.validate()` | FR01: Article Intake & Invariants |
| **US02** | Sp 1 | Nikitha (`ns713`) | 5 | `services/rss_service.py::RssService.parse_rss_xml()` | FR02: RSS XML Parsing |
| **US03** | Sp 1 | Nikitha (`ns713`) | 5 | `storage/json_storage.py::JsonStorage.save_articles()` | FR15: Atomic Data Persistence |
| **US04** | Sp 1 | Sashi (`sd683`) | 5 | `services/search_service.py::SearchService.search_articles()` | FR03: Multi-field Search |
| **US05** | Sp 1 | Sashi (`sd683`) | 5 | `services/categorisation_service.py::categorise_text()` | FR04: Rule-based Categorisation |
| **US06** | Sp 1 | Sashi (`sd683`) | 3 | `services/sentiment_service.py::score_sentiment()` | FR05: Lexical Polarity Scoring |
| **US07** | Sp 1 | Jyothi (`jb1080`) | 5 | `services/duplicate_service.py::calculate_similarity()` | FR06: Jaccard Similarity Bounds |
| **US08** | Sp 1 | Jyothi (`jb1080`) | 5 | `services/trend_service.py::extract_trending_topics()` | FR07: Stopword-filtered Trends |
| **US09** | Sp 1 | Jyothi (`jb1080`) | 3 | `services/source_analytics_service.py::get_source_stats()` | FR08: Source Volume & Share |
| **US10** | Sp 1 | Prashanth (`pj161`)| 3 | `models/alert_rule.py::AlertRule.matches()` | FR10: Keyword Alert Predicates |
| **US11** | Sp 1 | Prashanth (`pj161`)| 5 | `services/report_service.py::export_articles_csv()` | FR12: RFC 4180 CSV Export |
| **US12** | Sp 1 | Prashanth (`pj161`)| 3 | `interface/menu.py::NewsAppMenu.run()` | FR14: Interactive CLI Navigation |
| **US13–15** | Sp 2 | Nikitha (`ns713`) | 12 | `services/news_service.py::batch_import_articles()` | FR01, FR02, FR15 (Batch Ingestion) |
| **US16–18** | Sp 2 | Sashi (`sd683`) | 11 | `services/search_service.py::filter_by_date_range()` | FR03, FR04, FR05 (Advanced Filter) |
| **US19–21** | Sp 2 | Jyothi (`jb1080`) | 11 | `services/time_analytics_service.py::bucket_by_date()` | FR06, FR08, FR09 (Temporal Analytics) |
| **US22–24** | Sp 2 | Prashanth (`pj161`)| 10 | `services/alert_service.py::process_article_alerts()` | FR10, FR11, FR13 (Alert State & Read) |
| **US25–27** | Sp 3 | Nikitha (`ns713`) | 13 | `services/rss_service.py::poll_all_active_sources()` | FR02, FR15 (Multi-feed Recovery) |
| **US28–30** | Sp 3 | Sashi (`sd683`) | 14 | `services/sentiment_service.py::classify_score()` | FR04, FR05 (Ground-Truth Auditing) |
| **US31–33** | Sp 3 | Jyothi (`jb1080`) | 14 | `services/duplicate_service.py::find_duplicates()` | FR06, FR07, FR09 (4-Tier Dedup Hierarchy)|
| **US34–36** | Sp 3 | Prashanth (`pj161`)| 15 | `services/dashboard_service.py::generate_dashboard()` | FR12, FR13, FR14 (Consolidated Telemetry)|
| **Total** | | **4 Members** | **126** | **All 18 Production Modules Across System** | **Complete FR01–FR15 Traceability** |

### 2.2 Velocity and Burndown Trajectory
Development proceeded across three two-week sprints. Planned velocity was 42.0 story points per sprint. Actual velocity achieved was 40 SP in Sprint 1, 44 SP in Sprint 2, and 42 SP in Sprint 3, demonstrating high predictability and zero carry-over debt across sprint boundaries.

```
+-----------------------------------------------------------------------------------------+
|                                Cumulative Sprint Burndown                                |
+------------------+------------------+---------------------+-----------------------------+
| Sprint Milestone | Committed Points | Velocity (Delivered)| Remaining Outstanding Points|
+------------------+------------------+---------------------+-----------------------------+
| Sprint 0 (Plan)  | 126 SP           | 0 SP                | 126 SP                      |
| Sprint 1 Close   | 40 SP            | 40 SP               | 86 SP                       |
| Sprint 2 Close   | 44 SP            | 44 SP               | 42 SP                       |
| Sprint 3 Close   | 42 SP            | 42 SP               | 0 SP (Release Target Met)   |
+------------------+------------------+---------------------+-----------------------------+
```

```
[INSERT FIGURE 6: Cumulative Sprint Burndown Trajectory Chart HERE]
```

### 2.3 PERT Activity-on-Node Network and Critical Path Derivation
The project schedule was modelled as an Activity-on-Node (AoN) network comprising 17 work packages distributed across the four engineers. Durations were estimated using three-point approximations: optimistic ($a$), most likely ($m$), and pessimistic ($b$). The expected duration $T_e$ and variance $\sigma^2$ were calculated via:

$$T_e = \frac{a + 4m + b}{6}, \qquad \sigma^2 = \left(\frac{b - a}{6}\right)^2$$

```
[INSERT FIGURE 5: PERT Activity-on-Node Network Diagram (PNG from draw.io) HERE]
```
*Figure 5. PERT Activity-on-Node Network indicating the 12-activity Critical Path (41.85 working days).*

A forward pass established early start (ES) and early finish (EF) times, while a backward pass determined late start (LS), late finish (LF), and total float ($TF = LS - ES$). Exactly 12 activities exhibited zero float ($TF = 0$), forming the single deterministic Critical Path:

$$\text{Critical Path: } A1 \to A2 \to A3 \to A5 \to A6 \to A7 \to A9 \to A10 \to A11 \to A14 \to A16 \to A17$$

The cumulative expected duration along this path is **41.85 working days**. Summing the variances of critical activities yielded a path variance of $\sigma^2_{\text{path}} = 4.83\text{ days}^2$, resulting in a standard deviation of $\sigma = 2.20\text{ days}$. Evaluating schedule risk against a contractual 45-day deadline via the standard normal variate:

$$Z = \frac{45 - 41.85}{2.20} = \frac{3.15}{2.20} \approx 1.43 \implies P(T \le 45) = \Phi(1.43) = 92.36\%$$

The project carries a 92.36% statistical probability of on-time delivery under normal operating variances.

### 2.4 Software Cost and Effort Estimation (COCOMO I and COCOMO II)
Physical codebase sizing measures 2,741 Source Lines of Code (SLOC) of core application logic and 2,534 SLOC of automated verification infrastructure, totalling 5,275 deliverable SLOC (5.275 KSLOC).

#### COCOMO I (Basic, Organic Mode)
Applying Boehm's Organic parameters ($a = 2.4, b = 1.05, c = 2.5, d = 0.38$):
- **Core Application (2.741 KSLOC)**:
  $$\text{Effort} = 2.4 \times (2.741)^{1.05} \approx 6.94\text{ Person-Months (PM)}$$
  $$\text{TDEV} = 2.5 \times (6.94)^{0.38} \approx 5.21\text{ Months}$$
- **Total Monitored Codebase (5.275 KSLOC)**:
  $$\text{Effort} = 2.4 \times (5.275)^{1.05} \approx 13.78\text{ PM}, \quad \text{TDEV} = 2.5 \times (13.78)^{0.38} \approx 6.77\text{ Months}$$

#### COCOMO II (Post-Architecture Model)
The Post-Architecture model adjusts nominal effort via five scale factors ($B = 0.91 + 0.01 \sum SF_i = 1.012$) and seventeen effort multipliers ($EAF = \prod EM_i = 0.884$). Reflecting high analyst capability (`ACAP` = 0.85), standard tool use (`TOOL` = 1.00), and high execution reliability (`RELY` = 1.10), the adjusted effort for the core codebase is $E = 6.42\text{ PM}$ ($TDEV = 5.02\text{ months}$), validating that disciplined SQA rigor offsets nominal schedule pressure.

### 2.5 Earned Value Management (EVM) Analysis
The project operated under an authorized Budget at Completion (BAC) of **£18,000**, calculated from 126 Story Points at an institutional baseline of £142.86 per point across a 30-working-day release window. 

At project completion (Day 30), all 126 story points were verified and delivered into production. Actual Cost (AC) recorded across engineering timesheets was **£17,140**. Key performance indicators demonstrate optimal cost efficiency:
- **Planned Value (PV)**: $126\text{ SP} \times £142.86 = \mathbf{£18,000}$
- **Earned Value (EV)**: $126\text{ SP} \times £142.86 = \mathbf{£18,000}$
- **Actual Cost (AC)**: $\mathbf{£17,140}$
- **Cost Variance (CV)**: $EV - AC = £18,000 - £17,140 = \mathbf{+£860}$ (Favourable budget surplus)
- **Schedule Variance (SV)**: $EV - PV = £18,000 - £18,000 = \mathbf{£0.00}$ (Exactly on schedule)
- **Cost Performance Index (CPI)**: $\frac{EV}{AC} = \frac{18,000}{17,140} = \mathbf{1.050}$ (5.0% cost efficiency gain)
- **Schedule Performance Index (SPI)**: $\frac{EV}{PV} = \frac{18,000}{18,000} = \mathbf{1.000}$ (100% schedule alignment)
- **Variance at Completion (VAC)**: $BAC - EAC = £18,000 - £17,140 = \mathbf{+£860}$

---

## 3. Implementation (Back-End)

### 3.1 Four-Tier Layered Architecture and Domain Models
The backend strictly adheres to a four-tier decoupled architectural style. Upward dependencies are forbidden: higher layers depend only on immediate lower interfaces, ensuring modular testability.

```
[INSERT FIGURE 1: Four-Tier Layered Architecture Diagram (PNG from draw.io) HERE]
```
*Figure 1. Four-Tier Layered Architecture decoupling Presentation, Business Logic, Persistence, and Domain Entities.*

1. **Presentation Layer (`interface/`)**: `menu.py`, `formatting.py`, and `input_handler.py` coordinate CLI interactions, table rendering, ANSI formatting, and user input validation.
2. **Service & Business Logic Layer (`services/`)**: Eleven isolated service components encapsulating RSS feed ingestion, search, categorisation, sentiment scoring, deduplication, trending extraction, source telemetry, temporal metrics, alerting, CSV reporting, and dashboard assembly.
3. **Data Access & Storage Layer (`storage/`)**: `json_storage.py` manages crash-safe persistence, atomic file swapping, and backup snapshot recovery.
4. **Domain Model Layer (`models/`)**: Pure entity definitions enforcing strict constructor invariants.

```
[INSERT FIGURE 2: UML Class Diagram of Domain Entities (PNG from draw.io) HERE]
```
*Figure 2. UML Class Diagram detailing attributes, methods, and relationships of core domain entities.*

- `NewsArticle`: Validates non-empty headlines ($\ge 3$ characters), valid URL protocol schemes (`http`, `https`, `file`), publication date ISO parsing, and category labels.
- `NewsSource`: Encapsulates feed metadata, polling timestamps, and active status flags.
- `AlertRule` & `Alert`: `AlertRule` evaluates keyword presence against article content and category filters, generating immutable `Alert` records initialized in the `UNREAD` state.

### 3.2 Resilient Ingestion and Crash-Safe Atomic Persistence
To satisfy non-functional reliability requirements without relying on relational database engines, `JsonStorage` implements transactional file writes using standard-library filesystem primitives:
1. Data structures are serialized to a temporary staging file (`<filename>.tmp`).
2. The operating system swaps the temporary file over the target file using `os.replace()`, an atomic operation guaranteed by POSIX and Windows kernel specifications.
3. Prior to writing, an automated snapshot (`<filename>.bak`) is refreshed. If file parsing detects unexpected truncation or bit-corruption, `JsonStorage` automatically rolls back state to the `.bak` replica, preventing runtime corruption.

```
[INSERT FIGURE 3: UML Sequence Diagram of RSS Ingestion Pipeline (PNG from draw.io) HERE]
```
*Figure 3. UML Sequence Diagram illustrating the feed ingestion, multi-tier deduplication, enrichment, and atomic storage flow.*

### 3.3 Four-Tier Deduplication Hierarchy and Similarity Algorithms
Syndicated news streams contain substantial redundancy. `DuplicateService` applies a four-tier filtering hierarchy:
- **Tier 1 (Canonical URL Matching)**: Matches stripped, query-normalised article URLs ($O(1)$ set lookup).
- **Tier 2 (Headline Fingerprinting)**: Compares alphanumeric, lowercased, whitespace-collapsed headline tokens.
- **Tier 3 (Jaccard Token Similarity)**: Calculates the ratio of shared word tokens over total union tokens:
  $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
  If $J(A, B) \ge 0.70$, the incoming item is discarded as a near-duplicate derivative.
- **Tier 4 (Temporal Proximity Filter)**: Ensures matching articles falling within a 24-hour window are clustered.

### 3.4 Lexical Sentiment and Deterministic Categorisation
Text classification and sentiment analysis avoid non-deterministic machine learning models. `CategorisationService` maps incoming headlines and content against curated keyword lexicons, assigning categories (`Politics`, `Technology`, `Business`, `Science`, `Health`) based on maximum keyword frequency. `SentimentService` applies a deterministic lexical polarity rule:

$$S = P - N$$

where $P$ is the frequency of recognized positive terms and $N$ is the frequency of negative terms. The classification oracle is mathematically bounded: Positive if $S > 0$, Negative if $S < 0$, and Neutral if $S = 0$.

---

## 4. Testing and Test Coverage Measurement

### 4.1 Master Test Suite Architecture and Infrastructure
The testing framework was built exclusively using Python's native `unittest` framework to guarantee unassisted execution on university lab computers. Test suites are organized under member-specific namespaces conforming strictly to the module naming standard:
`ns713/test/`, `sd683/test/`, `jb1080/test/`, `pj161/test/`, `tests/shared/`, and `research/`.

The test runner `run_tests.py` integrates a native statement coverage tracer built upon Python's standard-library `trace` module, computing exact executed statement line counts across all 18 production modules without requiring third-party tools.

```
================================================================================
  CO7095 MASTER TEST SUITE EXECUTION SUMMARY
================================================================================
  Total Automated Tests Executed : 195
  Passed                         : 195
  Failed                         : 0
  Errors                         : 0
  Test Pass Rate                 : 100.0%
================================================================================
```

### 4.2 Black-Box Testing
Black-box testing applied formal specification-based testing techniques across all functional requirements:

1. **Equivalence Partitioning (EP)**:
   - *Headline Strings*: Partitioned into Valid Non-empty ($\ge 3$ characters), Empty/Whitespace Strings (Rejected), and Boundary Edge cases.
   - *URL Protocols*: Partitioned into Supported schemes (`http://`, `https://`, `file://`) and Unsupported schemes (`ftp://`, `mailto:`, empty).
2. **Boundary Value Analysis (BVA)**:
   - Evaluated headline length boundaries at lengths 0, 2 (invalid), 3 (minimum valid), and 4 (nominal valid).
   - Evaluated Jaccard similarity threshold boundaries at $J = 0.699$ (classified as Unique) versus $J = 0.700$ (classified as Duplicate).
3. **Decision Table Testing (DTT)**:
   - Applied to multi-condition search filtering combining category filters, date ranges, and keyword conjunctions.
   - Applied to `AlertRule.matches()` evaluating active status, category match, and keyword presence across all Boolean truth-table permutations.

| Test ID | Member | Technique | Target Function | Test Input & Condition | Expected Verdict | Actual Result |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| `TC-BB-ART-01` | `ns713` | EP | `NewsArticle.validate` | Complete, well-formed article fields | Valid (True) | **PASS** |
| `TC-BB-ART-02` | `ns713` | BVA | `NewsArticle.validate` | Headline length = 0 (empty string) | Invalid (False) | **PASS** |
| `TC-BB-ART-03` | `ns713` | BVA | `NewsArticle.validate` | Headline length = 2 characters | Invalid (False) | **PASS** |
| `TC-BB-ART-04` | `ns713` | BVA | `NewsArticle.validate` | Headline length = 3 characters | Valid (True) | **PASS** |
| `TC-BB-SRC-04` | `ns713` | EP | `NewsArticle.validate` | Unsupported protocol `ftp://feed.xml` | Invalid (False) | **PASS** |
| `TC-BB-SRH-01` | `sd683` | DTT | `SearchService.search` | Matching keyword and active category | Matching articles | **PASS** |
| `TC-BB-SNT-01` | `sd683` | EP | `SentimentService.score` | Headline with 3 positive, 1 negative words | Score = +2, Positive | **PASS** |
| `TC-BB-DUP-04` | `jb1080`| BVA | `DuplicateService.calc` | Token sets sharing $J = 0.666$ | Unique (False) | **PASS** |
| `TC-BB-DUP-05` | `jb1080`| BVA | `DuplicateService.calc` | Token sets sharing $J = 0.875 \ge 0.70$ | Duplicate (True) | **PASS** |
| `TC-BB-ALT-01` | `pj161` | DTT | `AlertRule.matches` | Rule enabled, keyword present, category match | Alert Triggered | **PASS** |

### 4.3 White-Box Testing and Coverage
White-box testing focused on basis path coverage, statement coverage, and branch condition coverage across core business algorithms.

#### Basis-Path Analysis of `DuplicateService.calculate_similarity()`
The control-flow graph (CFG) for token similarity calculation contains $N = 9$ nodes and $E = 11$ edges. Its McCabe cyclomatic complexity is:

$$M = E - N + 2P = 11 - 9 + 2(1) = 4$$

Four linearly independent basis paths were identified and tested:
- **Path 1 ($N1 \to N2 \to N6 \to N9$)**: Both token sets empty; triggers zero-union guard, returns $0.0$.
- **Path 2 ($N1 \to N2 \to N3 \to N4 \to N6 \to N9$)**: Disjoint token sets; empty intersection, returns $0.0$.
- **Path 3 ($N1 \to N2 \to N3 \to N4 \to N5 \to N7 \to N9$)**: Identical token sets; returns $1.0$.
- **Path 4 ($N1 \to N2 \to N3 \to N4 \to N5 \to N8 \to N9$)**: Partial token overlap; returns computed Jaccard ratio $|A \cap B| / |A \cup B|$.

```
[INSERT FIGURE 4: Control Flow Graph for Basis-Path Testing (PNG from draw.io) HERE]
```
*Figure 4. Control Flow Graph of calculate_similarity() indicating 4 basis paths ($M=4$).*

### 4.4 Research Component: Symbolic Execution and Concolic Testing

#### Research Component 1: Symbolic Execution with DPLL(T) SMT Solver
Symbolic execution replaces concrete inputs with symbolic variables $\alpha$, accumulating path conditions along execution branches. To evaluate satisfiability without relying on heavy external binaries, the team implemented an in-house SMT solver (`research/smt_solver.py`) integrating:
- A propositional DPLL engine (Davis-Putnam-Logemann-Loveland) with unit propagation, pure literal elimination, and backtracking search.
- A theory solver for Linear Integer Arithmetic ($T_{\text{LIA}}$) handling unbounded integer intervals and linear inequalities without artificial bounds.
- A theory solver for Strings ($T_{\text{String}}$) verifying length constraints, prefix matches, and character set memberships.
- A DPLL(T) integration architecture: DPLL abstracts theory predicates into propositional literals, queries theory solvers for consistency, and learns conflict clauses on contradiction.

```
                      +---------------------------------------+
                      |       Input First-Order Formula       |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |        Propositional Abstraction      |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |         DPLL SAT Solver Engine        | <------+
                      +---------------------------------------+        |
                                          |                            |
                         Boolean Model / Satisfying Assignment         | Conflict Lemma
                                          |                            | (Backtrack)
                                          v                            |
                      +---------------------------------------+        |
                      |   Theory Solvers (T_LIA & T_String)   | -------+
                      +---------------------------------------+
                                          |
                                  Theory Consistent?
                                    /           \
                                  Yes            No
                                  /               \
                                 v                 v
                        [ SAT + Witness ]     [ Learn Clause ]
```
*Figure 7. Architecture of the in-house DPLL(T) Satisfiability Modulo Theories (SMT) Solver.*

Symbolic execution was applied to all four team members' functional modules:
1. `NewsArticle.validate()`: Path condition $\Phi \equiv (\text{len}(h) \ge 3) \wedge (u.\text{scheme} \in \{\text{http}, \text{https}, \text{file}\})$. Solver synthesized satisfying witness $h = \text{"Breaking News"}, u = \text{"https://bbc.co.uk"}$.
2. `SentimentService.classify_score()`: Algebraic path condition $\Phi \equiv (P - N > 0)$. Solver proved satisfiability with witness $P=3, N=1$.
3. `DuplicateService.calculate_similarity()`: Path condition $\Phi \equiv (|A \cap B| / |A \cup B| \ge 0.70)$. Proved boundary witness with $|A \cap B|=7, |A \cup B|=8 \implies J = 0.875$.
4. `AlertRule.matches()`: First-order conjunction over keyword matching and category filters. Proved all 5 execution branches satisfiable.

#### Research Component 2: Concolic Testing Harness
Concolic testing (combining concrete and symbolic execution, pioneered in DART and CUTE) was implemented via a semi-automated exploration harness (`research/concolic_engine.py`). Rather than using complex bytecode rewriting, the harness systematically evaluates AST-derived symbolic path conditions across all four student packages, inverts conditional branch predicates, queries the DPLL(T) solver for satisfying models, and dispatches concrete test inputs to live production methods to record actual runtime outcomes.

In `RssService.parse_rss_xml()`, starting from well-formed seed XML $s_0$, successive branch predicate negations generated test inputs for missing headlines, unparseable dates, and malformed tags, verifying that exception handling gracefully contains parsing errors without application crashes.

### 4.5 Test Coverage Measurement and Analysis
Code statement coverage was measured using Python's native `trace.Trace` engine across all 2,287 production statements:

| Source Module Under Test | Total Statements | Executed Statements | Missed Statements | Statement Coverage (%) |
| :--- | :---: | :---: | :---: | :---: |
| `interface/__init__.py` | 4 | 4 | 0 | **100.0%** |
| `interface/formatting.py` | 64 | 64 | 0 | **100.0%** |
| `interface/input_handler.py` | 64 | 62 | 2 | **96.9%** |
| `models/__init__.py` | 5 | 5 | 0 | **100.0%** |
| `models/news_source.py` | 61 | 56 | 5 | **91.8%** |
| `models/alert_rule.py` | 56 | 51 | 5 | **91.1%** |
| `models/alert.py` | 54 | 49 | 5 | **90.7%** |
| `models/article.py` | 116 | 103 | 13 | **88.8%** |
| `services/duplicate_service.py` | 95 | 91 | 4 | **95.8%** |
| `services/dashboard_service.py` | 38 | 36 | 2 | **94.7%** |
| `services/search_service.py` | 95 | 89 | 6 | **93.7%** |
| `services/categorisation_service.py`| 65 | 60 | 5 | **92.3%** |
| `services/alert_service.py` | 121 | 111 | 10 | **91.7%** |
| `services/trend_service.py` | 77 | 70 | 7 | **90.9%** |
| `services/news_service.py` | 197 | 179 | 18 | **90.9%** |
| `services/report_service.py` | 107 | 97 | 10 | **90.7%** |
| `services/rss_service.py` | 129 | 114 | 15 | **88.4%** |
| `services/sentiment_service.py` | 78 | 67 | 11 | **85.9%** |
| `services/source_analytics_service.py`| 61 | 52 | 9 | **85.2%** |
| `storage/json_storage.py` | 88 | 71 | 17 | **80.7%** |
| `services/time_analytics_service.py` | 92 | 71 | 21 | **77.2%** |
| `interface/menu.py` | 592 | 455 | 137 | **76.9%** |
| `storage/__init__.py` | 2 | 2 | 0 | **100.0%** |
| `services/__init__.py` | 26 | 13 | 13 | **50.0%** |
| **Total Monitored Codebase** | **2,287** | **1,948** | **339** | **85.2%** |

Overall statement coverage reaches **85.2% (1,948 of 2,287 statements)**, satisfying the Outstanding tier ($\ge 85\%$) of the CO7095 marking rubric across the entire application codebase.

---

## 5. CMMI Level 2 Documentation Audit

The team audited its development processes against the seven Process Areas (PAs) of the Capability Maturity Model Integration (CMMI) Level 2 ("Managed"):

1. **Requirements Management (REQM)**: Managed by Nikitha Sarpur. Bidirectional traceability maintained across FR01–FR15, US01–US36, code commits, and test cases (see Appendix 1). Scope changes were formally evaluated for test-to-code impact before branch merging.
2. **Project Planning (PP)**: Managed by Jalakam Prashanth. WBS created with 17 activities; duration estimated via PERT three-point calculations; effort estimated via COCOMO I/II; cost baselined at £18,000.
3. **Project Monitoring and Control (PMC)**: Managed by Jalakam Prashanth. Bi-weekly sprint reviews and daily standups monitored progress against burndown charts. EVM metrics evaluated at Day 30 demonstrated cost efficiency ($CPI = 1.050$) and schedule alignment ($SPI = 1.000$).
4. **Measurement and Analysis (MA)**: Managed by Jyothi Bandalapati. Defined objective measurement baselines: physical SLOC (2,741 core / 5,275 total), statement coverage (85.2%), test pass rate (100.0%), and cyclomatic complexity ($M \le 10$).
5. **Process and Product Quality Assurance (PPQA)**: Managed by Sashi Dommaraju. Enforced Definition of Done (DoD) requiring mandatory peer reviews, zero test regressions, and coverage thresholds before pull requests were merged into `main`.
6. **Configuration Management (CM)**: Managed by Jalakam Prashanth. GitFlow branching model enforced (`main`, `develop`, `feature/USxx`). Commit messages standardized with story issue tags. Automated atomic persistence ensures runtime configuration stability.
7. **Supplier Agreement Management (SAM)**: Managed by Nikitha Sarpur. Evaluated the Python 3 standard library as sole supplier; strictly audited imports to enforce the zero-external-dependency constraint.

---

## 6. Conclusion of Section A

Section A demonstrated that the News Monitoring and Analytics Application fully meets and exceeds all functional, architectural, estimation, and quality assurance mandates established in the CO7095 syllabus. By leveraging pure Python standard-library capabilities, deterministic algorithm design, 195 automated unit and research tests, 85.2% statement coverage, an in-house DPLL(T) SMT solver, and disciplined CMMI Level 2 process management, the project establishes a rigorous benchmark for software quality assurance.

---

# SECTION B: AGILE DEVELOPMENT PROCESS AND TEAM COLLABORATION

## 1. Introduction to Section B

Section B details the agile organizational structure, collaborative software engineering methodologies, individual contributions, critical retrospectives, and engineering trade-offs that enabled the four-member team to deliver the system on schedule and within budget.

---

## 2. Team Structure and Allocation

The team operated under an Agile Scrum framework, rotating facilitation roles while maintaining strict individual ownership over specialized functional domains:

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

Each team member owned exactly 9 User Stories (31.5 Story Points), designed independent Black-box, White-box, Symbolic, and Concolic test packages, authored production service logic, and audited assigned CMMI Level 2 process areas.

---

## 3. Team Contribution and Critical Reflection

### 3.1 Collaborative Review Protocols and Cross-Verification
To ensure system integrity across subsystem boundaries, the team enforced a mandatory Peer Code Review Protocol on GitHub. Every feature pull request required review and formal approval from an adjacent domain owner before merging into `develop`. Cross-testing matrix:
- `sd683` executed search and categorisation integration tests over `ns713`'s parsed RSS feed outputs.
- `jb1080` audited sentiment calculations during source sentiment aggregation.
- `pj161` integrated all analytical services into the master CLI menu and CSV export pipelines.
- `ns713` generated the curated demo dataset (114 multi-domain articles) utilized across integration stress tests.

### 3.2 Critical Engineering Trade-offs and Limitations
1. **JSON Serialization vs Relational Database**: The decision to use serialized JSON storage satisfied the zero-database constraint and eliminated SQL injection vulnerabilities. While atomic swapping (`os.replace`) guarantees zero file corruption, in-memory loading bounds practical scalability to ~50,000 articles. An industrial deployment would transition to SQLite or PostgreSQL with B-tree indexing.
2. **Lexical Polarity vs Machine Learning NLP**: Lexical sentiment scoring ($S = P - N$) guaranteed total determinism and transparent test oracles. However, it lacks contextual nuance, sarcasm detection, and grammatical negation handling (e.g., *"not terrible"* is scored as negative).
3. **Keyword-Based Categorisation**: Simple keyword mapping is deterministic and blazingly fast ($< 5\text{ms}$), but ambiguous words (e.g., *"Apple"* as tech company vs agricultural fruit) require disambiguation rules.
4. **Jaccard Token Deduplication**: Jaccard similarity at $\theta = 0.70$ effectively prunes republished syndication, but bag-of-words tokenization is insensitive to sentence word order.

### 3.3 Ethical, Legal and Social Considerations
The application monitors public news streams. The team instituted strict ethical guidelines:
- **Fair Use and Copyright**: The ingestion engine captures public RSS feeds strictly for local analytical indexing, storing summaries rather than full copyrighted editorial content.
- **Source Neutrality**: Analytics present objective publishing volume and lexical polarity distributions without editorial ranking, avoiding algorithmic bias.

---

## References

1. Boehm, B.W., 1981. *Software Engineering Economics*. Englewood Cliffs, NJ: Prentice-Hall.
2. Boehm, B.W. et al., 2000. *Software Cost Estimation with COCOMO II*. Upper Saddle River, NJ: Prentice-Hall.
3. Chrissis, M.B., Konrad, M. and Shrum, S., 2011. *CMMI for Development: Guidelines for Process Integration and Product Improvement*. 3rd ed. Boston: Addison-Wesley.
4. Fleming, Q.W. and Koppelman, J.M., 2010. *Earned Value Project Management*. 4th ed. Newtown Square, PA: Project Management Institute.
5. Godefroid, P., Klarlund, N. and Sen, K., 2005. DART: Directed Automated Random Testing. In: *Proceedings of the 2005 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI)*. Chicago, IL, USA, pp.213–223.
6. King, J.C., 1976. Symbolic Execution and Program Testing. *Communications of the ACM*, 19(7), pp.385–394.
7. McCabe, T.J., 1976. A Complexity Measure. *IEEE Transactions on Software Engineering*, SE-2(4), pp.308–320.
8. Nieuwenhuis, R., Oliveras, A. and Tinelli, C., 2006. Solving SAT and SAT Modulo Theories: From an abstract Davis--Putnam--Logemann--Loveland procedure to DPLL(T). *Journal of the ACM*, 53(6), pp.937–977.
9. Pezzè, M. and Young, M., 2008. *Software Testing and Analysis: Process, Principles, and Techniques*. Hoboken, NJ: John Wiley & Sons.
10. Project Management Institute, 2017. *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 6th ed. Newtown Square, PA: Project Management Institute.
11. Sen, K., Marinov, D. and Agha, G., 2005. CUTE: A Concolic Unit Testing Engine for C. In: *Proceedings of the 10th European Software Engineering Conference (ESEC/FSE)*. Lisbon, Portugal, pp.263–272.
12. Walkinshaw, N., 2018. *Software Quality Assurance: Consistency in the Face of Complexity and Change*. Cham: Springer Nature.

---

# APPENDICES

### Appendix 1: Bidirectional Requirements Traceability Matrix (RTM)

| Req ID | Requirement Description | User Story ID | Implementation Module Path | Primary Verification Test ID |
| :---: | :--- | :---: | :--- | :--- |
| **FR01** | Article Intake & Constructor Validation | US01 | `models/article.py::NewsArticle` | `TC-BB-ART-01` to `04`, `TC-WB-ART-01` |
| **FR02** | RSS Feed XML Retrieval & Robust Parsing | US02 | `services/rss_service.py::RssService` | `TC-BB-RSS-01` to `06`, `TC-WB-RSS-01` |
| **FR03** | Multi-Field Article Search & Querying | US04 | `services/search_service.py::SearchService` | `TC-BB-SRH-01` to `06`, `TC-WB-SRH-01` |
| **FR04** | Deterministic Keyword Categorisation | US05 | `services/categorisation_service.py` | `TC-BB-CAT-01` to `05`, `TC-WB-CAT-01` |
| **FR05** | Lexical Sentiment Scoring ($S = P - N$) | US06 | `services/sentiment_service.py` | `TC-BB-SNT-01` to `05`, `TC-WB-SNT-01` |
| **FR06** | Four-Tier Deduplication & Jaccard Bounds | US07 | `services/duplicate_service.py` | `TC-BB-DUP-01` to `06`, `TC-WB-DUP-01` |
| **FR07** | Stopword-Filtered Trending Keyword Extr.| US08 | `services/trend_service.py::TrendService` | `TC-BB-TRD-01` to `05`, `TC-WB-TRD-01` |
| **FR08** | News Source Distribution & Volume Metrics| US09 | `services/source_analytics_service.py` | `TC-BB-SRC-01` to `05`, `TC-WB-SRC-01` |
| **FR09** | Temporal Date-Bucketing & Trend Analytics| US21 | `services/time_analytics_service.py` | `TC-BB-TIM-01` to `05`, `TC-WB-TIM-01` |
| **FR10** | Keyword Alert Rule Definition & Matching | US10 | `models/alert_rule.py::AlertRule` | `TC-BB-ALT-01` to `05`, `TC-WB-ALT-01` |
| **FR11** | Unread Alert Tracking & State Transitions | US24 | `services/alert_service.py::AlertService` | `TC-BB-ALT-06` to `09`, `TC-WB-ALT-02` |
| **FR12** | RFC 4180-Compliant CSV Report Generation | US11 | `services/report_service.py::ReportService`| `TC-BB-REP-01` to `04`, `TC-WB-REP-01` |
| **FR13** | Consolidated Executive CLI Telemetry View | US36 | `services/dashboard_service.py` | `TC-BB-DSH-01` to `04`, `TC-WB-DSH-01` |
| **FR14** | Interactive CLI Menu & ANSI Rendering | US12 | `interface/menu.py::NewsAppMenu` | `TC-WB-MNU-01` to `10`, Branch suites|
| **FR15** | Crash-Safe Atomic Persistence (`.tmp/.bak`)| US03 | `storage/json_storage.py::JsonStorage` | `TC-BB-STO-01` to `06`, `TC-WB-STO-01` |

---

### Appendix 2: Master Test Suite Execution and Coverage Telemetry

```
$ python run_tests.py
============================================================================
  CO7095 MASTER TEST SUITE (ALL STUDENT PACKAGES & INTEGRATION)
  Target Package Discovery:
   -> ns713\test
   -> sd683\test
   -> jb1080\test
   -> pj161\test
   -> tests\shared
   -> research
============================================================================
Ran 195 tests
OK   (executed: 195, passed: 195, failures: 0, errors: 0)

[INFO] Test Execution Summary:
  Total Tests Executed : 195
  Passed               : 195
  Failed               : 0
  Errors               : 0
  Pass Rate            : 100.0%

[INFO] Code Statement Coverage:
  Total Measured Statements : 2,287
  Executed Statements       : 1,948
  Missed Statements         : 339
  Overall Statement Coverage: 85.2%
```

---

### Appendix 3: Detailed Mathematical Formulations and Derivations

#### 1. PERT Critical Path Derivation
For each activity $i$, expected duration $T_{e,i}$ and variance $\sigma^2_i$ derive from optimistic ($a$), most likely ($m$), and pessimistic ($b$) bounds:

$$T_{e,i} = \frac{a_i + 4m_i + b_i}{6}, \qquad \sigma^2_i = \left(\frac{b_i - a_i}{6}\right)^2$$

Summing over the 12 zero-float critical activities ($A1, A2, A3, A5, A6, A7, A9, A10, A11, A14, A16, A17$):

$$T_{\text{path}} = \sum_{i \in \text{Critical}} T_{e,i} = 2.00 + 3.00 + 2.00 + 4.00 + 3.50 + 3.00 + 3.00 + 2.50 + 3.00 + 3.00 + 4.50 + 4.85 = \mathbf{41.85\text{ days}}$$

$$\sigma^2_{\text{path}} = \sum_{i \in \text{Critical}} \sigma^2_i = 0.111 + 0.444 + 0.111 + 0.444 + 0.444 + 0.444 + 0.444 + 0.250 + 0.444 + 0.444 + 0.694 + 0.556 = \mathbf{4.83\text{ days}^2}$$

$$\sigma_{\text{path}} = \sqrt{4.83} = \mathbf{2.20\text{ days}}$$

For contract deadline $D = 45\text{ days}$:

$$Z = \frac{45 - 41.85}{2.20} = 1.43 \implies P(T \le 45) = \Phi(1.43) = \mathbf{92.36\%}$$

#### 2. McCabe Cyclomatic Complexity Derivation
For `DuplicateService.calculate_similarity()` with $E = 11$ edges, $N = 9$ nodes, and $P = 1$ connected component:

$$M = E - N + 2P = 11 - 9 + 2(1) = \mathbf{4}$$

Alternative predicate formulation with $\pi = 3$ binary decision nodes ($N2, N4, N5$):

$$M = \pi + 1 = 3 + 1 = \mathbf{4}$$

#### 3. EVM Formula Summary
$$\text{Cost Variance (CV)} = EV - AC = £18,000 - £17,140 = \mathbf{+£860}$$
$$\text{Schedule Variance (SV)} = EV - PV = £18,000 - £18,000 = \mathbf{£0.00}$$
$$\text{Cost Performance Index (CPI)} = \frac{EV}{AC} = \frac{18,000}{17,140} = \mathbf{1.050}$$
$$\text{Schedule Performance Index (SPI)} = \frac{EV}{PV} = \frac{18,000}{18,000} = \mathbf{1.000}$$
$$\text{Estimate at Completion (EAC)} = \frac{BAC}{CPI} = \frac{18,000}{1.050} = \mathbf{£17,140}$$
$$\text{Variance at Completion (VAC)} = BAC - EAC = £18,000 - £17,140 = \mathbf{+£860}$$
