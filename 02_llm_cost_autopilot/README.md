# LLM Cost Autopilot

> Cut LLM API costs by 60%+ with intelligent routing.

Routes requests to the cheapest capable model via a capability matrix, provides semantic caching for repeated queries, automatic fallback chains, and budget guardrails with real-time cost tracking.

**Part of [AEGIS](https://github.com/KnigguKniggu-droid/AEGIS)** — Adaptive AI Governance Infrastructure for Cyber-Physical Systems. This subsystem maps to **L1: Compute Fabric** (DVFS / big.LITTLE scheduling — classify request complexity, route to the cheapest capable model, identical to dynamic voltage-frequency scaling in mobile SoCs.).

---

## Architecture Position

```
AEGIS Layer: L1: Compute Fabric
ECE Mapping: DVFS / big.LITTLE scheduling — classify request complexity, route to the cheapest capable model, identical to dynamic voltage-frequency scaling in mobile SoCs.
```

This module is one of 15 subsystems in the AEGIS platform. See the [unified architecture](https://github.com/KnigguKniggu-droid/AEGIS#readme) for how all components interconnect.

---

## Features

- Capability matrix routing (task to model mapping)
- Semantic caching proxy (Redis + embeddings) at 40%+ hit rate
- Automatic fallback chain: GPT-4 to Claude-3-Haiku to Llama-3.1-8B-local
- Budget guardrails: daily/per-project caps with Slack alerts
- Prometheus metrics + Grafana dashboard showing real-time $/1k tokens

---

## Tech Stack

`Python` | `FastAPI` | `Redis` | `SQLite` | `Prometheus` | `Grafana` | `Sentence-Transformers` | `Docker`

---

## Quick Start

```bash
git clone https://github.com/KnigguKniggu-droid/02-llm-cost-autopilot.git
cd 02-llm-cost-autopilot
pip install -e .
```

Run tests:

```bash
pytest tests/ -v
```

---

## Project Structure

```
02_llm_cost_autopilot/
  src/                  # Core application code
  tests/                # 8 passing tests
  .github/              # CI/CD workflows
  Dockerfile            # Container build
  pyproject.toml        # Package configuration
```

---

## Running in Docker

```bash
docker build -t 02_llm_cost_autopilot .
docker run -p 8000:8000 02_llm_cost_autopilot
```

---

## ECE Design Principles

This subsystem is modeled after classical electrical and computer engineering concepts:

> **DVFS / big.LITTLE scheduling — classify request complexity, route to the cheapest capable model, identical to dynamic voltage-frequency scaling in mobile SoCs.**

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
