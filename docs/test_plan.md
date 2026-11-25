# Master Software Test Plan
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction and Objectives

This **Master Software Test Plan** defines the formal verification and validation strategy for the **News Monitoring and Analytics Application**. The testing framework verifies that all 15 Functional Requirements (FR01–FR15) and 36 Agile User Stories (US01–US36) are completely satisfied, robust against edge cases, and resilient against input errors and network faults.

---

## 2. Levels of Testing

```
+-------------------------------------------------------------+
|              Acceptance Testing (User Scenarios)            |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|       System Testing (Complete Lifecycle & Data Recovery)    |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|     Integration Testing (Pipeline, Alerts, Analytics)       |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|       Unit Testing (Black-Box, White-Box, Symbolic, Concolic)|
+-------------------------------------------------------------+
```

### 2.1 Unit Testing
- **Scope**: Individual functions, methods, and classes within `models/`, `services/`, `storage/`, and `interface/`.
- **Framework**: Python Standard Library `unittest`.
- **Techniques**: Black-box specification partitioning, boundary value analysis, white-box branch coverage, loop testing, exception path validation.

### 2.2 Integration Testing
- **Scope**: Interactions between collaborating services (e.g., `NewsService` invoking `CategorisationService`, `SentimentService`, `DuplicateService`, and `AlertService`).
- **Target Suites**:
  - `tests/shared/integration/test_news_pipeline_integration.py`
  - `tests/shared/integration/test_monitoring_alert_integration.py`
  - `tests/shared/integration/test_analytics_reporting_integration.py`

### 2.3 System Testing
- **Scope**: Complete application lifecycle executed in an isolated environment simulating the end-to-end user journey.
- **Target Suites**:
  - `tests/shared/system/test_end_to_end_system.py`: Ingestion, search, filtering, alert acknowledgment, and report generation.
  - `tests/shared/system/test_data_recovery_system.py`: File corruption failover and atomic write verification.

### 2.4 Research Testing Methodologies
- **Symbolic Execution**: Abstract mathematical modeling of program paths to solve for branch constraints and identify execution conditions.
- **Concolic Testing (Concrete + Symbolic)**: Dynamic test generation combining concrete execution with branch constraint negation to discover unexplored paths.

---

## 3. Testing Ownership Matrix

Testing responsibilities are partitioned among all four team members to ensure balanced verification rigor:

| Member | Identifier | Student ID | Primary Modules Under Test | Assigned Test Suites |
| :--- | :--- | :--- | :--- | :--- |
| **Nikitha Sarpur** | `ns713` | 259060190 | `models/article.py`<br>`models/news_source.py`<br>`services/rss_service.py`<br>`storage/json_storage.py` | `ns713/test/blackbox/`<br>`ns713/test/whitebox/`<br>`ns713/test/symbolic/`<br>`ns713/test/concolic/` |
| **Sashi Dommaraju** | `Sd683` | 259062044 | `services/search_service.py`<br>`services/categorisation_service.py`<br>`services/sentiment_service.py` | `sd683/test/blackbox/`<br>`sd683/test/whitebox/`<br>`sd683/test/symbolic/`<br>`sd683/test/concolic/` |
| **Jyothi Bandalapati** | `Jb1080` | 259060742 | `services/duplicate_service.py`<br>`services/trend_service.py`<br>`services/source_analytics_service.py`<br>`services/time_analytics_service.py` | `jb1080/test/blackbox/`<br>`jb1080/test/whitebox/`<br>`jb1080/test/symbolic/`<br>`jb1080/test/concolic/` |
| **Jalakam Prashanth** | `Pj161` | 259060676 | `models/alert_rule.py`<br>`models/alert.py`<br>`services/alert_service.py`<br>`services/report_service.py`<br>`services/dashboard_service.py`<br>`interface/` | `pj161/test/blackbox/`<br>`pj161/test/whitebox/`<br>`pj161/test/symbolic/`<br>`pj161/test/concolic/` |
| **Shared Team** | *All* | *All* | Complete Integrated Subsystems & System Failover | `tests/shared/integration/`<br>`tests/shared/system/` |

---

## 4. Test Pass and Exit Criteria

### 4.1 Test Pass Criteria
- **Individual Test Case**: Evaluated as **PASS** if all `self.assert*` conditions evaluate to true with zero unhandled exceptions.
- **Suite Pass Rate Requirement**: **100% Pass Rate** on all committed branches. Zero known failing tests are permitted in release packages.

### 4.2 Code Coverage Target
- **Target Coverage**: **$\ge 85\%$ Statement Coverage** across core business models and services (`models/`, `services/`, `storage/`).
- **Current Verified Benchmark**:
  - `duplicate_service.py`: **95.7%**
  - `models/article.py`: **95.2%**
  - `dashboard_service.py`: **94.7%**
  - `search_service.py`: **93.7%**
  - `categorisation_service.py`: **92.3%**
  - `alert_service.py`: **91.7%**
  - `models/alert_rule.py`: **91.1%**
  - `trend_service.py`: **90.9%**
  - `report_service.py`: **90.7%**
  - `sentiment_service.py`: **85.9%**
  - `source_analytics_service.py`: **85.2%**
  - `rss_service.py`: **88.4%**
  - `json_storage.py`: **80.7%**
  - `formatting.py`: **100.0%**

---

## 5. Test Execution Instructions

### 5.1 Running the Master Test Suite
```bash
python run_tests.py
```
This discovers all 195 tests across all member folders, shared suites, and research modules, executes them under code tracing, and generates summary reports in `reports/execution/` and `reports/coverage/`.

### 5.2 Running Individual Member Suites
```bash
python run_tests.py --member ns713    # Nikitha Sarpur's tests
python run_tests.py --member sd683    # Sashi Dommaraju's tests
python run_tests.py --member jb1080   # Jyothi Bandalapati's tests
python run_tests.py --member pj161    # Jalakam Prashanth's tests
python run_tests.py --shared          # Shared integration & system tests
```

### 5.3 Standard Python Unittest CLI
```bash
python -m unittest discover -s tests
```
