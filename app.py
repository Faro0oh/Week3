import sys
sys.path.append("src")

import streamlit as st
import csv
import json
import httpx
from io import StringIO
from pathlib import Path

from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown


st.set_page_config(page_title="CSV Profiler", layout="wide")

st.title("CSV Profiler")
st.caption("Upload CSV → profile → export JSON + Markdown")

st.sidebar.header("Inputs")

rows = None
report = st.session_state.get("report")

use_url = st.sidebar.checkbox("Load from URL", value=False)

if use_url:
    url = st.sidebar.text_input(
        "CSV URL",
        placeholder="https://example.com/data.csv"
    )

    if url == "":
        st.warning("Paste a URL to load a CSV.")
        st.stop()

    try:
        r = httpx.get(url, timeout=10.0)
        r.raise_for_status()
        text = r.text
        rows = list(csv.DictReader(StringIO(text)))
    except Exception as e:
        st.error("Failed to load URL: " + str(e))
        st.stop()

uploaded = st.file_uploader("Upload a CSV", type=["csv"])
show_preview = st.sidebar.checkbox("Show preview", value=True)

if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))

if rows is not None:
    if len(rows) == 0:
        st.error("CSV has no data. Upload a CSV with at least 1 row.")
        st.stop()

    if len(rows[0]) == 0:
        st.warning("CSV has no headers (no columns detected).")

if rows is not None and show_preview:
    st.subheader("Preview")
    st.write(rows[:5])

if rows is not None:
    if st.button("Generate report"):
        st.session_state["report"] = profile_rows(rows)

report = st.session_state.get("report")

if report is not None:
    cols = st.columns(2)
    cols[0].metric("Rows", report["n_rows"])
    cols[1].metric("Columns", report["n_cols"])

if report is not None:
    st.subheader("Columns")
    st.write(report["columns"])

    with st.expander("Markdown preview", expanded=False):
        st.markdown(render_markdown(report))

if report is not None:
    report_name = st.sidebar.text_input("Report name", value="report")

    json_file = report_name + ".json"
    md_file = report_name + ".md"

    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_text = render_markdown(report)

    c1, c2 = st.columns(2)
    c1.download_button("Download JSON", data=json_text, file_name=json_file)
    c2.download_button("Download Markdown", data=md_text, file_name=md_file)

    if st.button("Save to outputs/"):
        out_dir = Path("outputs")
        out_dir.mkdir(parents=True, exist_ok=True)

        (out_dir / json_file).write_text(json_text, encoding="utf-8")
        (out_dir / md_file).write_text(md_text, encoding="utf-8")

        st.success(f"Saved outputs/{json_file} and outputs/{md_file}")

