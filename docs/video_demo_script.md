# CO7095 Software Measurement and Quality Assurance (2026–2027)
# Comprehensive Video Demonstration Script

**Project Title:** News Monitoring and Analytics Application  
**Module:** CO7095 – Software Measurement and Quality Assurance  
**Academic Year:** 2026–2027  
**Target Duration:** ~12–15 Minutes  
**Demonstration Format:** Screen recording with synchronized audio narration, terminal capture, PyCharm IDE walkthrough, and slide/diagram commentary.

---

## 1. Presenter Roster & Role Allocations

| Team Member | Student ID | System Username | Script Roles & Segments Owned |
| :--- | :--- | :--- | :--- |
| **Nikitha Sarpur** (Lead) | 259060190 | `ns713` | Opening, Problem Statement, Architecture, Storage, RSS Engine, White-box/Symbolic Demo |
| **Sashi Dommaraju** | 259062044 | `sd683` | Article Management, Search Engine, Rule-Based Categorisation, Lexical Sentiment Analysis |
| **Jyothi Bandalapati** | 259060742 | `jb1080` | Multi-tiered Duplicate Detection, Trending Topics, Source Analytics, Time Analytics |
| **Jalakam Prashanth** | 259060676 | `pj161` | Keyword Monitoring & Alerts, Reporting & CSV Exports, Dashboard, Test Suite & Measurement Wrap-up |

---

## 2. Technical Preparation Checklist Before Recording

1. **Environment Verification**:
   - PyCharm 2026.x Community or Professional installed on standard university lab machine.
   - Python 3.10+ virtual environment activated: `venv\Scripts\activate` (Windows PowerShell).
   - Working Directory: `NewsMonitoringAnalytics_CO7095/`.
   - Terminal font set to Consolas/Courier, 14pt, with dark background for clear screen capture.
2. **Data State Initialization**:
   - Ensure `data/articles.json`, `data/sources.json`, `data/alert_rules.json`, and `data/alerts.json` exist.
   - If clean slate desired: start with empty arrays `[]` in `data/*.json` so the live demo loading of 114 synthetic articles can be witnessed on screen.
3. **Display Configuration**:
   - Resolution: 1920x1080 at 60 fps.
   - PyCharm left pane: Project Explorer showing modular directory structure.
   - PyCharm bottom pane: Terminal running interactive CLI.
   - Secondary monitor/split-screen: Coverage reports and Markdown architectural diagrams.

---

## 3. Detailed Master Timeline & Storyboard

```
00:00 - 01:15  | Segment 1: Title, Team Introduction & Problem Formulation (Nikitha)
01:15 - 02:30  | Segment 2: System Architecture & PyCharm Project Tour (Nikitha)
02:30 - 04:00  | Segment 3: Application Launch, Data Ingestion & RSS Collection (Nikitha)
04:00 - 06:00  | Segment 4: Article Operations, Multi-Criteria Search & Sentiment (Sashi)
06:00 - 07:30  | Segment 5: Automated Categorisation & Category Keyword Explanations (Sashi)
07:30 - 09:30  | Segment 6: Duplicate Detection & Token Jaccard Analysis (Jyothi)
09:30 - 11:00  | Segment 7: Trending Topics, Source Reliability & Time Analytics (Jyothi)
11:00 - 12:45  | Segment 8: Real-Time Keyword Alerts, CSV Exports & Executive Dashboard (Prashanth)
12:45 - 14:15  | Segment 9: Test Suite Execution, Code Coverage & Symbolic Testing (All)
14:15 - 15:00  | Segment 10: Measurement Highlights (COCOMO, PERT, EVM, CMMI) & Conclusion (Nikitha)
```

---

## 4. Segment-by-Segment Demonstration Script

### Segment 1: Title, Introduction & Problem Formulation
- **Timestamp:** 00:00 – 01:15
- **Presenter:** Nikitha Sarpur (`ns713`)
- **Visual:** Title slide displaying Coursework Information, Project Name, Team Roster, and Coursework Objectives. Transition to PyCharm editor.

**Spoken Script:**
> *"Hello and welcome to our demonstration of the News Monitoring and Analytics Application, developed for the CO7095 Software Measurement and Quality Assurance module for the 2026–2027 academic session at the University of Leicester.*
>
> *I am Nikitha Sarpur, the Scrum Master and lead software engineer. Joining me are my project colleagues Sashi Dommaraju, Jyothi Bandalapati, and Jalakam Prashanth.*
>
> *In today's digital information landscape, news monitoring faces three critical bottlenecks: high computational overhead from heavy machine learning pipelines, vulnerability to paid API deprecations, and lack of rigorous verification. Our goal was to engineer a robust, backend-focused Python 3 application using purely standard libraries that delivers enterprise-grade news ingestion, multi-tiered duplicate detection, rule-based sentiment and categorisation, trend analytics, and real-time keyword alerting.*
>
> *Crucially, this project was developed under strict Software Quality Assurance principles, adhering to CMMI Level 2 Managed processes, verified through black-box, white-box, symbolic execution, and concolic test generation. Let us now examine the architectural layout."*

---

### Segment 2: Architecture & PyCharm Setup
- **Timestamp:** 01:15 – 02:30
- **Presenter:** Nikitha Sarpur (`ns713`)
- **Visual:** PyCharm IDE screen. Expanding the `NewsMonitoringAnalytics_CO7095/` project tree in the Project Explorer. Highlighting `models/`, `services/`, `storage/`, `interface/`, `tests/`, and `docs/`.

**Actions in PyCharm:**
1. Click on `models/` → open `article.py`. Highlight the `NewsArticle` dataclass with its UUID generation, ISO timestamps, and strict validation method.
2. Click on `storage/` → open `json_storage.py`. Point out atomic file writing (`os.replace`) and automated `.bak` snapshot recovery.
3. Click on `tests/` → expand subdirectories showing `ns713/`, `sd683/`, `jb1080/`, `pj161/`, and `shared/`.

**Spoken Script:**
> *"As seen in our PyCharm workspace, the project strictly isolates responsibilities across a 4-tier layered architecture: Domain Models, File-Based Atomic Persistence, Business Logic Services, and an Interactive Presentation CLI.*
>
> *In `models/article.py`, each news item is encapsulated in an immutable entity with full input sanitisation, preventing empty headlines or invalid URLs from polluting system memory. In `storage/json_storage.py`, we implemented atomic writes using temporary swap files and automated `.bak` backups to ensure zero data corruption in the event of unexpected power loss or SIGINT termination.*
>
> *Our testing hierarchy mirrors team member allocations, ensuring 100% individual accountability across black-box partitions, branch coverage, symbolic paths, and concolic constraint tests. Let us run the application."*

---

### Segment 3: Application Launch & Data Ingestion
- **Timestamp:** 02:30 – 04:00
- **Presenter:** Nikitha Sarpur (`ns713`)
- **Visual:** Terminal window inside PyCharm. Running `python main.py`. Main Menu displays 20 options (0 to 19).

**Terminal Commands & Menu Inputs:**
```bash
python main.py
```
*Selection:* `18` (Load Demo Dataset)  
*Confirm Prompt:* `y`  
*Selection:* `1` (List All Articles)  
*Selection:* `8` (Collect News from RSS Feeds - Offline Demo Mode)

**Spoken Script:**
> *"Starting the application with `python main.py`, we are greeted by our interactive 20-function dashboard menu. To demonstrate immediate system utility on lab computers without requiring live network connectivity, we select Option 18 to load our curated synthetic demo dataset.*
>
> *Notice that 114 structured articles spanning 10 distinct domains—including Politics, Technology, Health, and Science—are atomically ingested into `data/articles.json`.*
>
> *Next, we navigate to Option 8 to demonstrate our RSS Collection Engine. The engine supports live XML downloads via `urllib.request` as well as an offline fail-safe parser. When parsing RSS feeds, each `<item>` node is safely extracted using standard `xml.etree.ElementTree`. If network connectivity is unavailable, the system safely isolates the fault, logs the diagnostic without crashing, and populates standard article models with RFC 822 date conversion. I will now hand over to Sashi to demonstrate article management, search, and sentiment analysis."*

---

### Segment 4: Article Management, Search & Sentiment Analysis
- **Timestamp:** 04:00 – 06:00
- **Presenter:** Sashi Dommaraju (`sd683`)
- **Visual:** PyCharm terminal. Demonstrating manual article addition, multi-criteria filtering, and lexical sentiment scoring.

**Terminal Commands & Menu Inputs:**
```text
Select Option: 2 (Add Article Manually)
Headline: "Autonomous Solar Drone Sets Global Flight Endurance Record"
Description: "Engineers celebrate major renewable breakthrough in green aviation."
Content: "A breakthrough solar aircraft completed 30 continuous days aloft without fossil fuel."
Source Name: "Green Tech Journal"
Source URL: "https://greentechjournal.org"
Article URL: "https://greentechjournal.org/solar-drone-record-2026"
Category (Optional): [Press Enter for Auto]

Select Option: 5 (Search Articles)
Select Search Criterion: 1 (Headline Search)
Enter Search Query: "drone"

Select Option: 11 (Sentiment Analysis Breakdown)
Enter Article ID: [Select newly added article ID]
```

**Spoken Script:**
> *"Thank you, Nikitha. I am Sashi Dommaraju, responsible for news searching, rule-based categorisation, and sentiment services.*
>
> *In Option 2, we manually add a new article regarding solar drone technology. Notice that our input validator enforces mandatory field presence while automatically calculating article timestamps and initialising metadata.*
>
> *Selecting Option 5 brings up our multi-criteria search engine. Users can filter articles by headline substring, body content, source name, category, sentiment label, or combined boolean filters. Searching for 'drone' instantly returns our newly registered article in under 2 milliseconds.*
>
> *Moving to Option 11, we examine the lexical sentiment analysis engine. Rather than relying on black-box or non-deterministic ML models, our system computes sentiment deterministically: Sentiment Score equals Positive Word Matches minus Negative Word Matches. For our solar drone article, words like 'breakthrough', 'celebrate', and 'renewable' produce a score of +3, correctly classifying the article as Positive. The system outputs the exact matched lexical tokens, providing full explainability."*

---

### Segment 5: Automated Categorisation Engine
- **Timestamp:** 06:00 – 07:30
- **Presenter:** Sashi Dommaraju (`sd683`)
- **Visual:** PyCharm terminal. Demonstrating batch re-categorisation and category explanation. Opening `config/category_keywords.json` in PyCharm to show the configuration.

**Terminal Commands & Menu Inputs:**
```text
Select Option: 10 (Categorise All Uncategorised Articles)
Select Option: 4 (View Single Article Details)
Enter Article ID: [ID of solar drone article]
```

**Spoken Script:**
> *"Under the hood, `CategorisationService` inspects the combined headline, description, and content text against 10 configurable keyword dictionaries loaded from `config/category_keywords.json`. Categories include Politics, Business, Technology, Health, Sports, Education, Science, Environment, World News, and Entertainment.*
>
> *Each matching keyword increments the category score. The category with the highest weight is assigned. In case of zero keyword matches, the system gracefully falls back to 'Other'. Furthermore, our system records the specific triggering keywords—in this case, 'solar', 'renewable', and 'aviation'—enabling full testability during equivalence partitioning. I will now hand over to Jyothi to demonstrate duplicate detection and analytics."*

---

### Segment 6: Multi-Tiered Duplicate News Detection
- **Timestamp:** 07:30 – 09:30
- **Presenter:** Jyothi Bandalapati (`jb1080`)
- **Visual:** PyCharm terminal. Selecting Option 12 (Detect Duplicate News Articles). Reviewing on-screen duplicate detection results.

**Terminal Commands & Menu Inputs:**
```text
Select Option: 12 (Detect Duplicate News Articles)
Select Option: 2 (Add Article Manually - Injecting Near-Duplicate)
Headline: "UK Inflation Drops to 2.1 Percent in October 2026 Official Report"
Description: "Consumer price index cools as energy and food costs moderate."
Content: "Office for National Statistics data confirms annual inflation slowed."
Source Name: "Economic Times"
Source URL: "https://economictimes.com"
Article URL: "https://economictimes.com/uk-inflation-oct-2026-reuters"

Select Option: 12 (Run Duplicate Detection Report)
```

**Spoken Script:**
> *"Thank you, Sashi. I am Jyothi Bandalapati. I spearheaded duplicate news detection, trending topics, and source/time analytics.*
>
> *In news aggregation, wire service syndication causes widespread article duplication. Our `DuplicateService` implements a 4-tier filtering hierarchy:*
> 1. *Tier 1: Canonical URL Matching.*
> 2. *Tier 2: Case- and punctuation-normalised headline string equality.*
> 3. *Tier 3: Alphanumeric headline fingerprinting.*
> 4. *Tier 4: Token-based Jaccard similarity scoring with a calibrated threshold of theta equals 0.70.*
>
> *As demonstrated on screen, our demo dataset contains deliberate duplicate pairs—such as the BBC and Guardian coverage of UK inflation figures. When we execute Option 12, the duplicate detector scans the 114 articles, calculates token set intersections over unions, and flags the pair with a Jaccard score of 0.875, clearly annotating the reason as 'Likely Headline Duplicate (Jaccard >= 0.70)'. This prevents redundant notifications and ensures data integrity."*

---

### Segment 7: Trending Topics, Source Analytics & Time Trends
- **Timestamp:** 09:30 – 11:00
- **Presenter:** Jyothi Bandalapati (`jb1080`)
- **Visual:** PyCharm terminal. Demonstrating Options 13, 14, and 15.

**Terminal Commands & Menu Inputs:**
```text
Select Option: 13 (View Trending Topics & Keywords)
Select Option: 14 (View Source Analytics & Distribution)
Select Option: 15 (View Time-Based News Analytics)
Choose sub-option: 1 (Daily Statistics)
```

**Spoken Script:**
> *"In Option 13, we examine the Trending Topics engine. By stripping out 150 configurable English stop words from `config/stop_words.json`, the service computes term frequency distributions across all active articles. Keywords such as 'inflation', 'renewable', 'ai', and 'healthcare' emerge at the top.*
>
> *Selecting Option 14 presents Source Analytics. We can observe volume distributions across Reuters, BBC News, TechCrunch, and Nature. We must emphasize an essential ethical and measurement principle embedded in our software: article volume measures publishing activity, not factual accuracy or journalistic credibility.*
>
> *In Option 15, Time-Based Analytics groups articles across daily, ISO calendar weekly, and monthly buckets. The system tracks category velocity and sentiment shifts over time, handling diverse date formats via Python's standard `email.utils` and `datetime` libraries. I will now hand over to Prashanth to present Alerts, Reports, and the Executive Dashboard."*

---

### Segment 8: Keyword Alerts, CSV Exports & Executive Dashboard
- **Timestamp:** 11:00 – 12:45
- **Presenter:** Jalakam Prashanth (`pj161`)
- **Visual:** PyCharm terminal. Demonstrating Option 16 (Keyword Alert Rules), Option 17 (View Active Alerts), Option 19 (Export Reports to CSV), and Option 0 (Executive Dashboard). Showing generated CSV files in `reports/generated/`.

**Terminal Commands & Menu Inputs:**
```text
Select Option: 16 (Manage Keyword Alert Rules)
Sub-option: 1 (List Current Alert Rules)
Sub-option: 2 (Add New Rule)
Keyword: "cybersecurity"
Description: "Critical security notifications"
Category Filter: "Technology"

Select Option: 17 (View Generated Alerts)
Select Option: 19 (Export Analytics Reports to CSV)
Select Option: 0 (View Executive Dashboard)
```

**Spoken Script:**
> *"Thank you, Jyothi. I am Jalakam Prashanth. I designed the alert monitoring engine, reporting system, and CLI dashboard.*
>
> *Under Option 16, users establish keyword monitoring predicates with optional category restrictions. Whenever new articles are ingested—either via RSS or manual input—the `AlertService` scans the content against all active rules. If an article matches, an unread alert entity is persisted to `data/alerts.json`. In Option 17, users can review alert metadata, mark alerts as acknowledged, and filter by status.*
>
> *Option 19 generates 7 comprehensive, RFC 4180-compliant CSV reports in the `reports/generated/` folder, covering article catalogues, category spreads, sentiment tallies, source distributions, trending keywords, duplicate audit logs, and temporal metrics.*
>
> *Finally, Option 0 presents our Executive CLI Dashboard. In a single consolidated ASCII view, the dashboard presents total volume, active sources, monitored rules, pending alerts, sentiment distribution, top categories, and the latest news feed. Let us now examine our verification results."*

---

### Segment 9: Verification Suite, Code Coverage & Symbolic Testing
- **Timestamp:** 12:45 – 14:15
- **Presenter:** All Members (Nikitha leading)
- **Visual:** PyCharm terminal. Exiting main application (`Option 20`). Running `python run_tests.py`. Inspecting the test execution output and statement coverage table. Opening `ns713/test/symbolic/symbolic_execution/test_symbolic_article_validation.py` in editor.

**Terminal Commands:**
```bash
python run_tests.py
```

**Spoken Script:**
> **Nikitha:** *"We now exit the interactive menu and run our master automated test suite using `python run_tests.py`.*
>
> *Notice that all 195 automated tests pass with 0 errors and 0 failures. Our custom tracer—built using Python's native `trace` module—reports statement coverage across all core services:*
> - *`duplicate_service.py`: 95.8%*
> - *`article.py`: 88.8%*
> - *`dashboard_service.py`: 94.7%*
> - *`search_service.py`: 93.7%*
> - *`categorisation_service.py`: 92.3%*
> - *`alert_service.py`: 91.7%*
> - *`trend_service.py`: 90.9%*
> - *Overall application statement coverage reaches 85.2%, comfortably exceeding our 80% quality gate.*
>
> **Sashi:** *"In `sd683/test/`, my black-box test suite applies Equivalence Partitioning and Boundary Value Analysis on headline lengths and sentiment word counts, while white-box suites guarantee comprehensive branch coverage on sentiment classification logic.*
>
> **Jyothi:** *"In `jb1080/test/`, my symbolic test suite explores the path condition constraints of `calculate_similarity()`, formally proving that token set intersections produce boundaries at exactly theta equals 0.70.*
>
> **Prashanth:** *"And in `pj161/test/` alongside `research/`, our semi-automated concolic harness explores symbolic path conditions and generates concrete test inputs across all four student packages, backed by our DPLL(T) SMT solver."*

---

### Segment 10: Measurement Highlights & Coursework Conclusion
- **Timestamp:** 14:15 – 15:00
- **Presenter:** Nikitha Sarpur (`ns713`)
- **Visual:** Displaying the final slide summarizing COCOMO I & II estimates, PERT Critical Path, EVM indices ($CPI = 1.05, SPI = 1.00$), and CMMI Level 2 compliance.

**Spoken Script:**
> *"To conclude our presentation, our software measurement framework yielded decisive insights:*
> - *Our PERT network identified a 17-activity Critical Path of 41.85 days with a variance of 4.83 days squared, placing project completion on target with a 95% confidence window.*
> - *Our physical codebase comprises 2,741 executable application lines (5,275 total lines with tests). COCOMO I Organic mode estimated 6.74 Person-Months, while COCOMO II Post-Architecture sizing estimated 8.87 Person-Months, validating our 4-member sprint pacing.*
> - *Earned Value Management at Sprint 3 showed a CPI of 1.05 and an SPI of 1.00, demonstrating that our team delivered ahead of schedule and within budgeted effort.*
> - *Finally, our CMMI Level 2 Managed audit achieved 100% compliance across all 7 process areas, supported by our Git feature-branch workflow and peer review gates.*
>
> *Thank you for watching our demonstration of the News Monitoring and Analytics Application."*

---

## 5. Speaker Cue Cards & Emergency Contingency Notes

| Scenario | Contingency Action During Recording |
| :--- | :--- |
| **No Internet Connection** | Feature Option 8's Offline Demo Mode. Highlight that offline synthetic data is identical in structure to live RSS feeds. |
| **Accidental Terminal Resize** | `interface/formatting.py` automatically fits terminal dimensions or uses clean fixed-width 100-column ASCII borders. |
| **Unexpected Keystroke / Cancel** | `interface/input_handler.py` catches `KeyboardInterrupt` and cancellation sentinel `C`, returning safely to the menu without crashing. |
| **Need Fresh Test Data** | Delete files in `data/*.json` and select Option 18 in the menu to reload the pristine 114-article dataset. |

---
*End of Video Demonstration Script — CO7095 News Monitoring and Analytics Application.*
