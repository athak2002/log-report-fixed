# Log Report

Analyze the Apache-style access log at `/app/access.log` and produce a JSON summary report.

## Success Criteria

1. Parse every line in `/app/access.log`.
2. Write a valid JSON file to `/app/report.json` with exactly these keys:
   - `"total_requests"` — integer count of all log lines.
   - `"unique_ips"` — integer count of distinct client IP addresses.
   - `"top_path"` — string of the most frequently requested URL path.
3. The file must be valid JSON and contain correct values.
