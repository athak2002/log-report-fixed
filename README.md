# 🛠️ Log-Report Harbor Task Repair

[![Harbor Version](https://img.shields.io/badge/harbor-0.18.0-blue.svg)](https://github.com/continual-ai/harbor)
[![Python Version](https://img.shields.io/badge/python-3.12--slim-blue.svg)](https://www.python.org/)
[![Docker Pinned](https://img.shields.io/badge/docker-pinned-brightgreen.svg)](https://www.docker.com/)

A fully repaired and optimized Harbor (Terminal-Bench 2) task configuration for the `dynamo/log-report` task. This task tests an agent's ability to parse an Apache-style access log and generate a structured JSON report summarizing the requests.

This repository features pinned base images, a robust verifier, cleaned environment dependencies, and clear instruction sets aligned with Harbor task requirements.

---

## 📋 Task Specification

The task instruction is designed to guide an agent to:
1. Parse every request line in `/app/access.log`.
2. Generate a valid JSON report at `/app/report.json`.
3. Include the following precise keys and correct statistics:
   - `total_requests`: Total request count (**6**)
   - `unique_ips`: Count of unique client IP addresses (**3**)
   - `top_path`: The most frequently accessed request path (**`/index.html`**)

---

## 🔍 Defects Identified & Fixed

| Category | Defect Description | Impact | Resolution |
| :--- | :--- | :--- | :--- |
| **Format** | `artifacts` in `task.toml` was a string pointing to a wrong path (`/app/out.json`). | Silently failed Harbor's validation schema (interpreting the task directory as a dataset). | Corrected to an array containing the correct target output: `["/app/report.json"]`. |
| **Environment** | The base Docker image was unpinned (`FROM python:latest`). | Non-reproducible environment builds that break over time. | Pinned the base image using a secure, digest-locked tag: `python:3.12-slim@sha256:c3d81d2...`. |
| **Environment** | Reference solution (`solution_hint.py`) leaked in the agent container. | Cheatable task environment where agents could run the hint script directly. | Deleted `solution_hint.py` from the environment and Dockerfile completely. |
| **Verifier** | Assertion check only validated file existence and non-emptiness. | Permissive testing allowing incorrect or dummy outputs to get a perfect reward. | Rewrote `test_outputs.py` to validate JSON formatting, key presence, and correct numeric/string values. |
| **Verifier** | Reward path written to `/app/reward.txt` instead of `/logs/verifier/reward.txt`. | Harbor failed to discover evaluation results, raising `RewardFileNotFoundError`. | Updated `test.sh` to produce a CTRF report and write final reward scoring directly to the expected log directory. |
| **Verifier** | Loose exit code checks on pytest inside `test.sh`. | Potential for shell errors to swallow failure results. | Added strict bash flags (`set -uo pipefail`) and stored pytest's exit status explicitly (`rc=$?`). |
| **Instruction** | `instruction.md` was ambiguous with no concrete success criteria. | Poor developer/agent clarity regarding keys, types, and files to create. | Rewrote the instruction file to include structured, numbered success criteria. |

---

## 🚀 Execution & Verification

To verify the task setup, you can execute the Harbor run harness on your local system:

### 1. Verification of the Reference Solution (Oracle)
Ensures that the task can be successfully solved and verified:
```bash
harbor run -p . -a oracle
```
* **Expected Output:**
  ```text
  adhoc • oracle
  ┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┓
  ┃ Trials ┃ Exceptions ┃  Mean ┃
  ┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━┩
  │      1 │          0 │ 1.000 │
  └────────┴────────────┴───────┘

  ┏━━━━━━━━┳━━━━━━━┓
  ┃ Reward ┃ Count ┃
  ┡━━━━━━━━╇━━━━━━━┩
  │ 1.0    │     1 │
  └────────┴───────┘
  ```

### 2. Verification of a Non-functional Solution (Nop Agent)
Ensures that the verifier correctly rejects incorrect or empty solutions (preventing false passes):
```bash
harbor run -p . --agent nop
```
* **Expected Output:**
  ```text
  adhoc • nop
  ┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┓
  ┃ Trials ┃ Exceptions ┃  Mean ┃
  ┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━┩
  │      1 │          0 │ 0.000 │
  └────────┴────────────┴───────┘

  ┏━━━━━━━━┳━━━━━━━┓
  ┃ Reward ┃ Count ┃
  ┡━━━━━━━━╇━━━━━━━┩
  │ 0.0    │     1 │
  └────────┴───────┘
  ```

---

## 📂 Repository File Structure

```directory
.
├── README.md               <-- Repair documentation and info
├── task.toml               <-- Pinned task config & metadata
├── instruction.md          <-- Precise, numbered success criteria
├── environment/
│   ├── Dockerfile          <-- Reproducible environment pinned by digest
│   └── access.log          <-- Raw HTTP request log input
├── solution/
│   ├── solve.py            <-- Reference python script
│   └── solve.sh            <-- Reference run shell script
└── tests/
    ├── test.sh             <-- Verifier entrypoint producing reward.txt & ctrf.json
    └── test_outputs.py     <-- Detailed validation tests (Pytest)
```
