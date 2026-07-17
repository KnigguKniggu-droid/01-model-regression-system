# Output Arbitration System

> Multi-model consensus for critical LLM outputs.

Fans out to 3+ models in parallel with circuit breakers, uses LLM-as-judge to score each output, applies weighted voting with configurable quorum, and logs minority reports for audit.

**Part of [AEGIS](https://github.com/KnigguKniggu-droid/AEGIS)** — Adaptive AI Governance Infrastructure for Cyber-Physical Systems. This subsystem maps to **L4: Safety-Critical Fault Tolerance** (Triple Modular Redundancy (TMR) — three independent models produce outputs, Byzantine agreement selects the consensus, identical to voting logic in avionics.).

---

## Architecture Position

```
AEGIS Layer: L4: Safety-Critical Fault Tolerance
ECE Mapping: Triple Modular Redundancy (TMR) — three independent models produce outputs, Byzantine agreement selects the consensus, identical to voting logic in avionics.
```

This module is one of 15 subsystems in the AEGIS platform. See the [unified architecture](https://github.com/KnigguKniggu-droid/AEGIS#readme) for how all components interconnect.

---

## Features

- Parallel fanout to 3+ models (API + local) with circuit breakers
- LLM-as-judge scoring on correctness, style, safety
- Weighted voting with configurable quorum
- Minority report logging for audit trails
- Latency budget: parallel fanout + 200ms judge = <2s p99

---

## Tech Stack

`Python` | `FastAPI` | `AsyncIO` | `Redis` | `PostgreSQL` | `OpenTelemetry` | `Docker`

---

## Quick Start

```bash
git clone https://github.com/KnigguKniggu-droid/05-output-arbitration-system.git
cd 05-output-arbitration-system
pip install -e .
```

Run tests:

```bash
pytest tests/ -v
```

---

## Project Structure

```
05_output_arbitration_system/
  src/                  # Core application code
  tests/                # 11 passing tests
  .github/              # CI/CD workflows
  Dockerfile            # Container build
  pyproject.toml        # Package configuration
```

---

## Running in Docker

```bash
docker build -t 05_output_arbitration_system .
docker run -p 8000:8000 05_output_arbitration_system
```

---

## ECE Design Principles

This subsystem is modeled after classical electrical and computer engineering concepts:

> **Triple Modular Redundancy (TMR) — three independent models produce outputs, Byzantine agreement selects the consensus, identical to voting logic in avionics.**

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
