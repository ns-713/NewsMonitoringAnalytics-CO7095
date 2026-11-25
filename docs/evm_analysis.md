# Earned Value Management (EVM) Analysis Plan
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction to Earned Value Management

**Earned Value Management (EVM)** is an established software measurement and project control methodology that integrates project scope, schedule, and resource metrics into a unified performance measurement baseline (Fleming & Koppelman, 2010). By continuously comparing planned progress against actual expenditure and work completed, EVM enables project leadership to detect schedule slippages and effort deviations early in the development lifecycle.

### 1.1 Core Metrics Definitions

1. **Budget at Completion (BAC)**: The total planned budget allocated to complete the entire project scope. In agile software engineering, BAC is primarily established in **Planned Story Points (SP)** and mapped to an authorized financial baseline.
2. **Planned Value (PV)**: The authorized budget assigned to scheduled work expected to be completed by a specific milestone or reporting date.
3. **Earned Value (EV)**: The quantified value of work physically completed by the reporting date, measured in terms of the budget assigned to that work (100% accepted user stories).
4. **Actual Cost (AC)**: The actual effort or cost incurred in executing the completed work by the reporting date, recorded in developer effort equivalents and financial terms.

---

## 2. EVM Variances and Performance Indices Formulations

$$\text{Cost Variance (CV)} = \text{EV} - \text{AC}$$
- $\text{CV} > 0$: Under budget / effort surplus (favourable).
- $\text{CV} < 0$: Over budget / effort overrun (unfavourable).
- $\text{CV} = 0$: Exactly on budget.

$$\text{Schedule Variance (SV)} = \text{EV} - \text{PV}$$
- $\text{SV} > 0$: Ahead of schedule (favourable).
- $\text{SV} < 0$: Behind schedule (unfavourable).
- $\text{SV} = 0$: Exactly on schedule.

$$\text{Cost Performance Index (CPI)} = \frac{\text{EV}}{\text{AC}}$$
- $\text{CPI} > 1.0$: Effort/cost efficient (earning more value than cost expended).
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

## 3. Agile Story-Point Baseline and Financial Derivation Model

### 3.1 Primary Agile Measurement Baseline (Story Points)
In the Group 19 Scrum framework, the primary unit of project measurement is the **Story Point (SP)**, established through Planning Poker consensus:
- **Total Project Scope (BAC)**: **126 Story Points** across 3 Sprints (40 SP in Sprint 1, 44 SP in Sprint 2, 42 SP in Sprint 3).
- **Planned Value (PV)**: 126 SP.
- **Earned Value (EV)**: 126 SP (100% of User Stories US01–US36 verified and accepted against Definition of Done).
- **Actual Cost (AC)**: 120.0 Story Point equivalents of developer effort expended across all 3 sprints:
  - Sprint 1: 40.6 SP equivalents (early architecture and setup overhead).
  - Sprint 2: 42.7 SP equivalents (deduplication and analytics implementation).
  - Sprint 3: 36.7 SP equivalents (accelerated by test harness reuse and automated testing).
- **Agile Cost Variance**: $\text{CV} = \text{EV} - \text{AC} = 126 - 120 = \mathbf{+6.0 \text{ SP}}$ (Favourable 4.8% effort surplus).
- **Agile Cost Performance Index**: $\text{CPI} = \frac{\text{EV}}{\text{AC}} = \frac{126}{120} = \mathbf{1.050}$.
- **Agile Schedule Performance Index**: $\text{SPI} = \frac{\text{EV}}{\text{PV}} = \frac{126}{126} = \mathbf{1.000}$.

### 3.2 Academic Financial Model Derivation
To demonstrate corporate financial EVM governance, an industry-standard financial model is applied using an authorized academic benchmark budget:
- **Authorized Baseline Budget (BAC)**: **£18,000**.
- **Derived Baseline Rate per Story Point**:
  $$\text{Unit Rate} = \frac{\text{BAC}}{\text{Total SP}} = \frac{£18,000}{126 \text{ SP}} = \mathbf{£142.86 \text{ per Story Point}}$$
- **Conversion to Financial Performance Metrics**:
  - **Planned Value (PV)**: $126 \text{ SP} \times £142.86 = \mathbf{£18,000}$.
  - **Earned Value (EV)**: $126 \text{ SP} \times £142.86 = \mathbf{£18,000}$.
  - **Actual Cost (AC)**: **£17,140** (directly recorded from engineering timesheets across sprints: Sprint 1: £5,800, Sprint 2: £6,100, Sprint 3: £5,240; corresponding to 120.0 Story Point effort equivalents at the £142.86/SP baseline, with nominal rounding).
  - **Financial Cost Variance (CV)**:
    $$\text{CV} = \text{EV} - \text{AC} = £18,000 - £17,140 = \mathbf{+£860 \text{ (Favourable Underspend)}}$$
  - **Financial Schedule Variance (SV)**:
    $$\text{SV} = \text{EV} - \text{PV} = £18,000 - £18,000 = \mathbf{£0.00 \text{ (Exactly on Schedule)}}$$
  - **Cost Performance Index (CPI)**:
    $$\text{CPI} = \frac{£18,000}{£17,140} \approx \mathbf{1.050}$$
  - **Estimate at Completion (EAC)**:
    $$\text{EAC} = \frac{\text{BAC}}{\text{CPI}} = \frac{£18,000}{1.050} = \mathbf{£17,140}$$
  - **Variance at Completion (VAC)**:
    $$\text{VAC} = \text{BAC} - \text{EAC} = £18,000 - £17,140 = \mathbf{+£860 \text{ (Projected Favourable Surplus)}}$$

---

## 4. Final Project Performance Measurement Summary

| Metric Name | Symbol / Formula | Sprint 1 | Sprint 2 | Sprint 3 (Final) | Cumulative Project Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Budget at Completion (BAC)** | $\text{BAC}$ | £5,714 (40 SP) | £6,286 (44 SP) | £6,000 (42 SP) | **£18,000 (126 SP)** |
| **Planned Value (PV)** | $\text{PV}$ | £5,714 (40 SP) | £6,286 (44 SP) | £6,000 (42 SP) | **£18,000 (126 SP)** |
| **Earned Value (EV)** | $\text{EV}$ | £5,714 (40 SP) | £6,286 (44 SP) | £6,000 (42 SP) | **£18,000 (126 SP)** |
| **Actual Cost (AC)** | $\text{AC}$ | £5,800 (40.6 SP) | £6,100 (42.7 SP) | £5,240 (36.7 SP) | **£17,140 (120.0 SP)** |
| **Cost Variance (CV)** | $\text{EV} - \text{AC}$ | -£86 (-0.6 SP) | +£186 (+1.3 SP) | +£760 (+5.3 SP) | **+£860 (+6.0 SP)** |
| **Schedule Variance (SV)** | $\text{EV} - \text{PV}$ | £0 (0 SP) | £0 (0 SP) | £0 (0 SP) | **£0.00 (0 SP)** |
| **Cost Performance Index (CPI)** | $\text{EV} / \text{AC}$ | 0.985 | 1.030 | 1.145 | **1.050** |
| **Schedule Performance Index (SPI)** | $\text{EV} / \text{PV}$ | 1.000 | 1.000 | 1.000 | **1.000** |
| **Estimate at Completion (EAC)** | $\text{BAC} / \text{CPI}$ | £18,274 | £17,475 | £17,140 | **£17,140** |
| **Estimate to Complete (ETC)** | $\text{EAC} - \text{AC}$ | £12,474 | £5,575 | £0 | **£0.00** |
| **Variance at Completion (VAC)** | $\text{BAC} - \text{EAC}$ | -£274 | +£525 | +£860 | **+£860** |

---

## 5. Practical Value and Managerial Action Triggers

EVM enables the team to maintain proactive process control throughout the software lifecycle:
- **When $\text{SPI} < 0.90$**: The Scrum Master immediately flags stories with high slack in the PERT network (e.g., Activity E Search Engine or Activity J RSS Collection) to reassign engineering capacity to critical path blockers.
- **When $\text{CPI} < 0.90$**: Excessive effort is being consumed in rework or unexpected defect fixing; triggers peer code reviews and architectural refactoring before starting subsequent sprints.
- **When $\text{TCPI} > 1.15$**: Re-scoping or backlog refinement is required because completing remaining stories without scope adjustment is statistically improbable under historical performance trends.
