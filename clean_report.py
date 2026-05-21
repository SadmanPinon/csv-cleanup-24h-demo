from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class CleanResult:
    rows_in: int
    rows_out: int
    duplicates_removed: int
    invalid_emails: int
    missing_required: int
    companies: Counter[str]
    categories: Counter[str]


def normalize_name(value: str) -> str:
    return " ".join(part.capitalize() for part in value.strip().split())


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value.strip()


def normalize_company(value: str) -> str:
    cleaned = " ".join(value.strip().split())
    small_words = {"and", "of", "the", "for"}
    words = []
    for idx, word in enumerate(cleaned.split()):
        lower = word.lower()
        words.append(lower if idx and lower in small_words else word.capitalize())
    return " ".join(words)


def classify_lead(row: dict[str, str]) -> str:
    source = row.get("source", "").lower()
    company = row.get("company", "").lower()

    if source == "referral":
        return "Referral"
    if source == "conference":
        return "Event lead"
    if "unknown" in company or source == "upload":
        return "Needs source review"
    if source == "web":
        return "Website inbound"
    return "General follow-up"


def clean_rows(input_path: Path, output_path: Path) -> CleanResult:
    with input_path.open(newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    required = {"name", "email"}
    seen: set[str] = set()
    cleaned_rows: list[dict[str, str]] = []
    invalid_emails = 0
    missing_required = 0
    companies: Counter[str] = Counter()
    categories: Counter[str] = Counter()

    for raw in rows:
        row = {key: (value or "").strip() for key, value in raw.items()}
        row["name"] = normalize_name(row.get("name", ""))
        row["email"] = normalize_email(row.get("email", ""))
        row["phone"] = normalize_phone(row.get("phone", ""))
        row["company"] = normalize_company(row.get("company", ""))
        row["lead_category"] = classify_lead(row)

        review_flags: list[str] = []
        if not required.issubset({key for key, value in row.items() if value}):
            missing_required += 1
            review_flags.append("missing_required")

        if row["email"] and not EMAIL_RE.match(row["email"]):
            invalid_emails += 1
            review_flags.append("invalid_email")
        row["needs_review"] = ";".join(review_flags)

        dedupe_key = row["email"] or row["phone"] or "|".join(row.values())
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        if row["company"]:
            companies[row["company"]] += 1
        categories[row["lead_category"]] += 1
        cleaned_rows.append(row)

    final_fields = list(dict.fromkeys([*fieldnames, "lead_category", "needs_review"]))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=final_fields)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    return CleanResult(
        rows_in=len(rows),
        rows_out=len(cleaned_rows),
        duplicates_removed=len(rows) - len(cleaned_rows),
        invalid_emails=invalid_emails,
        missing_required=missing_required,
        companies=companies,
        categories=categories,
    )


def write_report(result: CleanResult, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    top_companies = "\n".join(
        f"- {company}: {count}" for company, count in result.companies.most_common(5)
    )
    if not top_companies:
        top_companies = "- No company data present"
    category_mix = "\n".join(
        f"- {category}: {count}" for category, count in result.categories.most_common()
    )
    if not category_mix:
        category_mix = "- No category data present"

    report_path.write_text(
        "\n".join(
            [
                "# CSV Cleanup Report",
                "",
                f"- Input rows: {result.rows_in}",
                f"- Clean rows exported: {result.rows_out}",
                f"- Duplicates removed: {result.duplicates_removed}",
                f"- Invalid emails flagged: {result.invalid_emails}",
                f"- Rows missing required fields: {result.missing_required}",
                "",
                "## Top Companies",
                "",
                top_companies,
                "",
                "## Lead Categories",
                "",
                category_mix,
                "",
            ]
        )
    )


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: python3 clean_report.py INPUT.csv OUTPUT.csv REPORT.md",
            file=sys.stderr,
        )
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    report_path = Path(sys.argv[3])
    result = clean_rows(input_path, output_path)
    write_report(result, report_path)
    print(f"Cleaned {result.rows_in} rows into {result.rows_out} rows.")
    print(f"Report written to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
