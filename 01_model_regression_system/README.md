# Model Regression Detection System

> Catches LLM drift before it hits users.

Production-grade regression detection that runs LLM-as-judge tests on every PR, tracks semantic drift across 50+ prompt templates with statistical significance testing, and integrates NVIDIA NIM free-tier inference for classification.

**Part of [AEGIS](https://github.com/KnigguKniggu-droid/AEGIS)** — Adaptive AI Governance Infrastructure for Cyber-Physical Systems. This subsystem maps to **L5: Adaptive Control** (Statistical Process Control (SPC) — CUSUM and z-score monitoring on model outputs, identical to control charts used in semiconductor fabrication.).

---

## Architecture Position

```
AEGIS Layer: L5: Adaptive Control
ECE Mapping: Statistical Process Control (SPC) — CUSUM and z-score monitoring on model outputs, identical to control charts used in semiconductor fabrication.
```

This module is one of 15 subsystems in the AEGIS platform. See the [unified architecture](https://github.com/KnigguKniggu-droid/AEGIS#readme) for how all components interconnect.

---

## Features

- LLM-as-judge regression tests on every PR via GitHub Actions
- Semantic drift tracking across 50+ prompt templates
- NVIDIA NIM free-tier + paid Nemotron 3 Ultra classification
- SQLite/PostgreSQL schema with typed Pydantic contracts
- Streamlit dashboard for run regressions, compare model versions, inspect drift reports

---

## Tech Stack

`Python` | `FastAPI` | `PyTest` | `SQLite` | `PostgreSQL` | `Docker` | `GitHub Actions` | `NVIDIA NIM` | `Streamlit` | `k6`

---

## Quick Start

```bash
git clone https://github.com/KnigguKniggu-droid/01-model-regression-system.git
cd 01-model-regression-system
pip install -e .
```

Run tests:

```bash
pytest tests/ -v
```

---

## Project Structure

```
01_model_regression_system/
  src/                  # Core application code
  tests/                # 12 passing tests
  .github/              # CI/CD workflows
  Dockerfile            # Container build
  pyproject.toml        # Package configuration
```

---

## Running in Docker

```bash
docker build -t 01_model_regression_system .
docker run -p 8000:8000 01_model_regression_system
```

---

## ECE Design Principles

This subsystem is modeled after classical electrical and computer engineering concepts:

> **Statistical Process Control (SPC) — CUSUM and z-score monitoring on model outputs, identical to control charts used in semiconductor fabrication.**

The AEGIS platform applies safety-critical engineering principles from integrated circuit design to LLM deployment, ensuring production reliability in autonomous vehicles, power grids, and medical devices.

---

## Related Projects

All 15 AEGIS subsystems:

| # | Project | Layer | ECE Mapping |
|---|---------|-------|-------------|
| 01 | [Model Regression Detection](https://github.com/KnigguKniggu-droid/AEGIS) | L5 | SPC |
| 02 | [LLM Cost Autopilot](https://github.com/KnigguKniggu-droid/AEGIS) | L1 | DVFS |
| 03 | [Failure Forensics](https://github.com/KnigguKniggu-droid/AEGIS) | L4 | BIST+ATPG |
| 04 | [Self-Healing Docs](https://github.com/KnigguKniggu-droid/AEGIS) | L6 | ECO |
| 05 | [Output Arbitration](https://github.com/KnigguKniggu-droid/AEGIS) | L4 | TMR |
| 06 | [Hybrid Search RAG](https://github.com/KnigguKniggu-droid/AEGIS) | L3 | Sensor Fusion |
| 07 | [Semantic Cache](https://github.com/KnigguKniggu-droid/AEGIS) | L2 | CAM |
| 08 | [SQL Guardrails](https://github.com/KnigguKniggu-droid/AEGIS) | L4 | MPU/MMU |
| 09 | [A/B Testing](https://github.com/KnigguKniggu-droid/AEGIS) | L5 | SPRT |
| 10 | [LoRA Pipeline](https://github.com/KnigguKniggu-droid/AEGIS) | L1 | SVD |
| 11 | [API Gateway](https://github.com/KnigguKniggu-droid/AEGIS) | L2 | Token Bucket |
| 12 | [Feature Flags](https://github.com/KnigguKniggu-droid/AEGIS) | L5 | FPGA Reconfig |
| 13 | [Dataset Generator](https://github.com/KnigguKniggu-droid/AEGIS) | L3 | Signal Conditioning |
| 14 | [Workflow Orchestrator](https://github.com/KnigguKniggu-droid/AEGIS) | L6 | FSM Sequencer |
| 15 | [LLM Observability](https://github.com/KnigguKniggu-droid/AEGIS) | L7 | Oscilloscope+SA |

---

## License

MIT
