# Model Handoff (Role 1 → Role 2)

This document tells the **AI Integrator** how to load the model, what inputs to send, what outputs to expect, and what the conversational layer **must not invent**.

---

## 1. Artefacts

| File | Purpose |
|------|---------|
| `models/trained_model.pkl` | Full scikit-learn **Pipeline** (preprocess + classifier) |
| `models/label_encoder.pkl` | Maps integers ↔ risk labels |
| `data/synthetic/students.csv` | Example data (generate locally; gitignored) |
| `src/data/generate_dataset.py` | Regenerates CSV with `seed=42` |

**Estimator currently saved:** Logistic Regression inside the pipeline.

**Label encoding:**
| Integer | Label |
|---------|-------|
| 0 | Low |
| 1 | Medium |
| 2 | High |

---

## 2. How to load and predict

```python
import joblib
import pandas as pd

model = joblib.load("models/trained_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# X = DataFrame with the feature columns listed below (same names/types)
pred_ids = model.predict(X)
pred_labels = label_encoder.inverse_transform(pred_ids)
# pred_labels[i] is "Low" | "Medium" | "High"
```

Do **not** re-implement encoding/scaling yourself — it is inside `trained_model.pkl`.

---

## 3. Expected input format

One row = one student. Column names must match exactly.

### Required feature columns (model input)

| Column | Type | Notes / example |
|--------|------|-----------------|
| `age` | int | e.g. 18–28 |
| `gender` | string | `Female`, `Male`, `Non-binary`, `Prefer not to say` |
| `programme` | string | See programmes list below |
| `specialisation` | string | Must belong to that programme |
| `year_of_study` | string | `First Year`, `Second Year`, `Third Year`, `Fourth Year` |
| `attendance` | int | 0–100 (display as `84%`) |
| `assignment_completion` | int | 0–100 (%) |
| `bc_connect_activity` | int | Activity count / intensity |
| `missed_assessments` | int | Count |
| `overall_average` | float | 0–100 (%) |
| `midyear_average` | float | 0–100 (%) |
| `test_average` | float | 0–100 (%) |
| `assignment_average` | float | 0–100 (%) |
| `practical_average` | float | 0–100 (%) |
| `failed_modules` | int | Count |
| `registered_modules` | int | Typically 4–6 |
| `passed_modules` | int | Count |

### Do **not** pass to `predict`
- `student_id` (optional to keep for UI display only)
- `profile`
- `risk_score`
- `risk_label` (this is what we predict)

### Programmes and specialisations

| Programme | Specialisations |
|-----------|-----------------|
| Bachelor of Information Technology | Software Development, Data Science, Cloud Computing, Cybersecurity, Network Engineering |
| Bachelor of Computing | Software Engineering, Artificial Intelligence |
| Diploma in Information Technology | Network Engineering, Software Development, Cybersecurity |
| Higher Certificate in Information Systems | Information Systems, End-User Computing, Systems Support |

---

## 4. Expected output format

| Field | Values |
|-------|--------|
| `risk_label` | `Low` \| `Medium` \| `High` |

Optional for the assistant (not from the model file directly):
- You may also show the input feature values you used (attendance, missed assessments, etc.) when explaining **why** a prediction is plausible.
- Do **not** invent a `risk_score` unless you compute something separately and label it clearly as non-model output.

---

## 5. What the model is good at explaining

Safe explanation themes (grounded in features Role 1 designed as predictors):
- Low **attendance**
- Low **assignment_completion**
- Weak **test_average** / **midyear_average** / **overall_average**
- Low **bc_connect_activity**
- High **missed_assessments**
- High **failed_modules**

Programme / specialisation are **context**, not the main risk driver.

---

## 6. Constraint management for the conversational layer (Role 2)

**Must**
- Treat model output as advisory only — not a final academic decision  
- Stick to provided features + predicted label  
- Stay within free-tier API limits (short prompts, cache where possible)

**Must not**
- Invent student history, grades, or incidents not in the input  
- Claim the model “failed” or “will exclude” a student  
- Override or hide the predicted label with speculative narrative  
- Pretend live Belgium Campus data was used (dataset is synthetic unless replaced later)

**Suggested reply pattern**
1. State predicted risk: Low / Medium / High  
2. Point to 2–4 concrete input signals (e.g. attendance 52%, 3 missed assessments)  
3. Reminder: support tool for staff awareness, not an official academic judgement  

---

## 7. Regenerating data / retraining (if Role 2 needs fresh artefacts)

```powershell
pip install -r requirements.txt
python src/data/generate_dataset.py
# Run notebooks 02 then 03 to refresh models/*.pkl and metrics
```

Keep seed **42** so the group stays aligned.

---

## 8. Contact / ownership

- **Role 1** owns: dataset generator, training, evaluation, `.pkl` artefacts, this handoff  
- **Role 2** owns: Gemini/Firebase conversational layer, prompts, API hooks for Role 3  
- Full evaluation narrative: `reports/evaluation_results.md`  
- Field definitions: `docs/dataset_dictionary.md`
