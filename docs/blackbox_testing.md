# Black-Box Testing Specification and Execution Log
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Specification-Based Black-Box Test Inventory

The black-box test suite exercises the system's public interfaces without inspecting internal control paths. Techniques applied include **Equivalence Partitioning (EP)**, **Boundary Value Analysis (BVA)**, **Decision Table Testing (DTT)**, and **State Transition Testing (STT)**.

---

## 2. Test Execution Log Table

| Test ID | Member | Feature / Module | Test Technique | Preconditions | Input / Stimulus | Expected Output | Actual Output | Result |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-BB-ART-01** | ns713 | Article Model | Valid Partition | Valid model | Headline, source, URL populated | `validate() == (True, [])` | `(True, [])` | **PASS** |
| **TC-BB-ART-02** | ns713 | Article Model | BVA (Empty) | Valid model | Headline = `""` | `validate() == (False, ['Headline cannot be empty.'])` | Matched error string | **PASS** |
| **TC-BB-ART-03** | ns713 | Article Model | BVA (2 chars) | Valid model | Headline = `"AI"` | Validation error (min length 3) | Matched error string | **PASS** |
| **TC-BB-ART-04** | ns713 | Article Model | BVA (3 chars) | Valid model | Headline = `"War"` | `validate() == (True, [])` | `(True, [])` | **PASS** |
| **TC-BB-ART-05** | ns713 | Article Model | EP (Missing Source) | Valid model | `source_name = ""` | Error: Source name cannot be empty | Matched error string | **PASS** |
| **TC-BB-ART-06** | ns713 | Article Model | EP (Missing URL) | Valid model | `article_url = ""` | Error: Article URL cannot be empty | Matched error string | **PASS** |
| **TC-BB-ART-07** | ns713 | Article Model | EP (Invalid Sentiment)| Valid model | `sentiment = "Invalid"` | Error: Invalid sentiment label | Matched error string | **PASS** |
| **TC-BB-ART-08** | ns713 | Article Model | Robustness (Unicode) | Valid model | Headline with accented glyphs & emoji | Preserves characters, returns True | Preserved & valid | **PASS** |
| **TC-BB-ART-09** | ns713 | Article Model | Robustness (10k chars)| Valid model | Body with 10,000+ characters | Handles memory, returns True | Handled & valid | **PASS** |
| **TC-BB-SRC-01** | ns713 | Source Model | Valid Partition | Valid source | Valid HTTPS feed URL | `validate() == (True, [])` | `(True, [])` | **PASS** |
| **TC-BB-SRC-02** | ns713 | Source Model | EP (Empty Name) | Valid source | `name = ""` | Error: Source name cannot be empty | Matched error string | **PASS** |
| **TC-BB-SRC-04** | ns713 | Source Model | Robustness (FTP) | Valid source | `feed_url = "ftp://..."` | Rejects non-http/https/file protocol | Matched error string | **PASS** |
| **TC-BB-RSS-01** | ns713 | RSS Parsing | Specification Match | RssService init | Well-formed RSS 2.0 XML | Extracts 1 article, normalises pubDate | 1 article parsed | **PASS** |
| **TC-BB-RSS-02** | ns713 | RSS Parsing | Fault Injection | RssService init | Corrupted unclosed `<rss>` XML | Returns `False`, error: Malformed XML | Malformed XML caught | **PASS** |
| **TC-BB-RSS-04** | ns713 | RSS Parsing | Missing Tag Fallback | RssService init | `<item>` missing pubDate/description | Generates valid article, fallback date | Article generated | **PASS** |
| **TC-BB-RSS-06** | ns713 | RSS Offline | Demo Fallback | Demo file exists | `load_offline_demo_feed()` | Returns $\ge 100$ synthetic articles | 114 articles returned | **PASS** |
| **TC-BB-SEA-01** | Sd683 | Search Service | Case Insensitivity | 3 articles | Query = `"quantum"` and `"QUANTUM"` | Both queries return identical match | 1 match returned | **PASS** |
| **TC-BB-SEA-02** | Sd683 | Search Service | BVA (Empty Query) | 3 articles | Query = `""` | Returns all 3 articles | 3 articles returned | **PASS** |
| **TC-BB-SEA-03** | Sd683 | Search Service | EP (No Match) | 3 articles | Query = `"NonExistentTerm"` | Returns empty list `[]` | `[]` returned | **PASS** |
| **TC-BB-SEA-05** | Sd683 | Search Service | Category Filter | 3 articles | Category = `"Business"` | Returns 1 matching Business article | 1 match returned | **PASS** |
| **TC-BB-SEA-08** | Sd683 | Search Service | Decision Table | 3 articles | Query="markets", Source="FT", Cat="Business" | Returns exact single conjunction match | 1 match returned | **PASS** |
| **TC-BB-CAT-01** | Sd683 | Categorisation | Domain Partition | Categoriser init | Headline: "Parliament Election Vote" | Classified as `"Politics"` | `"Politics"` assigned | **PASS** |
| **TC-BB-CAT-02** | Sd683 | Categorisation | Domain Partition | Categoriser init | Headline: "Cybersecurity Cloud Patch" | Classified as `"Technology"` | `"Technology"` assigned | **PASS** |
| **TC-BB-CAT-06** | Sd683 | Categorisation | Fallback Partition | Categoriser init | Abstract text with zero domain words | Falls back to `"Other"` | `"Other"` assigned | **PASS** |
| **TC-BB-CAT-08** | Sd683 | Categorisation | Decision Table | Categoriser init | 1 Tech keyword, 3 Business keywords | Resolves to highest count (`Business`) | `"Business"` assigned | **PASS** |
| **TC-BB-SEN-01** | Sd683 | Sentiment | Positive Polarity | Sentiment init | "Massive growth, success, innovation" | Label: `"Positive"`, Score $> 0$ | Positive, score = 3 | **PASS** |
| **TC-BB-SEN-02** | Sd683 | Sentiment | Negative Polarity | Sentiment init | "Severe crisis, bankruptcy, job loss" | Label: `"Negative"`, Score $< 0$ | Negative, score = -3 | **PASS** |
| **TC-BB-SEN-04** | Sd683 | Sentiment | BVA (Balanced Zero)| Sentiment init | "initial success and subsequent failure" | Score $= 0$, Label: `"Neutral"` | Neutral, score = 0 | **PASS** |
| **TC-BB-DUP-01** | Jb1080 | Duplicate Service | Exact URL | Article in repo | Candidate with identical article URL | `is_dup == True`, reason identifies URL | True, URL matched | **PASS** |
| **TC-BB-DUP-02** | Jb1080 | Duplicate Service | Normalised URL | Article in repo | URL with tracking query params (`?utm`) | Flagged as duplicate URL | True, URL matched | **PASS** |
| **TC-BB-DUP-03** | Jb1080 | Duplicate Service | Normalised Headline| Article in repo | Headline differing only in casing/punct | Flagged as duplicate headline | True, headline matched| **PASS** |
| **TC-BB-DUP-04** | Jb1080 | Duplicate Service | Token Fingerprint | Article in repo | Re-ordered words ("Treaty Signed...") | Flagged as fingerprint match | True, fingerprint | **PASS** |
| **TC-BB-DUP-05** | Jb1080 | Duplicate Service | Jaccard Similarity | Article in repo | Near-duplicate headline ($J \ge 0.70$) | Flagged as high similarity duplicate | True, similarity | **PASS** |
| **TC-BB-DUP-06** | Jb1080 | Duplicate Service | Non-Duplicate EP | Article in repo | Completely distinct sporting headline | `is_dup == False`, matched is `None` | False, unique | **PASS** |
| **TC-BB-TRD-01** | Jb1080 | Trend Service | Frequency Ranking | 3 articles | Ingest articles with repeated term | Top keyword has highest count | Quantum count = 4 | **PASS** |
| **TC-BB-TRD-02** | Jb1080 | Trend Service | Stop-Word Exclusion | 3 articles | Ingest text with "the", "and", "in" | Stop words absent from top trends | Stop words filtered | **PASS** |
| **TC-BB-SRCAN-01**| Jb1080 | Source Analytics | Count Verification | 5 articles | Articles from BBC and Reuters | Accurate count per source | BBC: 3, Reuters: 2 | **PASS** |
| **TC-BB-SRCAN-02**| Jb1080 | Source Analytics | Distribution Check | 5 articles | Articles from BBC and Reuters | Percentage shares sum to 100.0% | Sum = 100.0% | **PASS** |
| **TC-BB-ALT-01** | Pj161 | Alert Rules | Valid Partition | AlertService init | Keyword = `"climate"`, Cat = `"Environment"` | Rule registered and active | Registered | **PASS** |
| **TC-BB-ALT-02** | Pj161 | Alert Rules | BVA (Empty) | AlertService init | Keyword = `""` | Fails validation (keyword empty) | Validation error | **PASS** |
| **TC-BB-ALT-04** | Pj161 | Alert Monitoring | Trigger Matching | Active rule | Ingest article containing `"cybersecurity"` | Alert generated with status `"UNREAD"` | Alert generated | **PASS** |
| **TC-BB-ALT-05** | Pj161 | Alert Monitoring | Decision Table | Rule for Envir | Ingest Tech article containing keyword | No alert created (category mismatch) | 0 alerts created | **PASS** |
| **TC-BB-ALT-06** | Pj161 | Alert Management | State Transition | Unread alert | Call `mark_alert_read(alert_id)` | Transition from UNREAD to READ | State updated to READ | **PASS** |
| **TC-BB-ALT-07** | Pj161 | Alert Monitoring | Duplicate Guard | Active alert | Re-ingest identical matching article | Duplicate alert suppressed | 0 duplicate alerts | **PASS** |
| **TC-BB-REP-01** | Pj161 | Reporting Service| RFC 4180 CSV | 1 article | Call `export_articles_csv()` | CSV written with correct 8-column header| Header verified | **PASS** |
| **TC-BB-DSH-01** | Pj161 | Dashboard | BVA (Empty State) | Fresh repo | Call `get_dashboard_metrics()` | Returns 0 for all counters safely | Zero counters | **PASS** |
| **TC-BB-DSH-02** | Pj161 | Dashboard | Populated State | 1 article, 1 rule | Call `get_dashboard_metrics()` | Displays 1 article, 1 alert, unread = 1 | Counters verified | **PASS** |
