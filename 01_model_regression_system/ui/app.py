"""Streamlit dashboard for the Model Regression Detection System."""

from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "..")

import os
import json
import asyncio
import httpx
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go

from src.models import EmailCategory, ExpectedDifficulty, PromptConfig
from src.regressor import classify_severity, compute_accuracy, compute_per_difficulty, load_ground_truth

st.set_page_config(page_title="Model Regression System", page_icon=":bar_chart:", layout="wide")

st.title("Model Regression Detection System")
st.markdown("CI/CD-style prompt regression testing pipeline for LLM classification tasks.")

tab1, tab2, tab3, tab4 = st.tabs(["Classify Email", "Ground Truth Data", "Prompt Config", "Regression Simulator"])


def local_classify(subject: str, body: str) -> tuple[EmailCategory, str]:
    """Local keyword-based classifier that mimics the LLM prompt logic.

    This runs entirely on your machine with no API key needed. It uses
    the same category definitions as the prompt in classifier_v1.yaml.
    """
    text = (subject + " " + body).lower()

    billing_keywords = ["invoice", "charge", "payment", "refund", "billing", "subscription", "plan", "price", "cost", "credit card", "proration", "upgrade", "cancel subscription"]
    technical_keywords = ["api", "error", "bug", "500", "timeout", "webhook", "integration", "crash", "rate limit", "headers", "sdk", "endpoint", "server", "debug", "logs"]
    account_keywords = ["login", "password", "reset", "account", "access", "profile", "user", "sso", "ownership", "transfer", "credentials", "log in", "sign in"]
    general_keywords = ["feature", "request", "feedback", "gdpr", "data export", "dark mode", "question", "inquiry", "compliance", "privacy", "suggestion"]

    billing_score = sum(1 for kw in billing_keywords if kw in text)
    technical_score = sum(1 for kw in technical_keywords if kw in text)
    account_score = sum(1 for kw in account_keywords if kw in text)
    general_score = sum(1 for kw in general_keywords if kw in text)

    scores = {
        EmailCategory.BILLING: billing_score,
        EmailCategory.TECHNICAL: technical_score,
        EmailCategory.ACCOUNT: account_score,
        EmailCategory.GENERAL: general_score,
    }

    max_score = max(scores.values())
    if max_score == 0:
        return EmailCategory.GENERAL, "No keyword matches found. Defaulting to general."

    winner = max(scores, key=scores.get)
    reason = f"Matched keywords: {', '.join(kw for kw, cat in [(kw, cat) for cat in [EmailCategory.BILLING, EmailCategory.TECHNICAL, EmailCategory.ACCOUNT, EmailCategory.GENERAL] for kw in (billing_keywords if cat == EmailCategory.BILLING else technical_keywords if cat == EmailCategory.TECHNICAL else account_keywords if cat == EmailCategory.ACCOUNT else general_keywords) if kw in text and cat == winner][:5])}"
    return winner, reason


def classify_with_nvidia_nim(subject: str, body: str, use_free_tier: bool = True) -> None:
    """Classify using NVIDIA NIM (free tier or Nemotron 3 Ultra).
    
    Both tiers require a free NVIDIA API key from https://build.nvidia.com
    - Free tier: meta/llama-3.1-8b-instruct (rate limited)
    - Paid tier: nvidia/nemotron-3-ultra (requires credits)
    """
    import httpx
    import asyncio

    api_key = os.environ.get("NVIDIA_API_KEY", "")
    if not api_key:
        st.error("NVIDIA_API_KEY not found in environment.")
        st.markdown("**Get a free API key:** https://build.nvidia.com")
        st.info("Falling back to local classifier...")
        category, reason = local_classify(st.session_state.get("subject", ""), st.session_state.get("body", ""))
        st.success(f"Classification: {category.value.upper()}")
        st.write(f"**Reason:** {reason}")
        return

    if use_free_tier:
        model = "meta/llama-3.1-8b-instruct"
        st.info("Using NVIDIA NIM free tier (meta/llama-3.1-8b-instruct)...")
    else:
        model = "nvidia/nemotron-3-ultra"
        st.info("Using NVIDIA NIM Nemotron 3 Ultra...")

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.0,
        "max_tokens": 50,
    }

    status = st.empty()
    status.write("Calling NVIDIA NIM...")

    async def call_nim():
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()

    try:
        result = asyncio.run(call_nim())
        raw = result["choices"][0]["message"]["content"].strip().lower()
        for cat in EmailCategory:
            if raw.startswith(cat.value) or raw == cat.value:
                category = cat
                break
        else:
            category = EmailCategory.GENERAL

        st.success(f"Classification: {category.value.upper()}")
        st.write(f"**Model used:** {model}")
        st.write(f"**Raw output:** {raw}")

    except Exception as exc:
        st.error(f"NVIDIA NIM call failed: {exc}")
        st.info("Falling back to local classifier...")
        category, reason = local_classify(st.session_state.get("subject", ""), st.session_state.get("body", ""))
        st.success(f"Classification: {category.value.upper()}")
        st.write(f"**Reason:** {reason}")


def classify_with_openai(subject: str, body: str) -> None:
    """Classify using OpenAI GPT-4o-mini."""
    import httpx
    import asyncio

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("OPENAI_API_KEY not found in environment. Add it to your .env file or environment variables.")
        st.info("Falling back to local classifier...")
        category, reason = local_classify(st.session_state.get("subject", ""), st.session_state.get("body", ""))
        st.success(f"Classification: {category.value.upper()}")
        st.write(f"**Reason:** {reason}")
        return

    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "classifier_v1.yaml"
    import yaml
    raw = yaml.safe_load(prompt_path.read_text(encoding="utf-8"))
    system_prompt = raw.get("system_prompt", "")
    user_template = raw.get("user_template", "")
    user_content = user_template.format(subject=st.session_state.get("subject", ""), body=st.session_state.get("body", ""))

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.0,
        "max_tokens": 50,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    async def call_openai():
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()

    try:
        result = asyncio.run(call_openai())
        raw = result["choices"][0]["message"]["content"].strip().lower()
        for cat in EmailCategory:
            if raw.startswith(cat.value) or raw == cat.value:
                category = cat
                break
        else:
            category = EmailCategory.GENERAL

        st.success(f"Classification: {category.value.upper()}")
        st.write(f"**Model:** gpt-4o-mini")
        st.write(f"**Raw output:** {raw}")

    except Exception as exc:
        st.error(f"OpenAI call failed: {exc}")
        st.info("Falling back to local classifier...")
        category, reason = local_classify(st.session_state.get("subject", ""), st.session_state.get("body", ""))
        st.success(f"Classification: {category.value.upper()}")
        st.write(f"**Reason:** {reason}")


with tab1:
    st.subheader("Classify an Email")
    st.markdown("Paste an email below and the system will classify it into billing, technical, account, or general.")

    col1, col2 = st.columns(2)
    subject = col1.text_input("Email Subject", value="Invoice shows double charge for July")
    body = col2.text_area("Email Body", value="Hi, I just checked my July invoice and it looks like I was charged twice for the same subscription period. Can you look into this and issue a refund for the duplicate charge?", height=100)

    model_choice = st.selectbox(
        "Model",
        options=[
            "Local keyword classifier (no API key, instant)",
            "NVIDIA NIM free tier (Llama 3.1 8B, requires NVIDIA_API_KEY)",
            "NVIDIA NIM Nemotron 3 Ultra (requires NVIDIA_API_KEY)",
            "OpenAI GPT-4o-mini (requires OPENAI_API_KEY)",
        ],
        index=0,
    )

    if st.button("Classify Email", type="primary"):
        if "Local keyword" in model_choice:
            category, reason = local_classify(subject, body)
            st.success(f"Classification: {category.value.upper()}")
            st.write(f"**Reason:** {reason}")
        elif "NVIDIA NIM free" in model_choice:
            classify_with_nvidia_nim(subject, body, use_free_tier=True)
        elif "NVIDIA NIM with API" in model_choice:
            classify_with_nvidia_nim(subject, body, use_free_tier=False)
        elif "OpenAI" in model_choice:
            classify_with_openai(subject, body)

        category_info = {
            EmailCategory.BILLING: ("Questions about invoices, charges, payments, refunds, or subscription plans.", "#4a9eff"),
            EmailCategory.TECHNICAL: ("Bug reports, integration issues, API errors, or product malfunction reports.", "#2ecc71"),
            EmailCategory.ACCOUNT: ("Login problems, password resets, account access, profile changes, or user management.", "#f5a623"),
            EmailCategory.GENERAL: ("Anything that does not fit the three categories above.", "#e74c3c"),
        }
        info, color = category_info[category]
        st.info(f"**Category definition:** {info}")

        st.write("---")
        st.write("**Try these examples:**")
        examples = [
            ("API returns 500 error on /v2/users endpoint", "When I call GET /v2/users the server returns a 500 error."),
            ("Cannot log in after password reset", "I reset my password but now I cannot log in with the new password."),
            ("Feature request: dark mode for dashboard", "It would be helpful if you could add a dark mode option."),
            ("Refund not reflected on credit card", "You issued a refund but my credit card statement does not show it."),
        ]
        for ex_subject, ex_body in examples:
            if st.button(f"Try: {ex_subject}", key=f"example_{ex_subject}"):
                subject = ex_subject
                body = ex_body
                category, reason = local_classify(subject, body)
                st.success(f"Classification: {category.value.upper()}")
                st.write(f"**Reason:** {reason}")
                st.rerun()

with tab2:
    st.subheader("Ground Truth Test Items")
    gt_path = Path(__file__).resolve().parent.parent / "tests" / "ground_truth.json"
    if gt_path.exists():
        items = load_ground_truth(gt_path)
        data = []
        for item in items:
            data.append({
                "ID": item.id,
                "Subject": item.subject[:60],
                "Expected": item.expected_category.value,
                "Difficulty": item.expected_difficulty.value,
                "Tags": ", ".join(item.tags[:3]),
            })
        st.dataframe(data, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        cats = [i.expected_category.value for i in items]
        diffs = [i.expected_difficulty.value for i in items]
        col1.metric("Total Items", len(items))
        col2.metric("Categories", len(set(cats)))
        col3.metric("Difficulties", len(set(diffs)))

        fig = go.Figure(data=[go.Bar(
            x=list(set(cats)),
            y=[cats.count(c) for c in set(cats)],
            marker_color=["#4a9eff", "#2ecc71", "#f5a623", "#e74c3c"],
        )])
        fig.update_layout(title="Category Distribution", xaxis_title="Category", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure(data=[go.Bar(
            x=list(set(diffs)),
            y=[diffs.count(d) for d in set(diffs)],
            marker_color=["#2ecc71", "#f5a623", "#e74c3c"],
        )])
        fig2.update_layout(title="Difficulty Distribution", xaxis_title="Difficulty", yaxis_title="Count")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Ground truth file not found.")

with tab3:
    st.subheader("Prompt Configuration")
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "classifier_v1.yaml"
    if prompt_path.exists():
        import yaml
        raw = yaml.safe_load(prompt_path.read_text(encoding="utf-8"))
        st.code(raw.get("system_prompt", ""), language="text")
        st.write(f"**Model:** {raw.get('model', '')}")
        st.write(f"**Version:** {raw.get('version', '')}")
        st.write(f"**Temperature:** {raw.get('temperature', 0)}")
        st.write(f"**Categories:** {', '.join(raw.get('categories', []))}")
    else:
        st.warning("Prompt file not found. Showing default config.")
        st.json({"prompt_id": "classifier_v1", "version": "1.0.0", "model": "gpt-4o-mini"})

with tab4:
    st.subheader("Regression Simulator")
    st.markdown("Simulate model predictions and see regression detection in action.")

    gt_path = Path(__file__).resolve().parent.parent / "tests" / "ground_truth.json"
    if gt_path.exists():
        items = load_ground_truth(gt_path)

        col1, col2 = st.columns(2)
        accuracy_target = col1.slider("Simulated Accuracy (%)", 0, 100, 85)
        baseline_acc = col2.slider("Baseline Accuracy (%)", 0, 100, 90)

        if st.button("Run Simulation", type="primary"):
            import random
            random.seed(42)
            cats = [EmailCategory.BILLING, EmailCategory.TECHNICAL, EmailCategory.ACCOUNT, EmailCategory.GENERAL]
            predictions = []
            for item in items:
                if random.randint(1, 100) <= accuracy_target:
                    pred_cat = item.expected_category
                else:
                    pred_cat = random.choice([c for c in cats if c != item.expected_category])
                from src.models import ModelPrediction
                predictions.append(ModelPrediction(item_id=item.id, predicted_category=pred_cat))

            correct, total = compute_accuracy(items, predictions)
            actual_acc = correct / total
            delta = actual_acc - (baseline_acc / 100)
            severity = classify_severity(delta)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accuracy", f"{actual_acc:.1%}")
            col2.metric("Baseline", f"{baseline_acc / 100:.1%}")
            col3.metric("Delta", f"{delta:+.1%}")
            col4.metric("Severity", severity.value.upper())

            if severity.value == "critical":
                st.error("CRITICAL: Merge would be blocked. Regression exceeds 8% threshold.")
            elif severity.value == "warning":
                st.warning("WARNING: Regression exceeds 3% threshold. Review before merge.")
            else:
                st.success("No regression detected. Safe to merge.")

            per_diff = compute_per_difficulty(items, predictions)
            diff_data = []
            for diff, stats in per_diff.items():
                diff_data.append({"Difficulty": diff, "Accuracy": f"{stats['accuracy']:.1%}", "Correct": f"{int(stats['correct'])}/{int(stats['total'])}"})
            st.dataframe(diff_data, use_container_width=True)

            results = []
            for item, pred in zip(items, predictions, strict=True):
                is_correct = pred.predicted_category == item.expected_category
                results.append({
                    "ID": item.id,
                    "Expected": item.expected_category.value,
                    "Predicted": pred.predicted_category.value if pred.predicted_category else "NONE",
                    "Correct": "Yes" if is_correct else "No",
                })
            st.dataframe(results, use_container_width=True)
