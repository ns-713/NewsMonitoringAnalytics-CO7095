# Earned Value Management (EVM) Analysis Plan
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction to Earned Value Management

**Earned Value Management (EVM)** is a project management methodology that integrates project scope, schedule, and cost metrics into a unified performance measurement baseline. By comparing planned progress against actual expenditure and work completed, EVM enables project managers to detect schedule slippages and cost overruns early in the development lifecycle.

### 1.1 Core Metrics Definitions

1. **Budget at Completion (BAC)**: The total planned budget allocated to complete the entire project scope. In software projects without financial billing, BAC is often measured in **Planned Story Points** or **Planned Labor Hours**.
2. **Planned Value (PV)**: The authorized budget assigned to scheduled work expected to be completed by a specific reporting date.
3. **Earned Value (EV)**: The quantified value of work physically completed by the reporting date, measured in terms of the budget assigned to that work.
4. **Actual Cost (AC)**: The total actual cost (or actual labor hours) incurred in executing the completed work by the reporting date.

---

## 2. EVM Variances and Performance Indices Formulations

$$\text{Cost Variance (CV)} = \text{EV} - \text{AC}$$
- $\text{CV} > 0$: Under budget (favorable).
- $\text{CV} < 0$: Over budget (unfavorable).
- $\text{CV} = 0$: Exactly on budget.

$$\text{Schedule Variance (SV)} = \text{EV} - \text{PV}$$
- $\text{SV} > 0$: Ahead of schedule (favorable).
- $\text{SV} < 0$: Behind schedule (unfavorable).
- $\text{SV} = 0$: Exactly on schedule.

$$\text{Cost Performance Index (CPI)} = \frac{\text{EV}}{\text{AC}}$$
- $\text{CPI} > 1.0$: Cost efficient (earning more value than cost spent).
- $\text{CPI} < 1.0$: Cost inefficient.

$$\text{Schedule Performance Index (SPI)} = \frac{\text{EV}}{\text{PV}}$$
- $\text{SPI} > 1.0$: Progression rate faster than planned.
- $\text{SPI} < 1.0$: Progression rate slower than planned.

### Forecasting Formulations:

$$\text{Estimate at Completion (EAC)} = \frac{\text{BAC}}{\text{CPI}}$$

$$\text{Estimate to Complete (ETC)} = \text{EAC} - \text{AC}$$

$$\text{Variance at Completion (VAC)} = \text{BAC} - \text{EAC}$$

$$\text{To-Complete Performance Index (TCPI)} = \frac{\text{BAC} - \text{EV}}{\text{BAC} - \text{AC}}$$

---

## 3. Worked Sample Calculation Using Hypothetical Data

> [!NOTE]
> **Data Transparency Notice:**
> The following numerical scenario uses **clearly labelled hypothetical data** representing a midpoint project audit at the conclusion of Sprint 2.

### Scenario Baseline:
- **Total Project Budget (BAC)**: **126 Story Points** across 3 Sprints.
- **Reporting Checkpoint**: End of Sprint 2 (Week 4 of a 6-week schedule).
- **Planned Work through Sprint 2 (PV)**:
  - Sprint 1 Planned: 40 Story Points
  - Sprint 2 Planned: 43 Story Points
  - **$\text{PV} = 40 + 43 = \mathbf{83 \text{ Story Points}}$**
- **Actual Work Completed by Sprint 2 (EV)**:
  - Suppose the team successfully delivered Sprint 1 (40 points) and completed 35 points of Sprint 2:
  - **$\text{EV} = 40 + 35 = \mathbf{75 \text{ Story Points}}$**
- **Actual Labor Invested (AC)**:
  - Suppose the team logged the equivalent effort of **80 Story Points** due to extra debugging in XML RSS feeds:
  - **$\text{AC} = \mathbf{80 \text{ Point Equivalents}}$**

### Calculations:
1. **Cost Variance (CV)**:
   $$\text{CV} = \text{EV} - \text{AC} = 75 - 80 = \mathbf{-5.00 \text{ Points (Cost Overrun)}}$$
2. **Schedule Variance (SV)**:
   $$\text{SV} = \text{EV} - \text{PV} = 75 - 83 = \mathbf{-8.00 \text{ Points (Behind Schedule)}}$$
3. **Cost Performance Index (CPI)**:
   $$\text{CPI} = \frac{75}{80} \approx \mathbf{0.938}$$
   *Interpretation*: For every 1.0 unit of effort expended, the team earned 0.938 units of completed value.
4. **Schedule Performance Index (SPI)**:
   $$\text{SPI} = \frac{75}{83} \approx \mathbf{0.904}$$
   *Interpretation*: The team is progressing at ~90.4% of the planned schedule speed.
5. **Estimate at Completion (EAC)**:
   $$\text{EAC} = \frac{\text{BAC}}{\text{CPI}} = \frac{126}{0.938} \approx \mathbf{134.33 \text{ Total Points Expected}}$$
6. **Estimate to Complete (ETC)**:
   $$\text{ETC} = \text{EAC} - \text{AC} = 134.33 - 80 = \mathbf{54.33 \text{ Additional Points Needed}}$$
7. **Variance at Completion (VAC)**:
   $$\text{VAC} = \text{BAC} - \text{EAC} = 126 - 134.33 = \mathbf{-8.33 \text{ Points Deficit at Project Finish}}$$
8. **To-Complete Performance Index (TCPI)**:
   $$\text{TCPI} = \frac{126 - 75}{126 - 80} = \frac{51}{46} \approx \mathbf{1.109}$$
   *Interpretation*: To finish on the original budget, the team must increase productivity by ~10.9% during Sprint 3.

---

## 4. Blank Actual Project Measurement Template

Team members should populate this table as real sprint measurements are recorded during coursework execution:

| Metric Name | Symbol / Formula | Sprint 1 Actual | Sprint 2 Actual | Sprint 3 Actual | Final Project Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Budget at Completion** | $\text{BAC}$ | 126 | 126 | 126 | 126 |
| **Planned Value** | $\text{PV}$ | 40 | 83 | 126 | 126 |
| **Earned Value** | $\text{EV}$ | [     ] | [     ] | [     ] | [     ] |
| **Actual Cost / Effort** | $\text{AC}$ | [     ] | [     ] | [     ] | [     ] |
| **Cost Variance** | $\text{EV} - \text{AC}$ | [     ] | [     ] | [     ] | [     ] |
| **Schedule Variance** | $\text{EV} - \text{PV}$ | [     ] | [     ] | [     ] | [     ] |
| **Cost Performance Index** | $\text{EV} / \text{AC}$ | [     ] | [     ] | [     ] | [     ] |
| **Schedule Performance Index** | $\text{EV} / \text{PV}$ | [     ] | [     ] | [     ] | [     ] |
| **Estimate at Completion** | $\text{BAC} / \text{CPI}$ | [     ] | [     ] | [     ] | [     ] |
| **Estimate to Complete** | $\text{EAC} - \text{AC}$ | [     ] | [     ] | [     ] | [     ] |
| **Variance at Completion** | $\text{BAC} - \text{EAC}$ | [     ] | [     ] | [     ] | [     ] |

---

## 5. Practical Value and Managerial Action Triggers

EVM enables the team to maintain proactive process control:
- **When $\text{SPI} < 0.90$**: The Scrum Master immediately flags stories with high slack in the PERT chart (e.g., Activity E Search Engine or Activity J RSS Collection) to reassign capacity to critical path blockers.
- **When $\text{CPI} < 0.90$**: Excessive effort is being consumed in rework or unbudgeted bug fixes; triggers a peer code review and quality refactoring session before starting the next sprint.
- **When $\text{TCPI} > 1.15$**: Re-scoping or backlog refinement is required because completing remaining stories without scope modification is statistically improbable under historical performance.
