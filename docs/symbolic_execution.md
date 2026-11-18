# Academic Research Study: Symbolic Execution Analysis
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Introduction to Symbolic Execution

**Symbolic Execution** is a formal program analysis technique that evaluates software by executing programs on abstract symbolic input values rather than concrete data (King, 1976). While concrete execution runs a program on specific inputs (e.g., $x = 5$), symbolic execution assigns symbolic variables (e.g., $x = \alpha$) that represent all possible values within the input domain.

### 1.1 Core Foundations
1. **Symbolic State ($\sigma$)**: A mapping from program variables to symbolic expressions over inputs.
2. **Path Condition ($\Phi$)**: A quantifier-free first-order logic formula that accumulates all branch conditions encountered along a specific execution path. For an execution path to be feasible, $\Phi$ must be satisfiable ($\text{SAT}$).
3. **Constraint Solving**: An automated theorem prover or Satisfiability Modulo Theories (SMT) solver (such as Z3) checks whether a path condition $\Phi$ is satisfiable. If $\text{SAT}$, the solver produces a **model** (a concrete test input) that forces the program to execute that exact path.
4. **Execution Tree**: A tree representation of all possible execution paths through the program, where internal nodes represent conditional branching statements and leaf nodes represent program terminations or return points.

---

## 2. Representative Functions Evaluated Across Team Contributions

To demonstrate comprehensive research application across the developed codebase, representative functions were selected from every team member's engineering contribution:
- **Member 1 (ns713)**: `NewsArticle.validate()` in `models/article.py`
- **Member 2 (Sd683)**: `SentimentService.classify_score()` in `services/sentiment_service.py`
- **Member 3 (Jb1080)**: `DuplicateService.calculate_similarity()` in `services/duplicate_service.py`
- **Member 4 (Pj161)**: `AlertRule.matches()` in `models/alert_rule.py`

---

## 3. Function 1: Article Model Validation (Member 1 - ns713)

### 3.1 Source Code Under Analysis
```python
def validate(self) -> Tuple[bool, List[str]]:
    errors = []
    if not self.headline:                                              # Branch 1
        errors.append("Headline cannot be empty.")
    elif len(self.headline) < 3:                                       # Branch 2
        errors.append("Headline must be at least 3 characters long.")
    if not self.source_name:                                           # Branch 3
        errors.append("Source name cannot be empty.")
    if not self.article_url:                                           # Branch 4
        errors.append("Article URL cannot be empty.")
    if self.sentiment not in ["Positive", "Negative", "Neutral"]:        # Branch 5
        errors.append(f"Invalid sentiment '{self.sentiment}'.")
    return len(errors) == 0, errors
```

### 3.2 Symbolic Variables and Domains
- $H \in \text{String}$ (headline), with symbolic length $L_H = \text{len}(H) \in \mathbb{Z}_{\ge 0}$
- $SN \in \text{String}$ (source name), with length $L_{SN} \in \mathbb{Z}_{\ge 0}$
- $AU \in \text{String}$ (article URL), with length $L_{AU} \in \mathbb{Z}_{\ge 0}$
- $S \in \text{String}$ (sentiment label)

### 3.3 Execution Tree Diagram
```
                     [Root: errors = []]
                             |
                   Is (L_H == 0)?
                    /            \
             True  /              \ False
                  /                \
        [errors += E1]       Is (L_H < 3)?
                             /           \
                      True  /             \ False
                           /               \
                 [errors += E2]      [Check SN]
                                         |
                                  Is (L_SN == 0)?
                                   /           \
                            True  /             \ False
                                 /               \
                       [errors += E3]      [Check AU]
                                               |
                                        Is (L_AU == 0)?
                                         /           \
                                  True  /             \ False
                                       /               \
                             [errors += E4]       [Check S]
                                                      |
                                             Is (S ∉ Valid)?
                                               /           \
                                        True  /             \ False
                                             /               \
                                   [errors += E5]      [errors == []]
                                         |                   |
                                   (False, errors)     (True, [])
```

### 3.4 Path Conditions and Generated Test Cases

| Path ID | Path Condition ($\Phi$) | Constraint Solving Outcome | Generated Concrete Test Input | Expected Output | Actual Verification |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **Path 1** | $L_H = 0 \wedge L_{SN} > 0 \wedge L_{AU} > 0 \wedge S \in \text{Valid}$ | $\text{SAT}$ | `headline=""`, `source="BBC"`, `url="http://a.com"`, `sentiment="Positive"` | `(False, ["Headline cannot be empty."])` | **PASS** (`test_tc_sym_art_all_paths_feasible`) |
| **Path 2** | $L_H \in \{1, 2\} \wedge L_{SN} > 0 \wedge L_{AU} > 0 \wedge S \in \text{Valid}$ | $\text{SAT}$ | `headline="UK"`, `source="BBC"`, `url="http://a.com"`, `sentiment="Neutral"` | `(False, ["Headline must be at least 3 characters long."])` | **PASS** |
| **Path 3** | $L_H \ge 3 \wedge L_{SN} = 0 \wedge L_{AU} > 0 \wedge S \in \text{Valid}$ | $\text{SAT}$ | `headline="Global News"`, `source=""`, `url="http://a.com"`, `sentiment="Positive"` | `(False, ["Source name cannot be empty."])` | **PASS** |
| **Path 4** | $L_H \ge 3 \wedge L_{SN} > 0 \wedge L_{AU} = 0 \wedge S \in \text{Valid}$ | $\text{SAT}$ | `headline="Global News"`, `source="BBC"`, `url=""`, `sentiment="Positive"` | `(False, ["Article URL cannot be empty."])` | **PASS** |
| **Path 5** | $L_H \ge 3 \wedge L_{SN} > 0 \wedge L_{AU} > 0 \wedge S \notin \text{Valid}$ | $\text{SAT}$ | `headline="Global News"`, `source="BBC"`, `url="http://a.com"`, `sentiment="Optimistic"` | `(False, ["Invalid sentiment 'Optimistic'."])` | **PASS** |
| **Path 6** | $L_H \ge 3 \wedge L_{SN} > 0 \wedge L_{AU} > 0 \wedge S \in \text{Valid}$ | $\text{SAT}$ | `headline="Global News"`, `source="BBC"`, `url="http://a.com"`, `sentiment="Positive"` | `(True, [])` | **PASS** |

---

## 4. Function 2: Lexical Sentiment Classification (Member 2 - Sd683)

### 4.1 Source Code Under Analysis
```python
def classify_score(self, score: int) -> str:
    if score > 0:           # Branch 1
        return "Positive"
    elif score < 0:         # Branch 2
        return "Negative"
    else:                   # Branch 3
        return "Neutral"
```

### 4.2 Symbolic Formulation
- Let $P \in \mathbb{Z}_{\ge 0}$ represent count of positive lexicon tokens matched.
- Let $N \in \mathbb{Z}_{\ge 0}$ represent count of negative lexicon tokens matched.
- The score function is defined as: $S(P, N) = P - N$.

### 4.3 Path Conditions and Invariant Verification
- **Path 1 (Positive)**:
  $$\Phi_1 \equiv (P - N > 0) \iff (P > N)$$
  Boundary Solution: $P = 1, N = 0 \implies S = +1 \implies \text{Label} = \text{"Positive"}$.
- **Path 2 (Negative)**:
  $$\Phi_2 \equiv (P - N < 0) \iff (P < N)$$
  Boundary Solution: $P = 0, N = 1 \implies S = -1 \implies \text{Label} = \text{"Negative"}$.
- **Path 3 (Neutral)**:
  $$\Phi_3 \equiv (P - N = 0) \iff (P = N)$$
  Solutions: $P = 0, N = 0$ (no matches) or $P = 3, N = 3$ (balanced polarity).
  In both cases: $S = 0 \implies \text{Label} = \text{"Neutral"}$.

*Automated Verification*: Executed in `tests/sd683/symbolic/test_symbolic_sentiment_scoring.py` with 100% path coverage.

---

## 5. Function 3: Duplicate Similarity Threshold (Member 3 - Jb1080)

### 5.1 Source Code Under Analysis
```python
def calculate_similarity(self, text1: str, text2: str) -> float:
    set1 = set(self.normalise_headline(text1).split())
    set2 = set(self.normalise_headline(text2).split())
    if not set1 and not set2:
        return 1.0 if text1.strip() == text2.strip() else 0.0
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return float(intersection) / float(union) if union > 0 else 0.0
```

### 5.2 Mathematical Constraint Analysis
Let $A = \text{tokens}(T_1)$ and $B = \text{tokens}(T_2)$.
Let $k = |A \cap B|$, $n_A = |A|$, $n_B = |B|$.
The union cardinality is: $u = |A \cup B| = n_A + n_B - k$.
The Jaccard index is:
$$J(A, B) = \frac{k}{n_A + n_B - k}$$

For duplicate flagging under threshold $\theta = 0.70$:
$$\Phi_{\text{duplicate}} \equiv \left(\frac{k}{n_A + n_B - k} \ge 0.70\right) \iff k \ge 0.70 \times (n_A + n_B - k) \iff 1.70k \ge 0.70(n_A + n_B)$$

### 5.3 Boundary Solving:
- For $n_A = 9, n_B = 8, k = 7$:
  $$u = 9 + 8 - 7 = 10 \implies J = \frac{7}{10} = 0.70 \ge 0.70 \quad \text{[SAT: Flagged as Duplicate]}$$
- For $n_A = 8, n_B = 8, k = 6$:
  $$u = 8 + 8 - 6 = 10 \implies J = \frac{6}{10} = 0.60 < 0.70 \quad \text{[SAT: Classified as Unique]}$$

*Automated Verification*: Executed in `tests/jb1080/symbolic/test_symbolic_duplicate_matching.py`.

---

## 6. Function 4: Alert Rule Trigger Evaluation (Member 4 - Pj161)

### 6.1 Source Code Under Analysis
```python
def matches(self, headline: str, content: str = "", category: str = "") -> bool:
    if not self.enabled:                                                             # Branch 1
        return False
    if not self.keyword:                                                             # Branch 2
        return False
    if self.category_filter and self.category_filter.lower() != (category or "").lower(): # Branch 3
        return False
    target_text = f"{headline} {content}".lower()
    return self.keyword in target_text                                               # Branch 4
```

### 6.2 Formal First-Order Logic Path Conditions

| Path ID | Logical Formulation | Outcome | Synthesized Concrete Input |
| :---: | :--- | :---: | :--- |
| **Path 1** | $\neg \text{enabled}$ | `False` | `enabled=False, keyword="climate"` |
| **Path 2** | $\text{enabled} \wedge \text{len}(\text{keyword}) = 0$ | `False` | `enabled=True, keyword=""` |
| **Path 3** | $\text{enabled} \wedge \text{len}(\text{keyword}) > 0 \wedge (\text{category\_filter} \ne \text{None}) \wedge (\text{category\_filter} \ne \text{category})$ | `False` | `filter="Environment", category="Politics"` |
| **Path 4** | $\text{enabled} \wedge \text{len}(\text{keyword}) > 0 \wedge (\text{category\_filter} = \text{None} \vee \text{category\_filter} = \text{category}) \wedge (\text{keyword} \in \text{text})$ | `True` | `keyword="fusion", headline="Nuclear Fusion Energy"` |
| **Path 5** | $\text{enabled} \wedge \text{len}(\text{keyword}) > 0 \wedge (\text{category\_filter} = \text{None} \vee \text{category\_filter} = \text{category}) \wedge (\text{keyword} \notin \text{text})$ | `False` | `keyword="fusion", headline="Solar Panel Expansion"` |

*Automated Verification*: Executed in `tests/pj161/symbolic/test_symbolic_alert_rule_matching.py`.

---

## 7. Practical Theoretical Limitations of Pure Symbolic Execution

While powerful, symbolic execution encounters fundamental theoretical barriers in real-world software:
1. **Path Explosion**: In programs with loops or deep branch nesting, the number of feasible execution paths grows exponentially ($O(2^n)$), overwhelming constraint solvers.
2. **Environment & Native Code Barriers**: Standard SMT solvers cannot symbolically model operating system interactions, disk I/O, or network sockets (e.g., `urllib.request.urlopen`).
3. **Complex String & Regular Expression Theory**: Solving constraints over string transformations (such as regular expression replacement in `clean_html` or lowercase transformations) can be undecidable or computationally intractable for generalized solvers.
4. **Tool Support Trade-offs**: While academic tools like KLEE (for C/LLVM) and symbolic wrappers exist, applying them directly to Python's dynamic runtime requires specialized constraint translation, making hybrid approaches like **Concolic Testing** highly attractive.
