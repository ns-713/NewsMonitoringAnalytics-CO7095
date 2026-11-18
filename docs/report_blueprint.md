# CO7095 Coursework Report Blueprint & Authoring Guide
**Module:** CO7095 – Software Measurement and Quality Assurance (2026–2027)  
**Project:** News Monitoring and Analytics Application  
**Word Limit:** Maximum 5,000 words (exclusive of Title Page, Executive Summary, Table of Contents, References, and Appendices)  
**Format:** IEEE / Harvard Academic Technical Report Style  

---

## 1. Executive Word Budget & Structural Allocation

The coursework specification mandates a strict upper limit of **5,000 words**. To ensure comprehensive coverage without exceeding institutional thresholds, the word budget is calibrated across all required sections below:

| Report Section | Section Title | Target Words | Hard Min | Hard Max | Primary Responsible Member |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Section A1** | Introduction & Problem Formulation | 350 | 300 | 400 | Nikitha Sarpur (`ns713`) |
| **Section A2** | System Requirements & SQA Specification | 450 | 400 | 500 | Sashi Dommaraju (`sd683`) |
| **Section A3** | Architectural & Detailed Design | 600 | 550 | 650 | Nikitha Sarpur (`ns713`) |
| **Section A4** | Implementation Architecture & Key Algorithms | 700 | 650 | 750 | Sashi / Jyothi (`sd683` / `jb1080`) |
| **Section A5** | Software Verification & Testing Methodology | 950 | 900 | 1000 | All Members (240 words each) |
| **Section A6** | Software Measurement, Metrics & Estimation | 800 | 750 | 850 | Jyothi Bandalapati (`jb1080`) |
| **Section A7** | Process Improvement & CMMI Level 2 Audit | 500 | 450 | 550 | Jalakam Prashanth (`pj161`) |
| **Section B1** | Agile Team Management, Scrum & Contributions | 350 | 300 | 400 | Nikitha / Prashanth |
| **Section B2** | Critical Reflective Analysis & Limitations | 300 | 250 | 350 | All Members |
| **Total Core** | *(Excluding Front Matter, References & Appendices)* | **5,000** | **4,550** | **5,000** | **Balanced Team Effort** |

---

## 2. Section-by-Section Authoring Blueprint

---

### Section A1: Introduction & Problem Formulation
- **Target Word Count:** 350 words
- **Primary Owner:** Nikitha Sarpur (`ns713`)
- **Core Focus:**
  - Contextualise the challenge of modern multi-source news monitoring: syndication clutter, information overload, API rate limits, and non-deterministic cloud black boxes.
  - Formulate the engineering objective: a robust, pure Python standard-library application with local persistence, multi-criteria filtering, lexical sentiment classification, duplicate detection, and keyword alert mechanisms.
  - State the academic purpose: evaluating software measurement theories (PERT, COCOMO I/II, EVM) and quality assurance disciplines (Equivalence Partitioning, Boundary Value Analysis, Decision Tables, White-box Statement/Branch Coverage, Symbolic Execution, and Concolic Testing).
- **Key Artifacts & Tables to Embed:**
  - *Figure 1.1*: High-level contextual boundary diagram of the News Monitoring and Analytics Application.
  - *Table 1.1*: High-level system goals mapped to CO7095 learning outcomes.
- **Common Pitfalls to Avoid:**
  - Do NOT spend words providing generic journalism history.
  - Do NOT claim machine learning or deep neural network capabilities; explicitly state that algorithms are rule-based and lexical.

---

### Section A2: System Requirements & SQA Specification
- **Target Word Count:** 450 words
- **Primary Owner:** Sashi Dommaraju (`sd683`)
- **Core Focus:**
  - Present the functional requirements baseline (FR01 through FR15) condensed into a clear categorization (Ingestion, Analysis, Monitoring, Persistence, Reporting).
  - Explicitly detail Non-Functional Requirements (NFRs): Reliability (zero data corruption via atomic writes), Performance (< 50ms query latency for 1,000 articles), Maintainability (cyclomatic complexity $\le 10$), and Portability (pure standard library on Python 3.10+).
  - Link requirements to Agile Epics and User Stories (US01 to US36).
- **Key Artifacts & Tables to Embed:**
  - *Table 2.1*: Functional Requirements Summary Matrix with associated User Story IDs and Verification Criteria.
  - *Table 2.2*: Non-Functional Requirements and Quantitative Quality Gates.
- **Cross-Reference:** Link to `docs/requirements_specification.md` and `docs/user_stories.md`.

---

### Section A3: Architectural & Detailed Design
- **Target Word Count:** 600 words
- **Primary Owner:** Nikitha Sarpur (`ns713`)
- **Core Focus:**
  - Detail the 4-tier layered architectural pattern: Presentation Layer (`interface/`), Service/Business Logic Layer (`services/`), Data Access/Storage Layer (`storage/`), and Domain Model Layer (`models/`).
  - Justify the choice of loose coupling and dependency injection: Services receive storage handles, ensuring unit-testability with in-memory mocks.
  - Explain data safety: Atomic write design using temporary swap files (`.tmp`) and file replacement (`os.replace`), backed by automatic `.bak` snapshot rotation.
- **Key Artifacts & Figures to Embed:**
  - *Figure 3.1*: Layered Architectural Block Diagram with directional dependencies.
  - *Figure 3.2*: UML Class Diagram illustrating `NewsArticle`, `NewsSource`, `AlertRule`, and `Alert` entities.
  - *Figure 3.3*: Sequence Diagram of RSS Ingestion, Duplicate Checking, and Alert Triggering pipeline.
- **Cross-Reference:** Link to `docs/architecture.md`.

---

### Section A4: Implementation Architecture & Key Algorithms
- **Target Word Count:** 700 words
- **Primary Owners:** Sashi Dommaraju (`sd683`) & Jyothi Bandalapati (`jb1080`)
- **Core Focus:**
  - **Lexical Sentiment Analysis Algorithm**: Explain the scoring formula:
    $$\text{Score} = \sum_{w \in T} \mathbb{I}(w \in \mathcal{P}) - \sum_{w \in T} \mathbb{I}(w \in \mathcal{N})$$
    where $\mathcal{P}$ and $\mathcal{N}$ are configured positive and negative word sets. Detail boundary classifications ($\text{Score} > 0 \implies \text{Positive}$, $\text{Score} < 0 \implies \text{Negative}$, $\text{Score} = 0 \implies \text{Neutral}$). Discuss linguistic limitations (negation, sarcasm, idiom blindness).
  - **Rule-Based Categorisation**: Discuss maximum weighted keyword hit strategy and graceful fallback to 'Other'.
  - **4-Tier Duplicate Detection**:
    1. Canonical URL exact match.
    2. Case/whitespace/punctuation normalised headline match.
    3. Alphanumeric token fingerprint match.
    4. Token-based Jaccard similarity coefficient:
       $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
       with empirical threshold $\theta = 0.70$.
  - **RSS Parsing & Fault Tolerance**: Standard library `urllib.request` and `xml.etree.ElementTree` handling malformed XML without halting the execution loop.
- **Key Artifacts & Code Snippets to Embed:**
  - *Listing 4.1*: Normalisation and Jaccard token computation snippet.
  - *Listing 4.2*: Atomic file write algorithm snippet from `json_storage.py`.
- **Cross-Reference:** Link to `services/duplicate_service.py` and `services/sentiment_service.py`.

---

### Section A5: Software Verification & Testing Methodology
- **Target Word Count:** 950 words (Highest weight section)
- **Primary Owners:** All 4 Team Members (Allocated by module ownership)
- **Core Focus:**
  - **Testing Strategy & Infrastructure**: Master test suite using `unittest`, driven by `run_tests.py` with custom standard-library statement tracing (`sys.settrace`). 139 tests passing, 0 failures, 0 errors, in 4.4 seconds.
  - **Black-Box Testing (250 words - Sashi/Nikitha)**:
    - Equivalence Partitioning (EP) and Boundary Value Analysis (BVA) applied to headline length, URL formatting, date ranges, and sentiment score thresholds.
    - Decision Table Testing (DTT) on multi-condition search queries and alert rule evaluation.
    - State Transition Testing (STT) on `Alert` states (`UNREAD` $\to$ `READ`).
  - **White-Box Testing (250 words - Jyothi/Prashanth)**:
    - Basis path analysis, Cyclomatic Complexity ($M = E - N + 2P$), Statement Coverage, and Branch Coverage.
    - Present empirical coverage results: `duplicate_service` (95.7%), `article` (95.2%), `search_service` (93.7%), `categorisation_service` (92.3%), `alert_service` (91.7%), `trend_service` (90.9%).
  - **Symbolic Execution Study (225 words - Nikitha/Jyothi)**:
    - Formal path condition analysis on `NewsArticle.validate()`, `SentimentService.classify_score()`, and `DuplicateService.calculate_similarity()`.
    - Mathematical formulation of path predicates ($PC_1, PC_2, PC_3$) and constraint satisfaction using SymPy/Z3 solver logic.
  - **Concolic Testing Study (225 words - Sashi/Prashanth)**:
    - Concrete-symbolic execution on `RssService.parse_rss_xml()` and `ReportService.escape_csv_field()`.
    - Inversion of branch condition flags to systematically discover corner cases (e.g., embedded commas, newlines, malformed XML closing tags).
- **Key Artifacts & Tables to Embed:**
  - *Table 5.1*: Master Test Execution Summary Table (Test Counts, Passed, Coverage % per module).
  - *Figure 5.1*: Control Flow Graph (CFG) of `calculate_similarity()` with labeled cyclomatic paths.
  - *Table 5.2*: Symbolic Execution Path Condition Table for `NewsArticle.validate()`.
- **Cross-Reference:** Link to `docs/test_plan.md`, `docs/blackbox_testing.md`, `docs/whitebox_testing.md`, `docs/symbolic_execution.md`, and `docs/concolic_testing.md`.

---

### Section A6: Software Measurement, Metrics & Estimation
- **Target Word Count:** 800 words
- **Primary Owner:** Jyothi Bandalapati (`jb1080`)
- **Core Focus:**
  - **Codebase Physical Sizing**:
    - Application Core: 2,741 executable physical SLOC.
    - Test Suite & Infrastructure: 2,534 physical SLOC.
    - Total Monitored Codebase: 5,275 SLOC.
  - **PERT Critical Path Analysis**:
    - 17 structured activities across 3 sprints.
    - Expected activity time $T_e = \frac{a + 4m + b}{6}$, variance $\sigma^2 = \left(\frac{b - a}{6}\right)^2$.
    - Critical Path: A1 $\to$ A2 $\to$ A3 $\to$ A5 $\to$ A6 $\to$ A7 $\to$ A9 $\to$ A10 $\to$ A11 $\to$ A14 $\to$ A16 $\to$ A17.
    - Expected Total Duration: $41.85\text{ working days}$; Critical Path Variance: $4.83\text{ days}^2$ ($\sigma = 2.20\text{ days}$).
    - Probability of completion within 45 days: $Z = \frac{45 - 41.85}{2.20} = 1.43 \implies 92.36\%$.
  - **COCOMO I Organic Mode**:
    - Model: $\text{Effort} = 2.4 \times (KLOC)^{1.05}$, $\text{TDEV} = 2.5 \times (\text{Effort})^{0.38}$.
    - Application sizing ($2.741\text{ KLOC}$): $\text{Effort} = 6.74\text{ Person-Months}$, $\text{TDEV} = 5.15\text{ Calendar Months}$.
  - **COCOMO II Post-Architecture Model**:
    - 5 Scale Factors ($\sum SF = 18.97 \implies E = 1.104$).
    - 17 Cost Drivers ($\prod EM = 0.985$).
    - Effort: $A \times (\text{Size})^E \times \prod EM = 2.94 \times (2.741)^{1.104} \times 0.985 = 8.87\text{ Person-Months}$.
    - Comparative analysis explaining why COCOMO II yields higher effort (rigorous verification and automated test suite cost drivers).
  - **Earned Value Management (EVM)**:
    - Metrics tracked across 3 sprints (126 total Planned Story Points).
    - Sprint 3 Results: $PV = £18,000$, $EV = £18,000$, $AC = £17,140$.
    - Schedule Performance Index: $SPI = 1.00$; Cost Performance Index: $CPI = 1.05$.
    - Positive Cost Variance $CV = +£860$; Estimate at Completion $EAC = £17,140$.
- **Key Artifacts & Tables to Embed:**
  - *Figure 6.1*: PERT Activity-on-Node (AON) Network Diagram highlighting the Critical Path.
  - *Table 6.1*: Comparative Sizing and Estimation Summary (COCOMO I vs COCOMO II vs Actual Sprint Pacing).
  - *Table 6.2*: EVM Progression Table (PV, EV, AC, CPI, SPI across Sprints 1, 2, and 3).
- **Cross-Reference:** Link to `docs/pert_analysis.md`, `docs/cocomo_model_1.md`, `docs/cocomo_model_2.md`, and `docs/evm_analysis.md`.

---

### Section A7: Process Improvement & CMMI Level 2 Audit
- **Target Word Count:** 500 words
- **Primary Owner:** Jalakam Prashanth (`pj161`)
- **Core Focus:**
  - Explain the CMMI Level 2 ("Managed") quality management framework.
  - Synthesize the internal audit conducted across all 7 Process Areas:
    1. **Requirements Management (REQM)**: Bi-directional traceability from User Stories (US01–US36) to code to tests.
    2. **Project Planning (PP)**: WBS, PERT scheduling, and Planning Poker estimation (126 story points).
    3. **Project Monitoring & Control (PMC)**: Sprint burndown, weekly milestone reviews, EVM tracking.
    4. **Supplier Agreement Management (SAM)**: Formal criteria governing third-party libraries (strictly standard library, optional PyPI tools audited).
    5. **Measurement & Analysis (MA)**: Systematic metrics tracking (SLOC, cyclomatic complexity, code coverage %, test pass rates).
    6. **Process & Product Quality Assurance (PPQA)**: Peer review checklists, branch protection, pull request reviews.
    7. **Configuration Management (CM)**: Git branching policy (`main`, `develop`, `feature/*`), baseline tagging, and atomic data storage.
  - Transparently report findings: 100% compliance across audited specific goals, with action plans for non-blocking observations.
- **Key Artifacts & Tables to Embed:**
  - *Table 7.1*: CMMI Level 2 Process Area Compliance Matrix with specific artifacts verified.
- **Cross-Reference:** Link to `docs/cmmi_level_2_audit.md`.

---

### Section B1: Team Management, Agile Scrum & Contributions
- **Target Word Count:** 350 words
- **Primary Owners:** Nikitha Sarpur (`ns713`) & Jalakam Prashanth (`pj161`)
- **Core Focus:**
  - Summarize the Agile Scrum workflow: 3 Sprints of 2 weeks duration each.
  - Planning Poker estimation session (Fibonacci sequence: 1, 2, 3, 5, 8) totaling 126 Story Points evenly distributed (31.5 points per member).
  - Team contribution matrix: Explicitly articulate the balanced technical allocation across all 4 student engineers.
  - Git branching strategy, commit discipline, pull request reviews, and continuous integration testing.
- **Key Artifacts & Tables to Embed:**
  - *Table 8.1*: 4-Member Contribution Summary Matrix (Module Ownership, Story Points, Test Suites, Audit Roles).
  - *Figure 8.1*: Git Branching & Peer Review Workflow Diagram.
- **Cross-Reference:** Link to `docs/agile_plan.md`, `docs/planning_poker.md`, and `docs/contribution_matrix.md`.

---

### Section B2: Critical Reflective Analysis & Limitations
- **Target Word Count:** 300 words
- **Primary Owners:** All 4 Team Members
- **Core Focus:**
  - Technical Limitations: Lexical sentiment analysis lacks contextual disambiguation (sarcasm, negation handling); RSS collection requires network availability or fallback to demo dataset; memory footprint scales with JSON file size.
  - SQA Reflection: Value of combining black-box partition testing with white-box branch coverage and formal symbolic execution.
  - Future Work: Inverted indexing for sub-millisecond search at scale, SQLite persistence layer, and pluggable NLTK/VADER tokenisation.
- **Common Pitfalls to Avoid:**
  - Do NOT frame limitations as "mistakes"; present them as deliberate engineering trade-offs made within the constraint of zero third-party dependencies.

---

### Section B3: Academic References & Bibliography
- **Style:** IEEE or Harvard Academic Citation Style.
- **Key Academic Sources to Cite:**
  1. Boehm, B. et al. (2000) *Software Cost Estimation with COCOMO II*. Prentice Hall.
  2. CMMI Product Team (2010) *CMMI for Development, Version 1.3*. Software Engineering Institute, Carnegie Mellon University.
  3. Fleming, Q. W. and Koppelman, J. M. (2010) *Earned Value Project Management*. 4th edn. Project Management Institute.
  4. King, J. C. (1976) 'Symbolic execution and program testing', *Communications of the ACM*, 19(7), pp. 385–394.
  5. Sen, K., Marinov, D. and Agha, G. (2005) 'CUTE: a concolic unit testing engine for C', *ACM SIGSOFT Software Engineering Notes*, 30(5), pp. 263–272.
  6. Myers, G. J., Sandler, C. and Badgett, T. (2011) *The Art of Software Testing*. 3rd edn. John Wiley & Sons.
  7. McCabe, T. J. (1976) 'A complexity measure', *IEEE Transactions on Software Engineering*, SE-2(4), pp. 308–320.
  8. Project Management Institute (2021) *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 7th edn. PMI.

---

### Section B4: Appendices (Zero Penalty on Word Count)
The following documents from the repository should be incorporated as formal Appendices:
- **Appendix 1: Requirements Traceability Matrix (RTM)** (`docs/requirements_specification.md`)
- **Appendix 2: Complete User Stories Catalog (US01–US36)** (`docs/user_stories.md`)
- **Appendix 3: Master Test Execution Logs & Coverage Tables** (`docs/blackbox_testing.md`, `docs/whitebox_testing.md`)
- **Appendix 4: Mathematical Sizing & PERT Calculations** (`docs/pert_analysis.md`, `docs/cocomo_model_1.md`, `docs/cocomo_model_2.md`)
- **Appendix 5: EVM Sprint Ledger & Equations** (`docs/evm_analysis.md`)
- **Appendix 6: CMMI Level 2 Managed Audit Protocols & Checklists** (`docs/cmmi_level_2_audit.md`)
- **Appendix 7: Detailed Individual Contribution Matrix** (`docs/contribution_matrix.md`)

---

## 3. Formatting, Proofreading & Submission Checklist

- [ ] **Word Count Compliance**: Core report body strictly between 4,500 and 5,000 words.
- [ ] **Anonymous / Student Details**: Ensure all four student names and university IDs are prominent on the title page:
  - Nikitha Sarpur (ID: 259060190)
  - Sashi Dommaraju (ID: 259062044)
  - Jyothi Bandalapati (ID: 259060742)
  - Jalakam Prashanth (ID: 259060676)
- [ ] **Figure & Table Numbering**: All figures and tables cited in text sequentially (e.g., Figure 1.1, Table 2.1).
- [ ] **Equation Typography**: All mathematical formulas rendered in clean LaTeX notation with defined variables.
- [ ] **Zero Fabricated Data**: All test numbers (139 tests, 100% pass, 4.4s execution) and coverage percentages directly match output from `python run_tests.py`.
- [ ] **PDF Export**: Generate final submission PDF from LaTeX/Word ensuring font embedding and high-contrast vector diagrams.

---
*End of Coursework Report Blueprint — CO7095 News Monitoring and Analytics Application.*
