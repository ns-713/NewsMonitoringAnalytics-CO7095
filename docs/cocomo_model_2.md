# Constructive Cost Model II (COCOMO II) Estimation
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction and Architectural Model Framework

> [!NOTE]
> **Estimation Context Disclaimer:**
> In accordance with academic assessment rigor, the values presented here are parametric predictive estimates derived from the **COCOMO II Post-Architecture Model (2000)**. They reflect model-based planning baselines rather than retrospective payroll records.

**COCOMO II** extends the original 1981 model to account for modern development practices, object-oriented design, software reuse, developer capability, and process maturity. It introduces **5 Scale Factors ($W_i$)** that determine project diseconomies of scale and **17 Effort Multipliers ($\text{EM}_i$)** representing cost drivers.

---

## 2. COCOMO II Core Mathematical Formulation

### 2.1 Effort Equation (Person-Months)

$$\text{Effort (PM)} = A \times (\text{Size})^E \times \prod_{i=1}^{n} \text{EM}_i$$

Where:
- $A = 2.94$ (Calibrated baseline productivity constant for COCOMO II.2000).
- $\text{Size}$ is software size in thousands of Source Lines of Code (**KLOC**).
- $E$ is the scaling exponent determined by team scale factors:

$$E = B + 0.01 \times \sum_{i=1}^{5} \text{SF}_i$$

- $B = 0.91$ (Base exponent constant).
- $\text{EM}_i$ are the Effort Multipliers.

### 2.2 Schedule Equation (Calendar Months)

$$T_{\text{dev}} = C \times (\text{PM})^F$$

$$F = D + 0.2 \times (E - B) = 0.28 + 0.2 \times (E - 0.91)$$

Where $C = 3.67$ and $D = 0.28$.

---

## 3. Scale Factor (SF) Evaluation and Exponent Calculation

COCOMO II incorporates five scale factors that quantify whether the project experiences economies or diseconomies of scale:

| Scale Factor | Description | Project Rating | Value ($\text{SF}_i$) | Context Justification |
| :--- | :--- | :---: | :---: | :--- |
| **PREC** | Precedentedness | **High** | 3.72 | News ingestion, search, and RSS parsing are established problem domains with abundant architectural precedents. |
| **FLEX** | Development Flexibility | **High** | 3.04 | Relaxed external client constraints; high design freedom in structuring internal algorithms and test suites. |
| **RESL** | Architecture / Risk Resolution | **High** | 4.24 | Early modular prototyping, comprehensive UML design, and robust test runners developed in early sprints. |
| **TEAM** | Team Cohesion | **High** | 3.29 | Small 4-member postgraduate group with shared objectives, Git workflow, and daily collaboration. |
| **PMAT** | Process Maturity | **Nominal** | 4.68 | Structured Agile Scrum with requirements traceability, GitHub milestone tracking, and CMMI Level 2 audit adherence. |
| **Total Sum** | $\sum \text{SF}_i$ | | **18.97** | |

### Scaling Exponent ($E$) Calculation:
$$E = 0.91 + 0.01 \times (18.97) = 0.91 + 0.1897 = \mathbf{1.0997 \approx 1.100}$$

Because $E > 1.0$, the project exhibits slight diseconomies of scale, reflecting the increasing integration, synchronization, and communication overhead among team members.

---

## 4. Effort Multipliers (Cost Drivers) Selection

The 17 post-architecture cost drivers were evaluated against the project environment:

| Category | Cost Driver | Rating | Multiplier ($\text{EM}_i$) | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Product** | **RELY** (Required Reliability) | Nominal | 1.00 | Local academic application; non-critical life/financial system. |
| | **DATA** (Database Size) | Nominal | 1.00 | Data storage footprint (< 100 MB) is well within memory capacity. |
| | **CPLX** (Product Complexity) | Nominal | 1.00 | Standard string matching, Jaccard similarity, and XML parsing. |
| | **DOCU** (Documentation Match) | High | 1.11 | Extensive coursework documentation, SRS, architecture, and research papers. |
| **Platform** | **TIME** (Execution Time Constraint) | Nominal | 1.00 | Non-real-time CLI execution without millisecond hard deadlines. |
| | **STOR** (Main Storage Constraint) | Nominal | 1.00 | Runs easily within standard lab computer RAM (8–16 GB). |
| | **PVOL** (Platform Volatility) | Low | 0.87 | Stable Python 3.12 standard library environment without frequent OS shifts. |
| **Personnel**| **ACAP** (Analyst Capability) | High | 0.85 | Strong postgraduate analytical skills in measurement and testing. |
| | **PCAP** (Programmer Capability) | High | 0.88 | Competent Python engineering skills across all four contributors. |
| | **PCON** (Personnel Continuity) | High | 0.90 | Stable team roster maintained across the semester without turnover. |
| | **AEXP** (Applications Experience) | Nominal | 1.00 | Moderate familiarity with news analytics and text processing. |
| | **PEXP** (Platform Experience) | High | 0.91 | Extensive daily familiarity with Python, PyCharm, and Windows/Linux. |
| | **LTEX** (Language & Tool Experience)| High | 0.91 | High proficiency with Python standard library and `unittest`. |
| **Project** | **TOOL** (Use of Software Tools) | High | 0.90 | Automated test runners, PyCharm IDE diagnostics, and Git/GitHub Projects. |
| | **SITE** (Multisite Development) | Nominal | 1.00 | Combined in-person lab collaboration and shared GitHub repository. |
| | **SCED** (Required Schedule) | Nominal | 1.00 | Balanced 6-week schedule aligned with university coursework calendar. |

### Cumulative Effort Adjustment Factor ($\prod \text{EM}_i$):
$$\prod_{i=1}^{16} \text{EM}_i = 1.00 \times 1.00 \times 1.00 \times 1.11 \times 1.00 \times 1.00 \times 0.87 \times 0.85 \times 0.88 \times 0.90 \times 1.00 \times 0.91 \times 0.91 \times 0.90 \times 1.00 \times 1.00$$
$$\prod \text{EM}_i \approx \mathbf{0.485}$$

The favorable developer capability, platform stability, and modern tooling significantly reduce required effort compared to industry nominal baselines.

---

## 5. Detailed Step-by-Step Calculations

### 5.1 Scenario A: Core Application Codebase ($\text{Size} = 2.741 \text{ KLOC}$)

1. **Effort (PM)**:
   $$\text{PM} = A \times (\text{Size})^E \times \prod \text{EM}_i$$
   $$\text{PM} = 2.94 \times (2.741)^{1.100} \times 0.485$$
   $$(2.741)^{1.100} \approx 3.0305$$
   $$\text{PM} = 2.94 \times 3.0305 \times 0.485 = \mathbf{4.32 \text{ Person-Months}}$$

2. **Schedule Calculation ($T_{\text{dev}}$)**:
   $$F = 0.28 + 0.2 \times (1.100 - 0.91) = 0.28 + 0.038 = \mathbf{0.318}$$
   $$T_{\text{dev}} = 3.67 \times (\text{PM})^F = 3.67 \times (4.32)^{0.318}$$
   $$(4.32)^{0.318} \approx 1.590$$
   $$T_{\text{dev}} = 3.67 \times 1.590 = \mathbf{5.84 \text{ Calendar Months}}$$

3. **Average Staffing**:
   $$\text{Staff} = \frac{\text{PM}}{T_{\text{dev}}} = \frac{4.32}{5.84} = \mathbf{0.74 \text{ Full-Time Persons}}$$

---

### 5.2 Scenario B: Total Delivered System Including Test Suites ($\text{Size} = 5.275 \text{ KLOC}$)

1. **Effort (PM)**:
   $$\text{PM} = 2.94 \times (5.275)^{1.100} \times 0.485$$
   $$(5.275)^{1.100} \approx 6.2238$$
   $$\text{PM} = 2.94 \times 6.2238 \times 0.485 = \mathbf{8.87 \text{ Person-Months}}$$

2. **Schedule Calculation ($T_{\text{dev}}$)**:
   $$T_{\text{dev}} = 3.67 \times (8.87)^{0.318}$$
   $$(8.87)^{0.318} \approx 2.000$$
   $$T_{\text{dev}} = 3.67 \times 2.000 = \mathbf{7.34 \text{ Calendar Months}}$$

3. **Average Staffing Requirement**:
   $$\text{Staff} = \frac{\text{PM}}{T_{\text{dev}}} = \frac{8.87}{7.34} = \mathbf{1.21 \text{ Full-Time Equivalent Persons}}$$

---

## 6. Comparison of COCOMO I vs. COCOMO II

| Metric | Basic COCOMO I (Scenario B) | COCOMO II Post-Architecture (Scenario B) | Analytical Variance & Insights |
| :--- | :---: | :---: | :--- |
| **Effort (Person-Months)** | 13.84 PM | **8.87 PM** | COCOMO II estimates ~35.9% less effort due to credit for modern IDE tooling, team cohesion, and high language expressiveness. |
| **Development Schedule** | 6.78 Months | **7.34 Months** | COCOMO II schedule formula $T_{\text{dev}} = 3.67 \times (\text{PM})^{0.318}$ yields slightly longer nominal elapsed duration. |
| **Average Staffing** | 2.04 FTE | **1.21 FTE** | COCOMO II demonstrates that high analyst and tool capabilities require fewer full-time developers to achieve the same delivery. |

---

## 7. Assumptions and Limitations

- **Calibration Baseline**: COCOMO II parameters are calibrated against historical commercial software projects; university coursework exhibits different labor dynamics (e.g., intensive part-time bursts around deadlines).
- **Tool Automation**: Python's rich standard library (`urllib`, `xml.etree.ElementTree`, `unittest`, `csv`) significantly reduces the amount of boilerplate code required compared to lower-level languages.
