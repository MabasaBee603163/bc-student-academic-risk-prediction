"""Generate synthetic Belgium Campus–style student records for academic risk modeling."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from src.utils.config import DATA_DIR
except ModuleNotFoundError:  # pragma: no cover - script / flat import fallback
    DATA_DIR = Path(__file__).resolve().parents[2] / "data"

DEFAULT_SEED = 42
DEFAULT_N_STUDENTS = 2000
OUTPUT_PATH = DATA_DIR / "synthetic" / "students.csv"

# Belgium Campus programmes and specialisations
PROGRAMME_SPECIALISATIONS: dict[str, list[str]] = {
    "Bachelor of Information Technology": [
        "Software Development",
        "Data Science",
        "Cloud Computing",
        "Cybersecurity",
        "Network Engineering",
    ],
    "Bachelor of Computing": [
        "Software Engineering",
        "Artificial Intelligence",
    ],
    "Diploma in Information Technology": [
        "Network Engineering",
        "Software Development",
        "Cybersecurity",
    ],
    "Higher Certificate in Information Systems": [
        "Information Systems",
        "End-User Computing",
        "Systems Support",
    ],
}

YEAR_OF_STUDY = [
    "First Year",
    "Second Year",
    "Third Year",
    "Fourth Year",
]

# Qualification length limits year options
PROGRAMME_YEARS: dict[str, list[str]] = {
    "Bachelor of Information Technology": YEAR_OF_STUDY,
    "Bachelor of Computing": YEAR_OF_STUDY,
    "Diploma in Information Technology": ["First Year", "Second Year", "Third Year"],
    "Higher Certificate in Information Systems": ["First Year"],
}

GENDERS = ["Female", "Male", "Non-binary", "Prefer not to say"]

# Profile priors — strong predictors for academic risk (BC-style %).
PROFILES: dict[str, dict[str, Any]] = {
    "thriving": {
        "weight": 0.30,
        "attendance": (88, 99),
        "assignment_completion": (90, 100),
        "midyear_average": (78, 95),
        "test_average": (80, 96),
        "assignment_average": (82, 97),
        "practical_average": (82, 98),
        "bc_connect_activity": (12, 25),
        "missed_assessments": (0, 0),
        "failed_modules": (0, 0),
        "registered_modules": (4, 5),
    },
    "average": {
        "weight": 0.40,
        "attendance": (72, 90),
        "assignment_completion": (70, 90),
        "midyear_average": (58, 75),
        "test_average": (60, 78),
        "assignment_average": (60, 78),
        "practical_average": (62, 80),
        "bc_connect_activity": (5, 14),
        "missed_assessments": (0, 2),
        "failed_modules": (0, 1),
        "registered_modules": (4, 6),
    },
    "struggling": {
        "weight": 0.20,
        "attendance": (50, 75),
        "assignment_completion": (45, 72),
        "midyear_average": (40, 58),
        "test_average": (42, 60),
        "assignment_average": (42, 60),
        "practical_average": (45, 62),
        "bc_connect_activity": (1, 7),
        "missed_assessments": (2, 5),
        "failed_modules": (1, 3),
        "registered_modules": (5, 6),
    },
    "disengaged": {
        "weight": 0.10,
        "attendance": (25, 55),
        "assignment_completion": (25, 55),
        "midyear_average": (28, 48),
        "test_average": (30, 50),
        "assignment_average": (30, 50),
        "practical_average": (32, 52),
        "bc_connect_activity": (0, 3),
        "missed_assessments": (4, 8),
        "failed_modules": (2, 4),
        "registered_modules": (5, 6),
    },
}


def _uniform(low: float, high: float) -> float:
    return float(np.random.uniform(low, high))


def _randint(low: int, high: int) -> int:
    """Inclusive integer draw."""
    return int(np.random.randint(low, high + 1))


def generate_student_id(index: int) -> str:
    """Return a stable, unique anonymised student identifier."""
    return f"STU{index:05d}"


def choose_profile() -> str:
    """Sample a behavioral/academic profile using configured priors."""
    names = list(PROFILES.keys())
    weights = [PROFILES[name]["weight"] for name in names]
    return str(np.random.choice(names, p=weights))


def choose_programme_and_specialisation() -> tuple[str, str]:
    """Sample a Belgium Campus programme and one of its specialisations."""
    programme = random.choice(list(PROGRAMME_SPECIALISATIONS.keys()))
    specialisation = random.choice(PROGRAMME_SPECIALISATIONS[programme])
    return programme, specialisation


def generate_demographics(profile: str) -> dict[str, Any]:
    """Generate anonymised student information (no names)."""
    programme, specialisation = choose_programme_and_specialisation()
    year_options = PROGRAMME_YEARS[programme]

    # At-risk profiles skew earlier in the qualification
    if profile in {"struggling", "disengaged"}:
        age = _randint(17, 22)
        year_of_study = year_options[0] if len(year_options) == 1 else random.choice(year_options[:2])
    else:
        age = _randint(18, 28)
        year_of_study = random.choice(year_options)

    return {
        "age": age,
        "gender": random.choice(GENDERS),
        "programme": programme,
        "specialisation": specialisation,
        "year_of_study": year_of_study,
    }


def generate_engagement(profile: str) -> dict[str, Any]:
    """Generate engagement predictors (attendance, BC Connect, submissions)."""
    cfg = PROFILES[profile]
    attendance = int(np.clip(round(_uniform(*cfg["attendance"])), 0, 100))
    assignment_completion = int(np.clip(round(_uniform(*cfg["assignment_completion"])), 0, 100))
    bc_connect_activity = _randint(*cfg["bc_connect_activity"])
    missed_assessments = _randint(*cfg["missed_assessments"])

    return {
        "attendance": attendance,
        "assignment_completion": assignment_completion,
        "bc_connect_activity": bc_connect_activity,
        "missed_assessments": missed_assessments,
    }


def generate_academics(profile: str) -> dict[str, Any]:
    """Generate SA / Belgium Campus academic performance (percent averages + modules)."""
    cfg = PROFILES[profile]

    midyear_average = round(_uniform(*cfg["midyear_average"]), 1)
    test_average = round(_uniform(*cfg["test_average"]), 1)
    assignment_average = round(_uniform(*cfg["assignment_average"]), 1)
    practical_average = round(_uniform(*cfg["practical_average"]), 1)

    overall_average = (
        0.30 * midyear_average
        + 0.25 * test_average
        + 0.25 * assignment_average
        + 0.20 * practical_average
        + float(np.random.normal(0.0, 2.0))
    )
    overall_average = round(float(np.clip(overall_average, 0.0, 100.0)), 1)

    registered_modules = _randint(*cfg["registered_modules"])
    failed_modules = min(_randint(*cfg["failed_modules"]), registered_modules)
    passed_modules = max(0, registered_modules - failed_modules)

    return {
        "overall_average": overall_average,
        "midyear_average": midyear_average,
        "test_average": test_average,
        "assignment_average": assignment_average,
        "practical_average": practical_average,
        "failed_modules": failed_modules,
        "registered_modules": registered_modules,
        "passed_modules": passed_modules,
    }


def calculate_risk(
    demographics: dict[str, Any],
    engagement: dict[str, Any],
    academics: dict[str, Any],
) -> dict[str, Any]:
    """
    Derive risk from the main academic-risk predictors.

    Programme/specialisation are context only — risk is driven by engagement
    and performance signals.
    """
    score = 0.0

    # Core predictors
    score += (100.0 - engagement["attendance"]) * 0.28
    score += (100.0 - engagement["assignment_completion"]) * 0.22
    score += (100.0 - academics["test_average"]) * 0.18
    score += (100.0 - academics["midyear_average"]) * 0.12
    score += max(0, 10 - engagement["bc_connect_activity"]) * 1.8
    score += engagement["missed_assessments"] * 4.5
    score += academics["failed_modules"] * 9.0

    score += (100.0 - academics["overall_average"]) * 0.10

    if academics["registered_modules"] > 0:
        pass_ratio = academics["passed_modules"] / academics["registered_modules"]
        score += (1.0 - pass_ratio) * 12.0

    if demographics["year_of_study"] == "First Year":
        score += 2.0

    score += float(np.random.normal(0.0, 3.0))
    score = float(np.clip(score, 0.0, 100.0))

    if score < 28:
        label = "Low"
    elif score < 55:
        label = "Medium"
    else:
        label = "High"

    return {
        "risk_score": round(score, 2),
        "risk_label": label,
    }


def generate_student(index: int) -> dict[str, Any]:
    """Compose one full anonymised student record."""
    profile = choose_profile()
    demographics = generate_demographics(profile)
    engagement = generate_engagement(profile)
    academics = generate_academics(profile)
    risk = calculate_risk(demographics, engagement, academics)

    return {
        "student_id": generate_student_id(index),
        "profile": profile,
        **demographics,
        **engagement,
        **academics,
        **risk,
    }


def main(
    n_students: int = DEFAULT_N_STUDENTS,
    seed: int = DEFAULT_SEED,
    output_path: Path | None = None,
) -> Path:
    """Generate a synthetic student dataset and write it to CSV."""
    output = Path(output_path) if output_path else OUTPUT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)

    random.seed(seed)
    np.random.seed(seed)

    records = [generate_student(i + 1) for i in range(n_students)]
    df = pd.DataFrame(records)
    df.to_csv(output, index=False)

    label_counts = df["risk_label"].value_counts().to_dict()
    print(f"Generated {len(df)} students -> {output}")
    print(f"Risk label distribution: {label_counts}")
    print(f"Programmes: {sorted(df['programme'].unique().tolist())}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic student risk data.")
    parser.add_argument("-n", "--n-students", type=int, default=DEFAULT_N_STUDENTS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="Output CSV path (default: data/synthetic/students.csv)",
    )
    args = parser.parse_args()
    main(n_students=args.n_students, seed=args.seed, output_path=args.output)
