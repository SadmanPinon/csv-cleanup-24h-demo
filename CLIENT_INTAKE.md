# Client Intake - 24-Hour CSV Cleanup

Use this checklist before accepting a fixed-scope CSV cleanup job. It keeps the
work small enough to finish quickly and avoids private or regulated data.

## Fixed Scope

- One CSV file
- Up to 5,000 rows
- Standard cleanup, deduplication, validation flags, and a short report
- One revision for missed cleanup rules or formatting issues
- 24-hour delivery after the file and rules are received

## Client Should Provide

```text
1. The CSV file.
2. The columns that must appear in the final output.
3. Any non-sensitive validation rules.
4. The tool or workflow the cleaned CSV will be imported into.
5. Whether duplicate detection should use email, phone, company/name, or another column.
```

## Client Should Not Provide

- Passwords
- API keys
- SSNs or government IDs
- Medical records
- Bank or payment card data
- Private account exports
- Confidential employee, legal, or HR files

## Deliverables

- Cleaned CSV ready to import
- Duplicate/removal count
- Invalid email and missing-field flags
- Simple categories or source labels when useful
- Short Markdown quality report

## Acceptance Criteria

- The output file opens as valid CSV.
- Required columns are present.
- Duplicate rows identified by the agreed rule are removed or flagged.
- Invalid or missing required values are flagged, not silently deleted.
- The quality report includes input row count, exported row count, duplicate
  count, invalid email count, and missing required field count.

## Out Of Scope Unless Repriced

- More than 5,000 rows
- Multiple files or multi-table joins
- Web scraping
- Login-required systems
- Custom dashboards
- Sensitive or regulated data
- Manual research for every row
