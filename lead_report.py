#!/usr/bin/env python3
import csv
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_COLUMNS = [
    "business_name",
    "category",
    "region",
    "phone",
    "address",
    "website",
    "public_email",
    "source_url",
    "qa_note",
]


REQUIRED_VALUES = [
    "business_name",
    "category",
    "region",
    "phone",
    "address",
    "website",
    "source_url",
    "qa_note",
]


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_key(row):
    name = re.sub(r"[^a-z0-9]+", "", row.get("business_name", "").lower())
    phone = re.sub(r"\D+", "", row.get("phone", ""))
    website_host = urlparse(row.get("website", "")).netloc.lower().removeprefix("www.")
    return name, phone, website_host


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    fieldnames = reader.fieldnames or []
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    return rows, missing_columns


def build_report(rows, missing_columns):
    missing_values = []
    invalid_emails = []
    duplicate_keys = []
    seen = {}
    source_hosts = Counter()

    for index, row in enumerate(rows, start=2):
        for column in REQUIRED_VALUES:
            if not row.get(column, "").strip():
                missing_values.append((index, column))

        email = row.get("public_email", "").strip()
        if email and not EMAIL_RE.match(email):
            invalid_emails.append((index, email))

        key = normalize_key(row)
        if key in seen:
            duplicate_keys.append((seen[key], index, row.get("business_name", "")))
        else:
            seen[key] = index

        source_host = urlparse(row.get("source_url", "")).netloc.lower().removeprefix("www.")
        if source_host:
            source_hosts[source_host] += 1

    categories = Counter(row.get("category", "") for row in rows)
    regions = Counter(row.get("region", "") for row in rows)
    emails_available = sum(1 for row in rows if row.get("public_email", "").strip())

    lines = [
        "# Public Lead QA Report",
        "",
        f"- Rows checked: {len(rows)}",
        f"- Required columns missing: {len(missing_columns)}",
        f"- Required value gaps: {len(missing_values)}",
        f"- Duplicate business keys: {len(duplicate_keys)}",
        f"- Invalid public emails: {len(invalid_emails)}",
        f"- Rows with public/general email: {emails_available}",
        f"- Unique source domains: {len(source_hosts)}",
        "",
        "## Category Counts",
        "",
    ]

    for category, count in categories.most_common():
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Region Counts", ""])

    for region, count in regions.most_common():
        lines.append(f"- {region}: {count}")

    lines.extend(["", "## Source Domains", ""])

    for host, count in source_hosts.most_common():
        lines.append(f"- {host}: {count}")

    if missing_columns or missing_values or duplicate_keys or invalid_emails:
        lines.extend(["", "## Review Items", ""])
        for column in missing_columns:
            lines.append(f"- Missing required column: {column}")
        for row_number, column in missing_values:
            lines.append(f"- Row {row_number}: missing {column}")
        for first_row, second_row, name in duplicate_keys:
            lines.append(f"- Rows {first_row} and {second_row}: possible duplicate for {name}")
        for row_number, email in invalid_emails:
            lines.append(f"- Row {row_number}: invalid email `{email}`")
    else:
        lines.extend(["", "## Review Items", "", "- None."])

    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) != 3:
        print("Usage: lead_report.py input.csv output.md", file=sys.stderr)
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])
    rows, missing_columns = load_rows(input_path)
    output_path.write_text(build_report(rows, missing_columns), encoding="utf-8")
    print(f"Checked {len(rows)} public lead rows.")
    print(f"Report written to {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
