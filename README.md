# Log Report Harbor Task (Fixed)

This repository contains the corrected and fully repaired Harbor (Terminal-Bench 2) task `dynamo/log-report`. The task requires parsing an Apache-style access log into a JSON summary report.

All defects have been resolved to make the task correct, reproducible, and graded honestly.

---

## 🔍 Defects Identified & Fixed

### 1. Format: Artifact Path Mismatch & Typo in `task.toml`
* **Issue:** `task.toml` declared `artifacts = "/app/out.json"` as a plain string. However, Harbor's validation schema expects a list, which caused validation to fail silently (making Harbor treat the task path as a dataset directory). Furthermore, the actual solution output file is `report.json`, not `out.json`.
* **Fix:** Corrected line 1 to `artifacts = ["/app/report.json"]`.

### 2. Environment: Docker Base Image Not Pinned by Digest
* **Issue:** `environment/Dockerfile` used `FROM python:latest`. This is non-reproducible because the `latest` tag updates dynamically over time, breaking task consistency.
* **Fix:** Changed the base image to a pinned, lightweight digest: `FROM python:3.12-slim@sha256:c3d81d25b3154142b0b42eb1e61300024426268edeb5b5a26dd7ddf64d9daf28`.

### 3. Environment: Leaked Solution Hint
* **Issue:** The reference implementation was leaked directly into the agent environment at `environment/solution_hint.py` and copied into the image. This allowed any agent to simply execute the hint to solve the task.
* **Fix:** Deleted `solution_hint.py` from the environment directory and removed the corresponding `COPY` command from the `Dockerfile`.

### 4. Verifier: Weak Verifier Assertions (Gameable)
* **Issue:** The original `tests/test_outputs.py` only checked if `/app/report.json` existed and was non-empty. An agent writing any dummy file (e.g., `echo "dummy" > /app/report.json`) would pass the task.
* **Fix:** Rewrote `tests/test_outputs.py` to validate correct JSON structure and precise parsed values:
  * `total_requests == 6`
  * `unique_ips == 3`
  * `top_path == "/index.html"`

### 5. Verifier: Incorrect Reward Location and Missing CTRF
* **Issue:** The verifier script (`tests/test.sh`) wrote the reward output to `/app/reward.txt` instead of `/logs/verifier/reward.txt`. Additionally, it did not output `ctrf.json`, preventing Harbor from finding and validating the trial outcomes.
* **Fix:** Updated `tests/test.sh` to output the test execution results via CTRF to `/logs/verifier/ctrf.json` and output the final reward to `/logs/verifier/reward.txt`.

### 6. Instruction: Ambiguous Success Criteria
* **Issue:** `instruction.md` was a vague paragraph that didn't document file paths, format requirements, or target keys.
* **Fix:** Rewrote `instruction.md` with structured, numbered success criteria that correspond exactly to the verifier's test cases.

---

## 🚀 How to Run & Verify

Make sure you have Docker and the `harbor` CLI installed and configured.

### 1. Run the Oracle (Reference Solution)
To verify the task compiles and is solvable by the reference agent:
```bash
harbor run -p . -a oracle
```
**Expected Outcome:** `Mean: 1.000` (PASS, reward = 1)

### 2. Run the No-Op Agent (Nop)
To verify that the verifier correctly rejects empty/non-working solutions:
```bash
harbor run -p . --agent nop
```
**Expected Outcome:** `Mean: 0.000` (FAIL, reward = 0)
