# Test Execution, Defect Tracking, and Retesting Templates
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Metric Definition and Distinction Guide

> [!IMPORTANT]
> **Measurement Distinction Rule:**
> - **Test Pass Rate (%)**: Quantifies test assertion correctness.
>   $$\text{Test Pass Rate} = \frac{\text{Passed Tests}}{\text{Total Executed Tests}} \times 100$$
> - **Code Coverage (%)**: Quantifies the percentage of physical source code statements executed by the test suite.
>   $$\text{Statement Coverage} = \frac{\text{Executed Statements}}{\text{Total Measured Statements}} \times 100$$
> *Compilation success or test passing does NOT equal code coverage.*

---

## 2. Test Execution Log Template

Use this template to record official test runs across project sprints:

| Execution Run ID | Date & Timestamp | Target Test Suite | Executed By | Total Tests | Passed | Failed | Errors | Skipped | Pass Rate (%) | Duration (s) | Artifact Log Reference |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **RUN-001** | 2026-11-18 11:54 | Master Test Suite | Automated | 130 | 123 | 7 | 0 | 0 | 94.6% | 7.37s | `reports/execution/test_run_summary.txt` |
| **RUN-002** | 2026-11-18 11:56 | Master Test Suite | Automated | 130 | 130 | 0 | 0 | 0 | **100.0%** | 6.58s | Verified fixes applied |
| **RUN-003** | 2026-11-18 11:57 | Master Test Suite (+UI) | Automated | 139 | 139 | 0 | 0 | 0 | **100.0%** | 4.43s | Complete Master Benchmark |
| **RUN-004** | 2026-11-25 15:24 | Master Test Suite (Full System + SMT/Concolic Research) | Automated | 195 | 195 | 0 | 0 | 0 | **100.0%** | 26.83s | `reports/execution/test_run_summary.txt` (85.2% statement coverage) |

---

## 3. Defect Report Template

When a test failure occurs, log the defect using the following standardized schema:

```markdown
### DEFECT REPORT: [DEF-xxx] <Brief Title>

- **Defect ID**: DEF-001 (Example)
- **Date Logged**: 2026-11-18
- **Discovered In Test**: `test_tc_bb_dup_05_high_similarity_near_duplicate`
- **Severity**: Low / Minor / Major / Critical
- **Assigned Developer**: Jyothi Bandalapati (`Jb1080`)
- **Component / File**: `services/duplicate_service.py` / `jb1080/test/`
- **Description / Traceback**:
  `AssertionError: False is not true`
  Test headline variant produced Jaccard similarity of 0.666, which is strictly below the 0.70 threshold.
- **Root Cause Analysis**:
  The candidate headline in the test fixture had 9 union tokens with 6 intersections (6/9 = 0.6666 < 0.70).
- **Corrective Action**:
  Adjusted candidate headline to share 7 tokens out of 8 union tokens (7/8 = 0.875 >= 0.70), accurately verifying the high-similarity threshold branch.
- **Retest Verification**: Verified in RUN-002; test now passes cleanly.
- **Status**: CLOSED
```

### Blank Defect Logging Form:

| Defect ID | Date | Discovered In Test | Severity | Component | Summary of Defect | Status | Resolved By |
| :---: | :---: | :--- | :---: | :--- | :--- | :---: | :---: |
| **DEF-001** | 2026-11-18 | `test_tc_bb_dup_05` | Minor | Duplicate Test | Similarity token threshold boundary mismatch | CLOSED | Jb1080 |
| **DEF-002** | 2026-11-18 | `test_tc_wb_rss_04` | Major | RSS Service | ElementTree boolean node truth value dropping items | CLOSED | ns713 |
| **DEF-003** | 2026-11-18 | `test_tc_wb_tim_01` | Minor | Time Analytics | RFC 822 GMT dates missing dedicated parsedate call | CLOSED | Jb1080 |
| **DEF-004** | 2026-11-18 | `test_tc_wb_mnu_01` | Minor | Report Service | Export directory auto-creation on late reassignment | CLOSED | Pj161 |
| *[DEF-xxx]* | *[Date]* | *[Test ID]* | *[...] | *[...] | *[...] | *[OPEN/CLOSED]* | *[...] |

---

## 4. Retesting and Regression Verification Evidence

Whenever a bug is repaired, the developer must:
1. Execute the isolated failing test to confirm that the fix resolves the specific failure:
   ```bash
   python -m unittest ns713/test/blackbox/test_rss_blackbox.py
   ```
2. Execute the entire master test suite to verify that the change introduced **zero regressions** into other modules:
   ```bash
   python run_tests.py
   ```
3. Record the regression verification status in the defect log above before marking the issue as `CLOSED`.
