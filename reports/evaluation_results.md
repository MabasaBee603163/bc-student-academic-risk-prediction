# Model Development and Evaluation

**Project:** Belgium Campus — Student Academic Risk Prediction  
**Role:** 1 — Machine Learning Engineer  
**Problem:** Predict a student’s academic risk level as **Low**, **Medium**, or **High** to support early awareness. The model is a **decision-support** signal only — it does not make final academic decisions about students.

---

## 1. Data preparation

### 1.1 Dataset
Live campus extracts were not available for this assignment, so Role 1 generated an **anonymised synthetic dataset** styled after Belgium Campus programmes and SA percentage marking (not US GPA).

| Item | Detail |
|------|--------|
| Generator | `src/data/generate_dataset.py` |
| Output | `data/synthetic/students.csv` |
| Size | 2,000 students |
| Reproducibility | `seed=42` (same seed → same CSV for the whole group) |
| Identity | `student_id` only — no names |

**Programmes (with specialisations):**
- Bachelor of Information Technology — Software Development, Data Science, Cloud Computing, Cybersecurity, Network Engineering  
- Bachelor of Computing — Software Engineering, Artificial Intelligence  
- Diploma in Information Technology — Network Engineering, Software Development, Cybersecurity  
- Higher Certificate in Information Systems — Information Systems, End-User Computing, Systems Support  

**Year of study** is categorical: `First Year`, `Second Year`, `Third Year`, `Fourth Year` (qualification-appropriate limits apply).

### 1.2 Features used for modelling
**Strong predictors (primary risk signal):**
- `attendance` (%)
- `assignment_completion` (%)
- `test_average`, `midyear_average` (%)
- `bc_connect_activity`
- `missed_assessments`
- `failed_modules`

**Supporting academics / load:**
- `overall_average`, `assignment_average`, `practical_average`
- `registered_modules`, `passed_modules`
- `age`

**Context (weaker predictors; kept for realism):**
- `programme`, `specialisation`, `gender`, `year_of_study`

### 1.3 Excluded columns (leakage / IDs)
| Column | Reason |
|--------|--------|
| `student_id` | Identifier only |
| `profile` | Generation helper; not available in real campus data |
| `risk_score` | Continuous form of the label — would leak the target |

**Target:** `risk_label` ∈ {Low, Medium, High}

### 1.4 Preprocessing pipeline
Implemented in notebook `02_model_training.ipynb` as a scikit-learn `Pipeline`:

1. **One-hot encode** `programme`, `specialisation`, `gender`, `year_of_study`  
2. **Standard-scale** numeric features  
3. **Stratified train/test split** — 80% / 20%, `random_state=42`  
   - Train: 1,600 students  
   - Test: 400 students  

Exploratory analysis (`01_data_exploration.ipynb`) confirmed: no missing values, unique student IDs, roughly balanced classes, and expected links between attendance / averages and risk.

---

## 2. Modelling technique

The task is **multiclass classification**.

**Candidates compared** (same preprocess for fairness):
- Logistic Regression  
- Linear SVC  
- Random Forest  
- Gradient Boosting  

**Selection rule:** best **macro F1** on the held-out test set (treats Low / Medium / High equally).

**Selected model:** **Logistic Regression** (full preprocess + estimator pipeline).

**Saved artefacts:**
- `models/trained_model.pkl` — Pipeline (encoding + scaling + model)  
- `models/label_encoder.pkl` — `Low=0`, `Medium=1`, `High=2`

---

## 3. Evaluation results

Evaluation used the **same stratified 20% holdout** as training (`03_model_evaluation.ipynb`). Metrics below are from that test set (n = 400).

### 3.1 Overall metrics

| Metric | Value |
|--------|-------|
| Accuracy | **0.955** (95.5%) |
| Macro F1 | **0.956** |
| Weighted F1 | **0.955** |

### 3.2 Per-class performance

| Risk | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| Low | 0.953 | 0.946 | 0.949 | 149 |
| Medium | 0.919 | 0.947 | 0.932 | 131 |
| High | 1.000 | **0.975** | 0.987 | 120 |

**High-risk recall (0.975)** is especially important for interventions: only **3** High-risk students in the test set were missed (predicted as Medium).

### 3.3 Confusion matrix (rows = actual, columns = predicted)

|  | Pred Low | Pred Medium | Pred High |
|--|----------|-------------|-----------|
| **Actual Low** | 141 | 8 | 0 |
| **Actual Medium** | 7 | 124 | 0 |
| **Actual High** | 0 | 3 | 117 |

Most errors are **Low ↔ Medium** boundary cases. High risk is rarely confused with Low.

### 3.4 Interpretation
Performance is strong on this synthetic set because features were designed with realistic risk relationships. Results should be treated as a **credible baseline**, not as proof of performance on live Belgium Campus extracts. Re-evaluate when real data is available.

---

## 4. Limitations

1. **Synthetic data** — labels follow generation rules; real campus distributions may differ.  
2. **Medium class** — still the softest boundary (lowest F1 among the three).  
3. **Single train/test split** — no cross-validation; metrics have split-specific variance.  
4. **Decision support only** — outputs are risk indicators, not academic judgements or progression decisions.  
5. **Programme alone is weak** — intentional; risk is driven by engagement and performance signals.

---

## 5. Reproducibility for the team

```powershell
pip install -r requirements.txt
python src/data/generate_dataset.py
# Then Run All: notebooks/01 → 02 → 03
```

Keep `seed=42` so everyone regenerates the same synthetic CSV.
