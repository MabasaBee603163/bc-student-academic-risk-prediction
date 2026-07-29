# Dataset Dictionary

Anonymised synthetic Belgium Campus–style student records for academic risk prediction.

**File:** `data/synthetic/students.csv`  
**Generator:** `src/data/generate_dataset.py` (`seed=42`, default 2,000 rows)

---

## Columns

| Column | Type | Allowed / range | Definition | In model? |
|--------|------|-----------------|------------|-----------|
| `student_id` | string | `STU00001` … | Anonymised student ID | No (ID only) |
| `profile` | string | thriving, average, struggling, disengaged | Generation helper profile | No (leakage) |
| `age` | int | ~17–28 | Student age | Yes |
| `gender` | string | Female, Male, Non-binary, Prefer not to say | Demographic | Yes |
| `programme` | string | See handoff programme list | Qualification | Yes (context) |
| `specialisation` | string | Depends on programme | Stream within programme | Yes (context) |
| `year_of_study` | string | First Year … Fourth Year | Study level label | Yes |
| `attendance` | int | 0–100 | Attendance percentage | Yes (key) |
| `assignment_completion` | int | 0–100 | % of assignments completed | Yes (key) |
| `bc_connect_activity` | int | ≥ 0 | BC Connect engagement intensity | Yes (key) |
| `missed_assessments` | int | ≥ 0 | Count of missed assessments | Yes (key) |
| `overall_average` | float | 0–100 | Overall mark % | Yes |
| `midyear_average` | float | 0–100 | Mid-year assessment average % | Yes (key) |
| `test_average` | float | 0–100 | Test average % | Yes (key) |
| `assignment_average` | float | 0–100 | Assignment mark average % | Yes |
| `practical_average` | float | 0–100 | Practical mark average % | Yes |
| `failed_modules` | int | ≥ 0 | Failed modules count | Yes (key) |
| `registered_modules` | int | typically 4–6 | Modules registered | Yes |
| `passed_modules` | int | ≥ 0 | Modules passed | Yes |
| `risk_score` | float | 0–100 | Internal continuous risk (generator) | No (leakage) |
| `risk_label` | string | Low, Medium, High | **Target** risk class | Target |

---

## Target class balance (seed 42, n=2000)

Approximate mix: Low / Medium / High are intentionally near-balanced for training stability. Exact counts appear when you regenerate or open notebook 01.
