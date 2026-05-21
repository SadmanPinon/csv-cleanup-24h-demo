# 24-Hour CSV Cleanup + Categorization Demo

This folder is safe to publish as a public portfolio sample for the fixed-scope
CSV cleanup offer. It does not contain personal contact details, payment links,
API keys, private credentials, or client data.

## Files

- `index.html` - static service/demo page.
- `clean_report.py` - runnable cleanup script.
- `samples/messy_leads.csv` - synthetic messy CSV input.
- `out/clean_leads.csv` - cleaned sample output.
- `out/report.md` - sample quality and category report.
- `out/service-page-desktop.png` - desktop screenshot.
- `out/service-page-mobile.png` - mobile screenshot.
- `CLIENT_INTAKE.md` - buyer-facing scope, data boundary, and acceptance checklist.
- `LEAD_PILOT.md` - scope for the public business lead pilot offer.
- `samples/virginia-healthcare-wellness-public-sample.csv` - public-source
  healthcare/wellness lead pilot sample.

## Verify

```bash
python3 clean_report.py samples/messy_leads.csv out/clean_leads.csv out/report.md
```

Expected output:

```text
Cleaned 6 rows into 5 rows.
Report written to out/report.md
```

Lead pilot sample check:

```bash
python3 - <<'PY'
import csv
from pathlib import Path
rows = list(csv.DictReader(Path("samples/virginia-healthcare-wellness-public-sample.csv").open()))
print(len(rows), sorted(rows[0]))
PY
```

## Posting Boundary

Use the public demo link only as proof of work. Keep payment details in private
messages or platform payout fields. Do not publish personal email, PayPal links,
phone numbers, banking details, API keys, or private account exports.
