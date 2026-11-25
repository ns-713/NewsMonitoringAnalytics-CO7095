# Planning Poker Estimation and Sizing Artifact
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Estimation Methodology Notice

> [!IMPORTANT]
> **Planning Poker Estimation Protocol:**
> All 36 user stories were sized during synchronous Planning Poker consensus sessions conducted by Group 19 members using standard Fibonacci cards ($1, 2, 3, 5, 8$). Initial estimates were submitted independently by all four engineers to avoid anchoring bias. Divergent estimates were debated openly with reference to architectural risk, file I/O operations, domain dependencies, and testing overhead until unified team consensus was reached.

---

## 2. Planning Poker Story Point Table (36 User Stories)

| Story ID | Story Title | Assigned Member | Agreed Story Points | Complexity Rationale & Technical Drivers | Group Discussion & Consensus Notes | Estimation Evidence / Card Rounds |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- |
| **US01** | News Article Model | ns713 | **3** | Model validation, UUID generation, serialization, and dictionary reconstruction. | Team discussed field optionality and UUID stability across platforms | Consensus on first round: 3, 3, 3, 3 |
| **US02** | Manual News Entry | ns713 | **3** | CLI input acquisition, field validation, and integration with `NewsService`. | Review input sanitization needs for edge characters and Unicode | Cards: 3, 3, 5, 3 -> Settled at 3 |
| **US03** | News Source Management | ns713 | **3** | URL scheme validation (`http/https/file`), duplicate prevention, metadata tracking. | Protocol support scoped to local file and web feeds | Unanimous agreement: 3, 3, 3, 3 |
| **US04** | Headline and Keyword Search | Sd683 | **3** | Case-insensitive substring matching over collection in memory. | Evaluated in-memory list filtering versus indexed lookups | Cards: 2, 3, 3, 3 -> Settled at 3 |
| **US05** | Source and Date Filtering | Sd683 | **3** | Multi-format date parsing, interval inequality constraints. | Discussed handling malformed date strings gracefully | Cards: 3, 3, 3, 5 -> Settled at 3 |
| **US06** | Initial News Categorisation | Sd683 | **5** | Word boundary regexes across 10 category keyword dictionaries, scoring. | Complex regex matching and tie-breaking fallback to Other | Cards: 5, 5, 5, 8 -> Settled at 5 |
| **US07** | Trending Analytics Foundation | Jb1080 | **3** | Punctuation stripping, stop-word removal, and frequency distribution counters. | Scoped external stop-words list and tokenization rules | Unanimous agreement: 3, 3, 3, 3 |
| **US08** | URL Duplicate Detection | Jb1080 | **3** | Canonical URL normalization (query param stripping, scheme neutrality). | Discussed stripping tracking parameters (ref, utm) | Cards: 3, 3, 3, 3 -> Settled at 3 |
| **US09** | Source Article Counts | Jb1080 | **3** | Grouping collections by source and calculating percentage volume shares. | Straightforward grouping with percentage volume normalization | Cards: 2, 3, 3, 3 -> Settled at 3 |
| **US10** | Keyword Monitoring Rules | Pj161 | **3** | Rule entity definition, category filter constraints, enabled toggle. | Validated persistence structure and rule activation logic | Cards: 3, 3, 3, 3 -> Settled at 3 |
| **US11** | CLI Dashboard Backbone | Pj161 | **5** | Menu loop, ASCII table rendering, ANSI layout, input validation loop. | Terminal formatting and robust navigation state loop | Cards: 5, 5, 8, 5 -> Settled at 5 |
| **US12** | JSON Storage Foundation | Pj161 | **3** | Atomic file replacement, `.bak` generation, and corrupted data recovery. | Atomic write mechanics across Windows and Linux platforms | Cards: 3, 5, 3, 3 -> Settled at 3 |
| **US13** | RSS Feed Collection | ns713 | **5** | Network requests, User-Agent headers, timeout handling, socket exception traps. | Robust error handling when external feed servers are down | Cards: 5, 5, 8, 5 -> Settled at 5 |
| **US14** | RSS Parsing and Normalisation | ns713 | **5** | XML parsing (RSS 2.0 & Atom), missing tag fallbacks, date RFC 822 conversion. | Handling missing tags and heterogeneous XML structures | Cards: 5, 5, 5, 8 -> Settled at 5 |
| **US15** | Duplicate & Import Error Handling | ns713 | **3** | Batch ingestion duplicate checks and statistical counters. | Preventing partial batch insertion during I/O interruptions | Unanimous agreement: 3, 3, 3, 3 |
| **US16** | Sentiment Analysis | Sd683 | **5** | Lexicon token matching, polarity scoring, and transparency audit trail. | Rule-based lexicon with negation and intensifier windows | Cards: 5, 5, 5, 5 -> Unanimous 5 |
| **US17** | Configurable Category Rules | Sd683 | **3** | Dynamic loading and runtime updating of category dictionaries. | File write permissions and dynamic dictionary reloading | Unanimous agreement: 3, 3, 3, 3 |
| **US18** | Advanced News Filters | Sd683 | **3** | Multi-criteria conjunction logic over 5 simultaneous parameters. | Filtering performance on large article collections | Cards: 3, 3, 3, 5 -> Settled at 3 |
| **US19** | Trending Topic Frequency | Jb1080 | **3** | Multi-field extraction, date-specific trend slicing, top-N sorting. | Sorting efficiency and top-N keyword frequency ranking | Unanimous agreement: 3, 3, 3, 3 |
| **US20** | Duplicate Similarity Report | Jb1080 | **3** | Jaccard token index calculation ($\theta \ge 0.70$) and pair comparison loops. | Pairwise loop optimization and candidate comparison bounds | Cards: 3, 5, 3, 3 -> Settled at 3 |
| **US21** | Source Sentiment Analytics | Jb1080 | **3** | Multi-level aggregation (source $\times$ sentiment proportions). | Formulating tone distribution metrics and neutral thresholds | Unanimous agreement: 3, 3, 3, 3 |
| **US22** | Keyword Alerts | Pj161 | **5** | Automatic alert triggering during ingestion, duplicate alert suppression. | Alert generation queue and deduplication key structure | Cards: 5, 5, 5, 5 -> Unanimous 5 |
| **US23** | Alert Management | Pj161 | **3** | Queue viewing, mark as read, mark all as read state machine. | State transitions and persisting notification states | Cards: 2, 3, 3, 3 -> Settled at 3 |
| **US24** | Analytics CSV Reports | Pj161 | **3** | RFC 4180 CSV export generation for articles, categories, trends, and alerts. | Proper quoting and comma escaping in export routines | Unanimous agreement: 3, 3, 3, 3 |
| **US25** | Data Integrity Validation | ns713 | **3** | Exhaustive validation, symbolic execution tree across model attributes. | Testing edge cases, boundary dates, and Unicode strings | Cards: 3, 3, 3, 3 -> Settled at 3 |
| **US26** | Resilient RSS Collection | ns713 | **3** | Fault injection testing (bad URLs, 404s, malformed XML, slow hosts). | Simulating offline conditions and network timeouts | Cards: 3, 3, 5, 3 -> Settled at 3 |
| **US27** | Offline Demonstration Dataset | ns713 | **5** | Generating 105+ diverse synthetic news articles across 10 categories & duplicates. | Ensuring rich semantic variety for demonstration purposes | Cards: 5, 5, 8, 5 -> Settled at 5 |
| **US28** | Sentiment & Categorisation Edge Cases | Sd683 | **3** | Sarcasm, empty inputs, balanced scoring, multi-topic ambiguity. | Boundary value analysis on neutral and compound scores | Cards: 3, 3, 3, 3 -> Settled at 3 |
| **US29** | Combined Search & Filter Integration | Sd683 | **3** | CLI submenu wiring, table presentation, and result formatting. | User experience and intuitive filter prompts in terminal | Unanimous agreement: 3, 3, 3, 3 |
| **US30** | Analytics Validation | Sd683 | **3** | Verifying analytics against known mathematical ground truth fixtures. | Writing assertion fixtures for statistical sums | Cards: 2, 3, 3, 3 -> Settled at 3 |
| **US31** | Time-Based Analytics | Jb1080 | **5** | ISO calendar week bucketing, daily volume, monthly trends, and date recovery. | Calendar week calculations across year and leap boundaries | Cards: 5, 5, 5, 8 -> Settled at 5 |
| **US32** | Trend Comparisons | Jb1080 | **3** | Period-over-period delta calculation and velocity sorting. | Handling keywords appearing in only one time period | Cards: 3, 3, 3, 3 -> Settled at 3 |
| **US33** | Duplicate & Source Reporting | Jb1080 | **3** | Integrated report merging duplicate matches with source breakdown. | Clear formatting of duplicate similarity scores in tables | Unanimous agreement: 3, 3, 3, 3 |
| **US34** | Alert & Dashboard Integration | Pj161 | **3** | Prominent status badges, unread notification counter, quick navigation. | High-visibility unread count indicator on dashboard | Cards: 3, 3, 3, 3 -> Settled at 3 |
| **US35** | Integrated Reporting & Export | Pj161 | **5** | Master report consolidation and exporting all 7 CSV datasets. | File path safety and schema verification across all 7 CSVs | Cards: 5, 5, 5, 8 -> Settled at 5 |
| **US36** | Final CLI Integration & Usability | Pj161 | **3** | End-to-end integration, error trapping, exit confirmation, and polish. | Clean Ctrl+C / EOF handling and graceful menu termination | Cards: 3, 5, 3, 3 -> Settled at 3 |

---

## 3. Workload Balance Analysis

The distribution across team members ensures parity in engineering responsibility and testing load:

| Team Member | Identifier | Student ID | Total Stories | Sprint 1 Points | Sprint 2 Points | Sprint 3 Points | Total Story Points |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Nikitha Sarpur** | `ns713` | 259060190 | 9 | 9 | 13 | 11 | **33** |
| **Sashi Dommaraju** | `Sd683` | 259062044 | 9 | 11 | 11 | 9 | **31** |
| **Jyothi Bandalapati** | `Jb1080` | 259060742 | 9 | 9 | 9 | 11 | **29** |
| **Jalakam Prashanth** | `Pj161` | 259060676 | 9 | 11 | 11 | 11 | **33** |
| **Group 19 Total** | | | **36** | **40** | **44** | **42** | **126** |

- **Sprint 1 Committed**: 40 Story Points (12 Stories)
- **Sprint 2 Committed**: 44 Story Points (12 Stories)
- **Sprint 3 Committed**: 42 Story Points (12 Stories)
- **Project Total**: **126 Story Points** (Team Mean = 31.5 points per engineer)
