# Agile User Stories Specification (36 Detailed Stories)
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## Story Allocation Matrix Overview

Across 3 sprints of 1–2 weeks each, the team of 4 members completes a balanced workload:
- **4 Members × 3 Stories/Sprint × 3 Sprints = Exactly 36 User Stories**
- **Sprint 1 (US01 – US12)**: Application Backbone, Core Models, Manual Entry, Search Foundation, Source Counting, Rules & Persistence.
- **Sprint 2 (US13 – US24)**: Automated RSS Collection, Normalisation, Rule-based Categorisation & Sentiment, Duplicate Similarity, Trending Topics, Alert Triggering, CSV Reporting.
- **Sprint 3 (US25 – US36)**: Data Integrity, Resilient Ingestion, Offline Demonstration, Edge Cases, Multi-filter Integration, Temporal Analytics, Trend Shifts, Complete Dashboard & Usability.

---

# SPRINT 1 – Application Backbone and News Collection

### Member 1: Nikitha Sarpur (ns713 - 259060190)

#### US01 – News Article Model
- **User Story**: *As a user, I want news articles to have a standard structure so that article information can be consistently managed.*
- **Acceptance Criteria**:
  - `NewsArticle` contains `article_id`, `headline`, `description`, `content`, `source_name`, `source_url`, `article_url`, `publication_date`, `category`, `sentiment`, `sentiment_score`, `keywords`, `created_timestamp`.
  - Automatically generates unique identifier prefixed with `ART-`.
  - Serializes to dictionary via `to_dict()` and reconstructs via `from_dict()`.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `models/article.py`
- **Dependencies**: None
- **Black-Box Testing**: Validate article instantiation with valid fields, boundary check on 2-char vs 3-char headlines, and missing URL rejection.
- **White-Box Testing**: Statement and condition coverage of `NewsArticle.validate()`, `to_dict()`, and `full_text()`.
- **Symbolic/Concolic Relevance**: Evaluates symbolic constraints on string lengths and sentiment enum partitions.
- **GitHub Issue**: `[US01] Implement standardized NewsArticle domain model`
- **Branch**: `feature/US01-news-article-model`
- **Definition of Done**: Model passes all unit tests, enforces field validation, and integrates into persistence.

#### US02 – Manual News Entry
- **User Story**: *As a user, I want to add news articles manually so that I can maintain articles without RSS feeds.*
- **Acceptance Criteria**:
  - User can supply headline, source, URL, description, content, and date through CLI or API.
  - Automatically validates required fields (headline >= 3 chars, source non-empty).
  - Persists new record to `articles.json`.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/news_service.py`, `interface/menu.py`
- **Dependencies**: US01, US12
- **Black-Box Testing**: Add valid article; attempt adding article with empty headline; check rejection message.
- **White-Box Testing**: Branch coverage of `NewsService.add_article()` validation failure vs success paths.
- **Symbolic/Concolic Relevance**: Validates input parameter validation paths.
- **GitHub Issue**: `[US02] Implement manual news article addition and validation`
- **Branch**: `feature/US02-manual-news-entry`
- **Definition of Done**: Article is persisted, validated, and viewable in article list.

#### US03 – News Source Management
- **User Story**: *As a user, I want to register and manage news sources so that articles can be associated with their original source.*
- **Acceptance Criteria**:
  - `NewsSource` model holds `source_id`, `name`, `feed_url`, `url`, `category`, `enabled`, and `article_count`.
  - Verifies feed URL protocol (`http://`, `https://`, or `file://`).
  - Supports adding, viewing, and deleting sources.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `models/news_source.py`, `services/news_service.py`
- **Dependencies**: None
- **Black-Box Testing**: Register valid source; reject invalid protocol (`ftp://`); delete source by ID.
- **White-Box Testing**: Branch coverage in `NewsSource.validate()` and `NewsService.add_source()`.
- **Symbolic/Concolic Relevance**: Symbolic analysis of URL protocol prefix constraints.
- **GitHub Issue**: `[US03] Implement news source registry and validation`
- **Branch**: `feature/US03-news-source-management`
- **Definition of Done**: Sources persist to `sources.json` and appear in source management menu.

---

### Member 2: Sashi Dommaraju (Sd683 - 259062044)

#### US04 – Headline and Keyword Search
- **User Story**: *As a user, I want to search news headlines and content so that I can find relevant articles quickly.*
- **Acceptance Criteria**:
  - Case-insensitive substring searching across headlines and content.
  - Returns matching article list; returns empty list without error on no match.
  - Empty search query returns all articles.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/search_service.py`
- **Dependencies**: US01
- **Black-Box Testing**: Search for uppercase, lowercase, and mixed-case term; search non-existent string.
- **White-Box Testing**: Branch coverage in `SearchService.search_headline()` and `search_content()`.
- **Symbolic/Concolic Relevance**: Explores string substring matching conditions.
- **GitHub Issue**: `[US04] Implement headline and keyword text search`
- **Branch**: `feature/US04-news-search`
- **Definition of Done**: Search function passes unit tests and integrates with CLI search menu.

#### US05 – Source and Date Filtering
- **User Story**: *As a user, I want to filter articles by source and date so that I can narrow search results.*
- **Acceptance Criteria**:
  - Filters articles published by a specific news outlet name.
  - Filters articles published between `start_date` and `end_date` (inclusive).
  - Handles missing or malformed dates gracefully without crashing.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/search_service.py`, `services/time_analytics_service.py`
- **Dependencies**: US01
- **Black-Box Testing**: Filter by known source; filter by date window covering 1, many, and zero articles.
- **White-Box Testing**: Branch coverage in `filter_by_source()` and `filter_by_date_range()`.
- **Symbolic/Concolic Relevance**: Evaluates date inequality interval constraints.
- **GitHub Issue**: `[US05] Implement source and date filtering`
- **Branch**: `feature/US05-source-date-filter`
- **Definition of Done**: Filters return accurate subsets and handle edge-case dates.

#### US06 – Initial News Categorisation
- **User Story**: *As a user, I want news to be categorised so that articles can be organised by subject.*
- **Acceptance Criteria**:
  - Matches article text against keyword dictionaries for 10 domain categories.
  - Assigns category with the most keyword matches; falls back to "Other".
  - Strictly deterministic rule-based matching; no machine learning claims.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 1 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `services/categorisation_service.py`, `config/category_keywords.json`
- **Dependencies**: US01
- **Black-Box Testing**: Article with "election" categorised as Politics; article with no keywords categorised as Other.
- **White-Box Testing**: Loop testing over category dictionaries and max score resolution.
- **Symbolic/Concolic Relevance**: Concolic path inversion between category keywords and fallback path.
- **GitHub Issue**: `[US06] Implement rule-based keyword categorisation engine`
- **Branch**: `feature/US06-news-categorisation`
- **Definition of Done**: Keyword dictionaries loaded from JSON and accurately tag incoming articles.

---

### Member 3: Jyothi Bandalapati (Jb1080 - 259060742)

#### US07 – Trending Analytics Foundation
- **User Story**: *As a user, I want the system to count keywords so that I can identify frequently discussed topics.*
- **Acceptance Criteria**:
  - Tokenizes headlines and content, converts to lower-case, and strips punctuation.
  - Filters out English stop words loaded from `config/stop_words.json`.
  - Returns frequency distribution sorted descending.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/trend_service.py`, `config/stop_words.json`
- **Dependencies**: US01
- **Black-Box Testing**: Count frequencies across sample articles; ensure stop words like "the" are excluded.
- **White-Box Testing**: Branch coverage of `extract_keywords()` for numbers and token length filtering.
- **Symbolic/Concolic Relevance**: Concolic evaluation of token inclusion predicates (`len >= 3`, `not in stop_words`).
- **GitHub Issue**: `[US07] Implement keyword frequency counting and stop-word filtering`
- **Branch**: `feature/US07-trending-foundation`
- **Definition of Done**: Frequencies calculate accurately on test strings and collections.

#### US08 – URL Duplicate Detection
- **User Story**: *As a user, I want duplicate URLs detected so that repeated articles are not stored unnecessarily.*
- **Acceptance Criteria**:
  - Compares candidate article URL against existing articles.
  - Normalises URLs by ignoring protocol (`http` vs `https`), `www`, trailing slashes, and tracking query params.
  - Flags duplicate and prevents redundant insertion.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/duplicate_service.py`
- **Dependencies**: US01
- **Black-Box Testing**: Add article with same URL; add article with query string appended (`?ref=tw`); confirm match.
- **White-Box Testing**: Branch coverage of `DuplicateService.normalise_url()` and `check_duplicate()` URL path.
- **Symbolic/Concolic Relevance**: Symbolic analysis of URL normalization regular expressions.
- **GitHub Issue**: `[US08] Implement URL duplicate detection and normalisation`
- **Branch**: `feature/US08-url-duplicate-detection`
- **Definition of Done**: Prevents redundant storage of identical article URLs.

#### US09 – Source Article Counts
- **User Story**: *As a user, I want article counts grouped by source so that I can compare news-source activity.*
- **Acceptance Criteria**:
  - Calculates total articles published per registered news source.
  - Calculates percentage share of total repository volume.
  - Clearly notes in output that volume measures activity, not factual accuracy or credibility.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/source_analytics_service.py`
- **Dependencies**: US01, US03
- **Black-Box Testing**: Test with 3 sources having known counts; verify percentage sums to 100%.
- **White-Box Testing**: Statement coverage in `SourceAnalyticsService.get_source_counts()`.
- **Symbolic/Concolic Relevance**: Mathematical constraint validation for percentage sum.
- **GitHub Issue**: `[US09] Implement news source article count and volume distribution`
- **Branch**: `feature/US09-source-article-counts`
- **Definition of Done**: Returns dictionary and distribution list; disclaimers documented.

---

### Member 4: Jalakam Prashanth (Pj161 - 259060676)

#### US10 – Keyword Monitoring Rules
- **User Story**: *As a user, I want to create keyword monitoring rules so that I can track topics of interest.*
- **Acceptance Criteria**:
  - `AlertRule` model contains `rule_id`, `keyword`, `description`, `category_filter`, `enabled`, and `created_at`.
  - Allows adding, toggling enabled/disabled status, and deleting rules.
  - Persists rules to `alert_rules.json`.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `models/alert_rule.py`, `services/alert_service.py`
- **Dependencies**: None
- **Black-Box Testing**: Add valid rule; reject empty keyword; toggle rule status and verify change.
- **White-Box Testing**: Branch coverage in `AlertRule.validate()` and `AlertService.toggle_rule()`.
- **Symbolic/Concolic Relevance**: Symbolic evaluation of keyword match boolean algebra.
- **GitHub Issue**: `[US10] Implement keyword monitoring rules and persistence`
- **Branch**: `feature/US10-keyword-monitoring-rules`
- **Definition of Done**: Rules are stored, managed, and retrieved reliably.

#### US11 – CLI Dashboard Backbone
- **User Story**: *As a user, I want a main dashboard so that I can navigate the application's functions.*
- **Acceptance Criteria**:
  - Numbered interactive terminal menu with options for all core features.
  - Formatted dashboard rendering high-level metrics (article count, sources, active rules, alerts).
  - Clean error trapping for invalid inputs.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 1 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `interface/menu.py`, `interface/formatting.py`, `services/dashboard_service.py`
- **Dependencies**: US01, US03, US10
- **Black-Box Testing**: Launch menu; select option 1; enter invalid input and verify graceful warning.
- **White-Box Testing**: Statement coverage of `DashboardService.get_dashboard_metrics()`.
- **Symbolic/Concolic Relevance**: State machine transition validation for menu routing.
- **GitHub Issue**: `[US11] Build interactive CLI dashboard and menu navigation`
- **Branch**: `feature/US11-cli-dashboard-backbone`
- **Definition of Done**: Main menu executes and displays aggregated metrics correctly.

#### US12 – JSON Storage and Reporting Foundation
- **User Story**: *As a user, I want information saved persistently so that I can access it after restarting the application.*
- **Acceptance Criteria**:
  - `JsonStorage` provides atomic write operations using temporary files and `os.replace`.
  - Creates `.bak` backups before modifying files.
  - Automatically handles missing files by returning default empty structures.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 1 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `storage/json_storage.py`
- **Dependencies**: None
- **Black-Box Testing**: Save and reload list; read non-existent file returning default; verify backup file creation.
- **White-Box Testing**: Branch coverage of `load_data()` with missing file, empty file, and corrupt JSON.
- **Symbolic/Concolic Relevance**: Exception path testing on file system I/O failure.
- **GitHub Issue**: `[US12] Implement robust atomic JSON storage and backup manager`
- **Branch**: `feature/US12-json-storage-foundation`
- **Definition of Done**: Atomic save and safe load verified under crash and corruption scenarios.

---

# SPRINT 2 – Monitoring and Analytics

### Member 1: Nikitha Sarpur (ns713 - 259060190)

#### US13 – RSS Feed Collection
- **User Story**: *As a user, I want the system to collect news from RSS feeds so that article collection can be automated.*
- **Acceptance Criteria**:
  - Fetches XML data from registered RSS feed URLs using `urllib.request`.
  - Sets appropriate `User-Agent` headers and timeout threshold.
  - Network timeout or HTTP error in one feed does not crash application or halt other feeds.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 2 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `services/rss_service.py`
- **Dependencies**: US03
- **Black-Box Testing**: Ingest valid feed; test with invalid URL; test with local `file://` feed.
- **White-Box Testing**: Branch coverage of `fetch_feed_xml()` HTTPError, URLError, and Timeout handling.
- **Symbolic/Concolic Relevance**: Network status code constraint analysis.
- **GitHub Issue**: `[US13] Implement safe RSS XML feed collection service`
- **Branch**: `feature/US13-rss-feed-collection`
- **Definition of Done**: Feeds download reliably with complete error logging.

#### US14 – RSS Parsing and Normalisation
- **User Story**: *As a user, I want feed data converted into standard articles so that different feeds are handled consistently.*
- **Acceptance Criteria**:
  - Parses XML with standard library `xml.etree.ElementTree`.
  - Extracts title, link, description, and publication date.
  - Normalises RFC 822 / RSS dates to ISO `YYYY-MM-DD`.
  - Strips HTML tags from description and summary fields.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 2 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `services/rss_service.py`
- **Dependencies**: US01, US13
- **Black-Box Testing**: Parse standard RSS 2.0 item; parse Atom `<entry>`; verify ISO date conversion.
- **White-Box Testing**: Branch coverage in `parse_rss_xml()`, `parse_pub_date()`, and `clean_html()`.
- **Symbolic/Concolic Relevance**: Concolic exploration of XML element presence and date parsing branches.
- **GitHub Issue**: `[US14] Implement RSS XML parsing and article normalisation`
- **Branch**: `feature/US14-rss-parsing-normalisation`
- **Definition of Done**: Feed items convert into populated `NewsArticle` objects.

#### US15 – Duplicate and Import Error Handling
- **User Story**: *As a user, I want invalid and duplicate feed items handled so that importing news remains reliable.*
- **Acceptance Criteria**:
  - Batch import filters out malformed items and items missing required headlines.
  - Evaluates candidate feed items against existing articles to prevent duplicate ingestion.
  - Reports statistics: total processed, added, duplicates skipped, invalid skipped.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/news_service.py`, `services/duplicate_service.py`
- **Dependencies**: US08, US14
- **Black-Box Testing**: Ingest feed twice; second run must report 0 added and all duplicates skipped.
- **White-Box Testing**: Branch testing of `import_articles_batch()` duplicate and validation branches.
- **Symbolic/Concolic Relevance**: Path analysis of batch ingestion control flow.
- **GitHub Issue**: `[US15] Implement duplicate filtering and error tracking in batch import`
- **Branch**: `feature/US15-import-error-handling`
- **Definition of Done**: Re-ingesting existing feeds causes zero duplicate records.

---

### Member 2: Sashi Dommaraju (Sd683 - 259062044)

#### US16 – Sentiment Analysis
- **User Story**: *As a user, I want news sentiment classified so that I can understand general tone.*
- **Acceptance Criteria**:
  - Tokenizes text and counts matches against positive and negative word dictionaries.
  - Calculates `score = positive_matches - negative_matches`.
  - Classifies: Score > 0 -> Positive, Score < 0 -> Negative, Score == 0 -> Neutral.
  - Identifies specific lexical words contributing to score.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 2 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `services/sentiment_service.py`, `config/positive_words.json`, `config/negative_words.json`
- **Dependencies**: US01
- **Black-Box Testing**: Score positive sentence; score negative sentence; score balanced sentence (score 0).
- **White-Box Testing**: Branch coverage of `classify_score()` and `analyse_text()`.
- **Symbolic/Concolic Relevance**: Symbolic execution of score function $S = P - N$ and boundary inputs.
- **GitHub Issue**: `[US16] Implement rule-based lexical sentiment analysis`
- **Branch**: `feature/US16-sentiment-analysis`
- **Definition of Done**: Classifies articles deterministically and documents limitations (sarcasm, negation).

#### US17 – Configurable Category Rules
- **User Story**: *As a user, I want configurable categorisation keywords so that categories can be maintained.*
- **Acceptance Criteria**:
  - Category keyword dictionaries loaded from `config/category_keywords.json`.
  - Allows inspecting configured keywords per category through service and CLI.
  - Supports updating and persisting keywords for existing categories.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/categorisation_service.py`, `config/category_keywords.json`
- **Dependencies**: US06
- **Black-Box Testing**: View keywords for "Science"; add keyword to category; verify persistence.
- **White-Box Testing**: Branch coverage in `update_keywords()` and `get_keywords_for_category()`.
- **Symbolic/Concolic Relevance**: Set membership constraint validation.
- **GitHub Issue**: `[US17] Implement category configuration and keyword dictionary management`
- **Branch**: `feature/US17-configurable-category-rules`
- **Definition of Done**: Changes persist to JSON configuration and affect subsequent classifications.

#### US18 – Advanced News Filters
- **User Story**: *As a user, I want combined filters so that I can locate news using multiple conditions.*
- **Acceptance Criteria**:
  - Conjunction filter supporting simultaneous query, source, category, sentiment, and date limits.
  - Omitting a filter applies no restriction for that dimension.
  - Returns intersection of all applied filter criteria.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/search_service.py`
- **Dependencies**: US04, US05, US06, US16
- **Black-Box Testing**: Filter simultaneously by category="Technology" AND sentiment="Positive" AND source="Reuters".
- **White-Box Testing**: Condition coverage across all 5 optional parameters in `combined_filter()`.
- **Symbolic/Concolic Relevance**: Multi-variable boolean conjunction constraint solving.
- **GitHub Issue**: `[US18] Implement combined multi-criteria news filtering`
- **Branch**: `feature/US18-advanced-news-filters`
- **Definition of Done**: Combined filter executes in CLI and passes multi-criteria tests.

---

### Member 3: Jyothi Bandalapati (Jb1080 - 259060742)

#### US19 – Trending Topic Frequency
- **User Story**: *As a user, I want trending keywords calculated so that I can identify popular news topics.*
- **Acceptance Criteria**:
  - Calculates top 10 and top 25 trending keywords across repository.
  - Allows date-specific trend extraction for articles published on a given date.
  - Excludes numbers and words under 3 characters.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/trend_service.py`
- **Dependencies**: US07
- **Black-Box Testing**: Ingest articles with repeated term "quantum"; verify "quantum" is top ranked.
- **White-Box Testing**: Loop and condition coverage in `get_keyword_frequencies()` and `get_trending_by_date()`.
- **Symbolic/Concolic Relevance**: Symbolic analysis of token frequency counters.
- **GitHub Issue**: `[US19] Implement trending topics and top-N keyword frequency analytics`
- **Branch**: `feature/US19-trending-topic-frequency`
- **Definition of Done**: Trending topics display in dashboard and CLI menu.

#### US20 – Duplicate Similarity Report
- **User Story**: *As a user, I want likely duplicate headlines identified so that repeated news coverage can be analysed.*
- **Acceptance Criteria**:
  - Computes Jaccard similarity over non-stop headline token sets.
  - Flags headline pairs exceeding similarity threshold ($\theta \ge 0.70$).
  - Explains reason for flagging (exact URL, normalised headline, fingerprint, similarity).
  - Generates list of duplicate pairs across repository.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/duplicate_service.py`
- **Dependencies**: US08
- **Black-Box Testing**: Provide headlines with 80% word overlap; confirm flagged with similarity score.
- **White-Box Testing**: Branch coverage in `calculate_similarity()` and `find_all_duplicates()`.
- **Symbolic/Concolic Relevance**: Symbolic boundary constraint solving for Jaccard index $\theta = 0.70$.
- **GitHub Issue**: `[US20] Implement headline similarity matching and duplicate reporting`
- **Branch**: `feature/US20-duplicate-similarity-report`
- **Definition of Done**: Identifies near-duplicate headlines and outputs detailed comparison report.

#### US21 – Source Sentiment Analytics
- **User Story**: *As a user, I want sentiment grouped by source so that I can compare the tone of articles published by different sources.*
- **Acceptance Criteria**:
  - Computes positive, negative, and neutral article counts for each source.
  - Calculates percentage breakdown per source.
  - Documents that metrics reflect collection tone rather than media bias or factual truth.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/source_analytics_service.py`
- **Dependencies**: US09, US16
- **Black-Box Testing**: Compute source sentiment on sample with known positive/negative distribution per source.
- **White-Box Testing**: Loop and calculation coverage in `get_sentiment_distribution_by_source()`.
- **Symbolic/Concolic Relevance**: Grouping and aggregation arithmetic validation.
- **GitHub Issue**: `[US21] Implement source sentiment profiling and distribution analytics`
- **Branch**: `feature/US21-source-sentiment-analytics`
- **Definition of Done**: Source tone profiles render in CLI and include required analytical disclaimer.

---

### Member 4: Jalakam Prashanth (Pj161 - 259060676)

#### US22 – Keyword Alerts
- **User Story**: *As a user, I want alerts generated when monitored keywords appear so that I can identify relevant news.*
- **Acceptance Criteria**:
  - Scans newly added or collected articles against all enabled monitoring rules.
  - Creates `Alert` record containing `alert_id`, `rule_id`, `keyword`, `article_id`, `headline`, and timestamp.
  - Prevents generating repeated duplicate alerts for the same article and rule.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 2 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `services/alert_service.py`, `models/alert.py`
- **Dependencies**: US10
- **Black-Box Testing**: Add rule for "climate"; ingest climate article; verify alert is created; ingest again; verify no duplicate alert.
- **White-Box Testing**: Branch coverage in `AlertService.process_article()` duplicate alert check.
- **Symbolic/Concolic Relevance**: Symbolic path condition solving for alert trigger predicates.
- **GitHub Issue**: `[US22] Implement automated keyword alert generation engine`
- **Branch**: `feature/US22-keyword-alerts`
- **Definition of Done**: Alerts are created, persisted, and viewable in alert views.

#### US23 – Alert Management
- **User Story**: *As a user, I want to view and manage alerts so that I can track important news notifications.*
- **Acceptance Criteria**:
  - Displays list of alerts showing keyword, article headline, date, and status.
  - Allows marking specific alert as READ.
  - Supports marking all unread alerts as READ in one operation.
  - Persists status changes to `alerts.json`.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/alert_service.py`, `models/alert.py`
- **Dependencies**: US22
- **Black-Box Testing**: Mark single alert read; verify unread count decrements; mark all read.
- **White-Box Testing**: State transition testing in `mark_alert_read()` and `mark_all_alerts_read()`.
- **Symbolic/Concolic Relevance**: Finite state machine verification (UNREAD -> READ).
- **GitHub Issue**: `[US23] Implement alert queue management and read status tracking`
- **Branch**: `feature/US23-alert-management`
- **Definition of Done**: Users can inspect and acknowledge alerts in CLI.

#### US24 – Analytics CSV Reports
- **User Story**: *As a user, I want analytics exported to CSV so that I can use the results outside the application.*
- **Acceptance Criteria**:
  - Exports articles, category distribution, source analytics, trending topics, and alerts to CSV.
  - Adheres strictly to RFC 4180 with standard library `csv` module.
  - Writes files to `reports/generated/` directory.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 2 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/report_service.py`
- **Dependencies**: US01, US19, US21, US22
- **Black-Box Testing**: Export all CSVs; inspect headers and row count matching repository counts.
- **White-Box Testing**: Statement coverage across all export functions in `ReportService`.
- **Symbolic/Concolic Relevance**: Concolic verification of field delimiter and quotation escaping.
- **GitHub Issue**: `[US24] Implement CSV analytics and report export service`
- **Branch**: `feature/US24-analytics-csv-reports`
- **Definition of Done**: Generates valid CSV files readable by standard spreadsheet tools.

---

# SPRINT 3 – Integration, Reporting, and Quality

### Member 1: Nikitha Sarpur (ns713 - 259060190)

#### US25 – Data Integrity Validation
- **User Story**: *As a user, I want news data validated so that incomplete or invalid articles do not affect the system.*
- **Acceptance Criteria**:
  - Rejects articles with empty headlines or headlines shorter than 3 characters.
  - Rejects articles with missing sources or missing URLs.
  - Rejects invalid sentiment strings not matching Positive, Negative, or Neutral.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `models/article.py`, `services/news_service.py`
- **Dependencies**: US01, US02
- **Black-Box Testing**: Equivalence partitioning and boundary value testing across all article attributes.
- **White-Box Testing**: Full branch coverage of `NewsArticle.validate()`.
- **Symbolic/Concolic Relevance**: Programmatic symbolic execution tree verifying all validation paths.
- **GitHub Issue**: `[US25] Implement rigorous data integrity and field validation`
- **Branch**: `feature/US25-data-integrity-validation`
- **Definition of Done**: 100% of validation paths tested and documented.

#### US26 – Resilient RSS Collection
- **User Story**: *As a user, I want RSS failures handled safely so that other feeds can continue to be processed.*
- **Acceptance Criteria**:
  - Malformed XML in one feed logged without halting collection batch.
  - HTTP 404, 500, or DNS resolution failures handled gracefully with descriptive warnings.
  - Timeout threshold prevents process hanging on unresponsive remote hosts.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/rss_service.py`
- **Dependencies**: US13, US14
- **Black-Box Testing**: Supply list with 1 good feed and 2 broken feeds; verify good feed is ingested.
- **White-Box Testing**: Exception branch coverage for URLError, HTTPError, and ParseError.
- **Symbolic/Concolic Relevance**: Concolic fault-injection for corrupt XML structures.
- **GitHub Issue**: `[US26] Enhance RSS collection resilience and fault isolation`
- **Branch**: `feature/US26-resilient-rss-collection`
- **Definition of Done**: Tested with malformed and timing-out feeds with zero crashes.

#### US27 – Offline Demonstration Dataset
- **User Story**: *As a user, I want demonstration news available offline so that I can use the system without internet access.*
- **Acceptance Criteria**:
  - Provides realistic offline dataset containing >= 100 curated news articles in `dataset/demo_news.json`.
  - Spans all 10 categories, positive/negative/neutral tones, multiple sources, and dates.
  - Includes explicit duplicate examples for testing duplicate detection.
  - Prominently labeled as synthetic demonstration data.
- **Assigned Member**: Nikitha Sarpur (ns713) | **Sprint**: 3 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `dataset/demo_news.json`, `services/news_service.py`
- **Dependencies**: US01, US12
- **Black-Box Testing**: Load demo dataset into fresh storage; verify 100+ articles added.
- **White-Box Testing**: Statement coverage of `NewsService.load_demo_data()`.
- **Symbolic/Concolic Relevance**: Verification of schema validity for synthetic dataset.
- **GitHub Issue**: `[US27] Create comprehensive offline synthetic demonstration dataset`
- **Branch**: `feature/US27-offline-demo-dataset`
- **Definition of Done**: Demo dataset loads completely offline without internet connection.

---

### Member 2: Sashi Dommaraju (Sd683 - 259062044)

#### US28 – Sentiment and Categorisation Edge Cases
- **User Story**: *As a user, I want ambiguous and empty text handled safely so that analysis results are reliable.*
- **Acceptance Criteria**:
  - Empty strings, punctuation-only strings, and whitespace return Neutral sentiment score 0.
  - Multi-topic ambiguous articles resolve to highest scoring category or "Other" on tie.
  - Sarcasm, negation, and domain limitations documented in module specifications.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/sentiment_service.py`, `services/categorisation_service.py`
- **Dependencies**: US06, US16
- **Black-Box Testing**: Test empty strings, punctuation strings, and equally balanced positive/negative text.
- **White-Box Testing**: Condition coverage on score calculations and tie-breaking logic.
- **Symbolic/Concolic Relevance**: Symbolic constraint solving for boundary condition $P = N$.
- **GitHub Issue**: `[US28] Address sentiment and categorisation boundary edge cases`
- **Branch**: `feature/US28-sentiment-categorisation-edge-cases`
- **Definition of Done**: Edge cases handled deterministically with zero unhandled exceptions.

#### US29 – Combined Search and Filter Integration
- **User Story**: *As a user, I want combined search filters to work together so that results match my criteria.*
- **Acceptance Criteria**:
  - Interactive multi-filter menu allowing users to specify query, source, category, sentiment, and date boundaries.
  - Outputs matching articles in aligned table.
  - Displays count of matching items.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/search_service.py`, `interface/menu.py`
- **Dependencies**: US18
- **Black-Box Testing**: Search query "quantum" constrained by category="Science" and sentiment="Positive".
- **White-Box Testing**: Branch coverage of `MainMenu.filter_news()` execution flow.
- **Symbolic/Concolic Relevance**: Conjunction constraint satisfaction verification.
- **GitHub Issue**: `[US29] Integrate combined search and filter into interactive CLI`
- **Branch**: `feature/US29-search-filter-integration`
- **Definition of Done**: CLI filter menu operates seamlessly on active article repository.

#### US30 – Analytics Validation
- **User Story**: *As a user, I want analytical results checked against known sample data so that results are trustworthy.*
- **Acceptance Criteria**:
  - Verified test fixtures compare computed sentiment scores and categorisation against known ground truth.
  - Validates that source percentages sum to exactly 100%.
  - Disclaims all machine learning claims; documents rule-based deterministic nature.
- **Assigned Member**: Sashi Dommaraju (Sd683) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: Low
- **Related Modules**: `sd683/test/`
- **Dependencies**: US06, US16, US21
- **Black-Box Testing**: Execute verification test suite against curated ground truth fixtures.
- **White-Box Testing**: Assertion verification across mathematical calculations.
- **Symbolic/Concolic Relevance**: Proof of determinism under identical inputs.
- **GitHub Issue**: `[US30] Validate analytical algorithms against ground truth test suites`
- **Branch**: `feature/US30-analytics-validation`
- **Definition of Done**: Validation tests pass and are documented in test execution reports.

---

### Member 3: Jyothi Bandalapati (Jb1080 - 259060742)

#### US31 – Time-Based Analytics
- **User Story**: *As a user, I want daily, weekly, and monthly analytics so that I can monitor news changes over time.*
- **Acceptance Criteria**:
  - Aggregates article counts by day (`YYYY-MM-DD`), week (`YYYY-Www`), and month (`YYYY-MM`).
  - Tracks sentiment evolution across time buckets.
  - Safely groups unparseable or missing dates into "Unknown Date" bucket without failing.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 3 | **Story Points**: 5 | **Priority**: High
- **Related Modules**: `services/time_analytics_service.py`
- **Dependencies**: US01, US16
- **Black-Box Testing**: Group articles spanning 3 months; verify monthly, weekly, and daily distributions.
- **White-Box Testing**: Statement and branch coverage in `TimeAnalyticsService` grouping methods.
- **Symbolic/Concolic Relevance**: Temporal partitioning constraint analysis.
- **GitHub Issue**: `[US31] Implement daily, weekly, and monthly temporal analytics`
- **Branch**: `feature/US31-time-based-analytics`
- **Definition of Done**: Temporal statistics display in CLI and export to CSV.

#### US32 – Trend Comparisons
- **User Story**: *As a user, I want to compare trending topics across different periods so that topic changes can be analysed.*
- **Acceptance Criteria**:
  - Compares keyword frequency between two article sets or date windows.
  - Computes change in keyword frequency ($\Delta = \text{Count}_2 - \text{Count}_1$).
  - Sorts topics by absolute change magnitude to highlight emerging and declining terms.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/trend_service.py`
- **Dependencies**: US19, US31
- **Black-Box Testing**: Compare period 1 vs period 2; verify correct calculation of positive and negative deltas.
- **White-Box Testing**: Branch coverage of `compare_trends()` with disjoint and overlapping vocabularies.
- **Symbolic/Concolic Relevance**: Differential frequency arithmetic validation.
- **GitHub Issue**: `[US32] Implement multi-period trend comparison and velocity tracking`
- **Branch**: `feature/US32-trend-comparisons`
- **Definition of Done**: Period trend shifts compute accurately and display in CLI.

#### US33 – Duplicate and Source Reporting
- **User Story**: *As a user, I want integrated duplicate and source reports so that news coverage can be evaluated.*
- **Acceptance Criteria**:
  - Displays duplicate detection pairs with matched headlines, sources, reason, and similarity percentage.
  - Displays source analytics breakdown including category share and sentiment proportions.
  - Exports duplicate pairs to `duplicates_report.csv`.
- **Assigned Member**: Jyothi Bandalapati (Jb1080) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: Medium
- **Related Modules**: `services/duplicate_service.py`, `services/source_analytics_service.py`, `services/report_service.py`
- **Dependencies**: US20, US21, US24
- **Black-Box Testing**: Scan repository with intentional duplicates; verify report highlights pairs and exports CSV.
- **White-Box Testing**: Branch coverage in `DuplicateService.find_all_duplicates()`.
- **Symbolic/Concolic Relevance**: Set union and intersection verification.
- **GitHub Issue**: `[US33] Implement integrated duplicate detection and source profiling reports`
- **Branch**: `feature/US33-duplicate-source-reporting`
- **Definition of Done**: Reports render cleanly in CLI and export to CSV.

---

### Member 4: Jalakam Prashanth (Pj161 - 259060676)

#### US34 – Alert and Dashboard Integration
- **User Story**: *As a user, I want keyword alerts displayed in the dashboard so that monitored news is easy to access.*
- **Acceptance Criteria**:
  - Dashboard prominently displays total alerts and count of unread alerts.
  - Visual status indicator highlights when unread notifications are pending.
  - Direct menu access to review and acknowledge alerts.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `services/dashboard_service.py`, `interface/menu.py`
- **Dependencies**: US11, US22, US23
- **Black-Box Testing**: Trigger 2 alerts; open dashboard; verify unread alert count reflects 2.
- **White-Box Testing**: Statement coverage in `DashboardService` alert metric aggregation.
- **Symbolic/Concolic Relevance**: State indicator validation.
- **GitHub Issue**: `[US34] Integrate keyword alerts into executive dashboard`
- **Branch**: `feature/US34-alert-dashboard-integration`
- **Definition of Done**: Unread alerts are surfaced prominently on dashboard landing.

#### US35 – Integrated Reporting and Export
- **User Story**: *As a user, I want complete analytics reports and CSV exports so that findings can be reviewed.*
- **Acceptance Criteria**:
  - Consolidated system report prints overview of articles, categories, sources, trends, and alerts.
  - Option 17 exports 7 distinct CSV datasets to `reports/generated/`:
    `articles_report.csv`, `category_distribution.csv`, `source_analytics.csv`,
    `trending_topics.csv`, `alerts_report.csv`, `duplicates_report.csv`, `time_trends.csv`.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 3 | **Story Points**: 5 | **Priority**: High
- **Dependencies**: US13, US21, US24, US31, US33
- **Black-Box Testing**: Execute full CSV export; verify all 7 files exist with valid row counts and non-zero size.
- **White-Box Testing**: Statement coverage across all export routines in `ReportService`.
- **Symbolic/Concolic Relevance**: Multi-file CSV schema compliance verification.
- **GitHub Issue**: `[US35] Complete integrated multi-dataset reporting and CSV export suite`
- **Branch**: `feature/US35-integrated-reporting-export`
- **Definition of Done**: Generates all 7 CSV files without error.

#### US36 – Final CLI Integration and Usability
- **User Story**: *As a user, I want the application integrated and easy to navigate so that all major features can be accessed consistently.*
- **Acceptance Criteria**:
  - Consistent numbered menu (0 to 19) with back navigation on every submenu.
  - Safe exit confirmation on option 0.
  - Clean error messages on invalid input; zero crashes on EOF or Ctrl+C.
  - Polished ASCII table rendering with column truncation.
- **Assigned Member**: Jalakam Prashanth (Pj161) | **Sprint**: 3 | **Story Points**: 3 | **Priority**: High
- **Related Modules**: `main.py`, `interface/menu.py`, `interface/formatting.py`, `interface/input_handler.py`
- **Dependencies**: All preceding stories
- **Black-Box Testing**: Walk through every menu option from 0 to 19; test cancellation ('B'); verify clean exit.
- **White-Box Testing**: Statement and branch coverage across `MainMenu` and `InputHandler`.
- **Symbolic/Concolic Relevance**: Comprehensive CLI navigation state machine verification.
- **GitHub Issue**: `[US36] Final application integration, menu usability, and error trapping`
- **Branch**: `feature/US36-final-cli-integration`
- **Definition of Done**: Application runs end-to-end smoothly, suitable for laboratory demonstrations.
