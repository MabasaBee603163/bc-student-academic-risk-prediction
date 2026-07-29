# BC Student Academic Risk Prediction

Belgium Campus–style project that predicts a student’s **academic risk** as **Low**, **Medium**, or **High** from anonymised educational features (attendance, assignment completion, test/midyear averages, BC Connect activity, missed assessments, failed modules, and related fields).

This is a **decision-support** tool for staff awareness not a final academic judgement about students.

---

## What’s included (Role 1)


| Area                      | Location                              |
| ------------------------- | ------------------------------------- |
| Synthetic data generator  | `src/data/generate_dataset.py`        |
| EDA notebook              | `notebooks/01_data_exploration.ipynb` |
| Training notebook         | `notebooks/02_model_training.ipynb`   |
| Evaluation notebook       | `notebooks/03_model_evaluation.ipynb` |
| Trained model             | `models/trained_model.pkl`            |
| Label encoder             | `models/label_encoder.pkl`            |
| Model Dev & Eval write-up | `reports/evaluation_results.md`       |
| Short model notes         | `reports/model_notes.md`              |
| Role 2 handoff            | `docs/role2_info.md`                  |
| Dataset dictionary        | `docs/dataset_dictionary.md`          |


---

## Setup

```powershell
git clone https://github.com/MabasaBee603163/bc-student-academic-risk-prediction.git
cd bc-student-academic-risk-prediction
git checkout main
git pull
pip install -r requirements.txt
```

Use Python 3.11+ (developed with 3.13). If `pip` is not recognised on Windows:

```powershell
python -m pip install -r requirements.txt
```

---

## Generate the dataset

The CSV is **not** in git (gitignored). Everyone regenerates it locally with the same seed (`42`) so results stay aligned:

```powershell
python src/data/generate_dataset.py
```

Output: `data/synthetic/students.csv` (2,000 anonymised students).

---

## Run the notebooks

Open the project in Cursor / VS Code, select your Python kernel, then **Run All** in order:

1. `notebooks/01_data_exploration.ipynb` — EDA
2. `notebooks/02_model_training.ipynb` — train & save model (overwrites `models/*.pkl`)
3. `notebooks/03_model_evaluation.ipynb` — metrics & confusion matrix

**Who needs to run what?**


| Role                   | Generate CSV               | Run notebooks                                      |
| ---------------------- | -------------------------- | -------------------------------------------------- |
| Role 1 (ML)            | Yes                        | Yes (01 - 02 - 03) to verify / retrain             |
| Role 2 (AI Integrator) | Optional (for sample rows) | Optional - use saved `.pkl` + `docs/role2_info.md` |
| Role 3 (Front-end)     | Optional                   | No - consume Role 2 API                            |
| Role 4 (Lead)          | Optional                   | Optional - review `reports/`                       |


---

## For Role 2 (conversational layer)

Start here: `**[docs/role2_info.md](docs/role2_info.md)`**

That doc covers:

- How to load `trained_model.pkl` / `label_encoder.pkl`
- Required input columns and types
- Output labels (`Low` / `Medium` / `High`)
- What the assistant must / must not invent

Field definitions: `[docs/dataset_dictionary.md](docs/dataset_dictionary.md)`

---

## Project layout

```
bc-student-academic-risk-prediction/
├── data/synthetic/          # students.csv (generated locally)
├── docs/                    # handoff + dictionary
├── models/                  # trained_model.pkl, label_encoder.pkl
├── notebooks/               # 01 EDA, 02 train, 03 evaluate
├── reports/                 # evaluation write-up + notes
├── src/data/generate_dataset.py
└── requirements.txt
```

---

## Team roles (brief)

1. **ML Engineer** — dataset, model, evaluation, handoff docs *(this repo state)*
2. **AI Integrator** — Gemini / conversational layer grounded on model I/O
3. **Front-end** — simple web UI + demo video
4. **Project lead** — scope, persona, final report compilation

---

## Notes

- Keep generator seed **42** unless the whole team agrees to change it.

