# Model Notes

## Choice summary
- **Task:** Multiclass academic risk (`Low` / `Medium` / `High`)
- **Winner:** Logistic Regression (by test macro F1)
- **Why shortlist several models:** Avoid locking into one algorithm before comparing a linear baseline, SVC, and tree ensembles
- **Why macro F1:** Balances all risk classes; High recall remains a key secondary check for support use-cases

## Experiments (notebook 02)
Compared Logistic Regression, Linear SVC, Random Forest, and Gradient Boosting under an identical preprocessing pipeline (one-hot categoricals + scaled numerics + stratified 80/20 split).

## Design decisions
- SA / Belgium Campus **percentage marks** (`overall_average`, `midyear_average`, `test_average`) instead of GPA  
- `programme` + `specialisation` as context; risk logic emphasises attendance, completion, BC Connect, missed assessments, failed modules  
- Drop `profile` and `risk_score` at train time to avoid leakage  

## Limitations to remember in the report / UI copy
- Synthetic data  
- Not a final academic decision engine  
- Re-validate on real campus data before operational use  

Full write-up: `reports/evaluation_results.md`  
Handoff for Role 2: `docs/model_handoff.md`
