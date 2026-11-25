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

## 3. Financial and Story-Point Baseline Model

### Scenario Baseline:
- **Total Project Budget (BAC)**: **126 Story Points** across 3 Sprints (Valued at **£18,000** based on standard academic industry labor rate of £142.86 per point across 4 engineers).
- **Sprint Schedule**:
  - **Sprint 1 Planned**: 40 Story Points (£5,714)
  - **Sprint 2 Planned**: 44 Story Points (£6,286) — Cumulative PV: 84 SP (£12,000)
  - **Sprint 3 Planned**: 42 Story Points (£6,000) — Cumulative PV: 126 SP (£18,000)
- **Final Project Execution Totals**:
  - **Planned Value (PV)**: 126 SP (£18,000)
  - **Earned Value (EV)**: 126 SP (£18,000) — 100% of User Stories US01–US36 verified and accepted.
  - **Actual Cost (AC)**: 120 Point Equivalents (£17,140) — Favourable efficiency realized from automated testing and code reuse.

### Final Key Performance Calculations:
1. **Cost Variance (CV)**:
   $$\text{CV} = \text{EV} - \text{AC} = £18,000 - £17,140 = \mathbf{+£860 \text{ (Favourable Underspend)}}$$
2. **Schedule Variance (SV)**:
   $$\text{SV} = \text{EV} - \text{PV} = £18,000 - £18,000 = \mathbf{£0.00 \text{ (Exactly on Schedule)}}$$
3. **Cost Performance Index (CPI)**:
   $$\text{CPI} = \frac{\text{EV}}{\text{AC}} = \frac{£18,000}{£17,140} \approx \mathbf{1.050}$$
4. **Schedule Performance Index (SPI)**:
   $$\text{SPI} = \frac{\text{EV}}{\text{PV}} = \frac{£18,000}{£18,000} = \mathbf{1.000}$$
5. **Estimate at Completion (EAC)**:
   $$\text{EAC} = \frac{\text{BAC}}{\text{CPI}} = \frac{£18,000}{1.050} = \mathbf{£17,140}$$
6. **Estimate to Complete (ETC)**:
   $$\text{ETC} = \text{EAC} - \text{AC} = £17,140 - £17,140 = \mathbf{£0.00 \text{ (Work Fully Completed)}}$$
7. **Variance at Completion (VAC)**:
   $$\text{VAC} = \text{BAC} - \text{EAC} = £18,000 - £17,140 = \mathbf{+£860 \text{ (Projected Favourable Surplus)}}$$
8. **To-Complete Performance Index (TCPI)**:
   $$\text{TCPI} = \frac{\text{BAC} - \text{EV}}{\text{BAC} - \text{AC}} = \frac{£18,000 - £18,000}{£18,000 - £17,140} \implies \mathbf{1.000}$$

---

## 4. Final Project Performance Measurement Summary

| Metric Name | Symbol / Formula | Sprint 1 | Sprint 2 | Sprint 3 (Final) | Cumulative Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Budget at Completion (BAC)** | $\text{BAC}$ | £5,714 (40 SP) | £6,286 (44 SP) | £6,000 (42 SP) | **£18,000 (126 SP)** |
| **Planned Value (PV)** | $\text{PV}$ | £5,714 (40 SP) | £6,286 (44 SP) | £6,000 (42 SP) | **£18,000 (126 SP)** |
| **Earned Value (EV)** | $\text{EV}$ | £5,714 (40 SP) | £6,286 (44 SP) | £6,000 (42 SP) | **£18,000 (126 SP)** |
| **Actual Cost (AC)** | $\text{AC}$ | £5,800 | £6,100 | £5,240 | **£17,140** |
| **Cost Variance (CV)** | $\text{EV} - \text{AC}$ | -£86 | +£186 | +£760 | **+£860** |
| **Schedule Variance (SV)** | $\text{EV} - \text{PV}$ | £0 | £0 | £0 | **£0.00** |
| **Cost Performance Index (CPI)** | $\text{EV} / \text{AC}$ | 0.985 | 1.030 | 1.145 | **1.050** |
| **Schedule Performance Index (SPI)** | $\text{EV} / \text{PV}$ | 1.000 | 1.000 | 1.000 | **1.000** |
| **Estimate at Completion (EAC)** | $\text{BAC} / \text{CPI}$ | £18,274 | £17,475 | £17,140 | **£17,140** |
| **Estimate to Complete (ETC)** | $\text{EAC} - \text{AC}$ | £12,474 | £5,575 | £0 | **£0.00** |
| **Variance at Completion (VAC)** | $\text{BAC} - \text{EAC}$ | -£274 | +£525 | +£860 | **+£860** |

---

## 5. Practical Value and Managerial Action Triggers

EVM enables the team to maintain proactive process control:
- **When $\text{SPI} < 0.90$**: The Scrum Master immediately flags stories with high slack in the PERT chart (e.g., Activity E Search Engine or Activity J RSS Collection) to reassign capacity to critical path blockers.
- **When $\text{CPI} < 0.90$**: Excessive effort is being consumed in rework or unbudgeted bug fixes; triggers a peer code review and quality refactoring session before starting the next sprint.
- **When $\text{TCPI} > 1.15$**: Re-scoping or backlog refinement is required because completing remaining stories without scope modification is statistically improbable under historical performance.
