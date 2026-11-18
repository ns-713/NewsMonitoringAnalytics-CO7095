# Constructive Cost Model I (COCOMO I) Estimation
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction and Estimation Premise

> [!NOTE]
> **Estimation Context Disclaimer:**
> The calculations in this document represent algorithmic parametric estimates derived from Boehm's **COCOMO I (1981)** model. They serve as software measurement baselines for academic planning and do not represent actual billable commercial labor or time-card recordings.

The **Constructive Cost Model (COCOMO I)**, developed by Barry Boehm, is an empirical software cost estimation model that relates software size—measured in thousands of Source Lines of Code (KLOC)—to required development effort, project schedule, and team staffing.

---

## 2. Codebase Sizing and Metric Extraction

The source code metrics were physically extracted from the developed repository:

| Code Segment | Total Lines | Blank / Comment Lines | Executable Source Lines of Code (SLOC) | Sizing in KLOC |
| :--- | :---: | :---: | :---: | :---: |
| **Core Application** (`models`, `services`, `storage`, `interface`, `config`) | 3,271 | 530 | **2,741** | **2.741 KLOC** |
| **Verification & Test Suites** (`tests/`, `run_tests.py`) | 3,216 | 682 | **2,534** | **2.534 KLOC** |
| **Total Delivered System** | **6,487** | **1,212** | **5,275** | **5.275 KLOC** |

---

## 3. COCOMO I Development Modes

COCOMO I defines three modes of software development based on system complexity and environmental rigidity:

1. **Organic Mode**:
   - Small, experienced teams working in familiar in-house environments.
   - Stable, thoroughly understood requirements with minimal external system interfaces.
   - Low innovation pressure; standard software practices.
2. **Semi-Detached Mode**:
   - Intermediate team size with mixed levels of domain experience.
   - Blend of rigid and relaxed requirements with moderate technical interfaces.
3. **Embedded Mode**:
   - Highly complex, mission-critical systems with severe hardware and operational constraints (e.g., avionics, real-time air traffic control).
   - Strict regulatory oversight and inflexible interfaces.

### Mode Selection & Justification:
The **News Monitoring and Analytics Application** is classified under the **Organic Mode**:
- **Team Size**: 4 postgraduate university students working collaboratively in a familiar academic environment.
- **Technology Stack**: Standard Python 3, JSON persistence, and standard libraries with zero external paid APIs or embedded hardware constraints.
- **Domain Understanding**: Clear, stable coursework requirements with flexible internal design freedom.

---

## 4. Mathematical Equations and Parameter Coefficients

The Basic COCOMO I equations for effort and schedule are formulated as:

$$\text{Effort} = a \times (\text{KLOC})^b \quad \text{[Person-Months (PM)]}$$

$$T_{\text{dev}} = c \times (\text{Effort})^d \quad \text{[Calendar Months]}$$

$$\text{Average Staffing} = \frac{\text{Effort}}{T_{\text{dev}}} \quad \text{[Full-Time Persons]}$$

$$\text{Productivity} = \frac{\text{SLOC}}{\text{Effort}} \quad \text{[LOC / Person-Month]}$$

### Model Coefficients Table:

| Development Mode | $a$ | $b$ | $c$ | $d$ |
| :--- | :---: | :---: | :---: | :---: |
| **Organic** | **2.4** | **1.05** | **2.5** | **0.38** |
| **Semi-Detached** | 3.0 | 1.12 | 2.5 | 0.35 |
| **Embedded** | 3.6 | 1.20 | 2.5 | 0.32 |

---

## 5. Detailed Step-by-Step Calculations

### 5.1 Scenario A: Core Application Codebase ($\text{Size} = 2.741 \text{ KLOC}$)

1. **Effort Calculation**:
   $$\text{Effort} = 2.4 \times (2.741)^{1.05}$$
   $$(2.741)^{1.05} \approx 2.8753$$
   $$\text{Effort} = 2.4 \times 2.8753 = \mathbf{6.90 \text{ Person-Months (PM)}}$$

2. **Development Time ($T_{\text{dev}}$)**:
   $$T_{\text{dev}} = 2.5 \times (6.90)^{0.38}$$
   $$(6.90)^{0.38} \approx 2.0792$$
   $$T_{\text{dev}} = 2.5 \times 2.0792 = \mathbf{5.20 \text{ Months}}$$

3. **Average Staffing Requirement**:
   $$\text{Staff} = \frac{6.90}{5.20} \approx \mathbf{1.33 \text{ Full-Time Persons}}$$

4. **Productivity**:
   $$\text{Productivity} = \frac{2,741 \text{ LOC}}{6.90 \text{ PM}} \approx \mathbf{397.2 \text{ LOC / Person-Month}}$$

---

### 5.2 Scenario B: Total Delivered System Including Test Suites ($\text{Size} = 5.275 \text{ KLOC}$)

1. **Effort Calculation**:
   $$\text{Effort} = 2.4 \times (5.275)^{1.05}$$
   $$(5.275)^{1.05} \approx 5.7674$$
   $$\text{Effort} = 2.4 \times 5.7674 = \mathbf{13.84 \text{ Person-Months (PM)}}$$

2. **Development Time ($T_{\text{dev}}$)**:
   $$T_{\text{dev}} = 2.5 \times (13.84)^{0.38}$$
   $$(13.84)^{0.38} \approx 2.7118$$
   $$T_{\text{dev}} = 2.5 \times 2.7118 = \mathbf{6.78 \text{ Months}}$$

3. **Average Staffing Requirement**:
   $$\text{Staff} = \frac{13.84}{6.78} \approx \mathbf{2.04 \text{ Full-Time Persons}}$$

4. **Academic Team Alignment**:
   In an academic coursework setting, team members are not working as full-time industrial software engineers; each student dedicates approximately 15–20 hours per week (equivalent to $0.40 - 0.50$ Full-Time Equivalent (FTE)):
   $$\text{Available Team Capacity} = 4 \text{ Students} \times 0.50 \text{ FTE} = \mathbf{2.00 \text{ Full-Time Equivalent Persons}}$$
   This perfectly corroborates the model's staffing calculation of **2.04 persons**, confirming that the project scale is well-dimensioned for a four-person university cohort across a semester.

---

## 6. Assumptions and Model Limitations

1. **Static Sizing Assumption**: Basic COCOMO assumes that KLOC can be estimated accurately upfront. In modern Agile iterative environments, source lines grow incrementally across sprints.
2. **Homogeneous Effort Distribution**: The basic model assumes a uniform distribution of development skill without accounting for variations in unit testing rigor, symbolic execution, or formal documentation overhead.
3. **Language Expressiveness**: COCOMO I was calibrated largely on procedural languages (Fortran, C, COBOL). Modern high-level languages like Python achieve significantly higher functional density per line of code than historical systems, meaning equivalent functional capability requires fewer source lines.
