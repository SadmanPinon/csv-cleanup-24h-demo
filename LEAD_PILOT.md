# Public Business Lead Pilot

Fixed-scope pilot: 100 Virginia healthcare, med spa, wellness, and
recovery-center business leads for `$99`.

## Deliverables

- Clean CSV with public business contact fields.
- Deduped business names and source URLs.
- QA note for each row.
- Short summary with counts by region and category.

## Fields

- Business name
- Category
- Region
- Phone
- Address
- Website
- Public/general office email when available
- Source URL
- QA note

## Data Boundary

Use public business contact information only. Do not collect patient data,
private medical information, private account data, personal contact enrichment,
login-only sources, restricted databases, spam lists, or anything requiring
credentials.

## Pilot Sample

Download the 9-row sample:

```text
samples/virginia-healthcare-wellness-public-sample.csv
```

Every sample row includes an official source URL and was checked for required
fields.

Sample QA report:

```text
out/lead-pilot-report.md
```
