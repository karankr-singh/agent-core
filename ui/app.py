# ui/app.py
import json
import os
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Agent System Dashboard", layout="wide")
st.title("🧠 Agent System Dashboard")

# ---------- helpers ----------
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def extract_tags(text):
    return re.findall(r"#\w+(:[^]\s]+)?", text)

def safe_len(x):
    return len(x) if x else 0

# ---------- load data ----------
memory = load_json("../memory.json", {"goal": "N/A", "history": []})
reputation = load_json("../reputation.json", {})
schedule = load_json("../schedule.json", [])
vector_mem = load_json("../vector_memory.json", [])

# ---------- layout ----------
col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
    st.subheader("🎯 Current Goal")
    st.write(memory.get("goal", "N/A"))

    st.subheader("🧾 Recent History")
    history = memory.get("history", [])
    if history:
        for h in history[-10:]:
            st.code(f"{h['type']}: {str(h['content'])[:500]}")
    else:
        st.info("No history yet.")

# ---------- RIGHT ----------
with col2:
    st.subheader("⭐ Reputation Scores")
    if reputation:
        rep_df = pd.DataFrame(list(reputation.items()), columns=["Agent", "Score"])
        st.bar_chart(rep_df.set_index("Agent"))
        st.dataframe(rep_df, use_container_width=True)
    else:
        st.info("No reputation data yet.")

    st.subheader("📅 Scheduled Goals")
    if schedule:
        for t in schedule:
            st.write(f"• {t.get('goal', 'Unknown goal')}")
    else:
        st.info("No scheduled goals.")

# ---------- ANALYTICS ----------
st.markdown("---")
st.subheader("📊 System Analytics")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Memory Entries", safe_len(history))
with c2:
    st.metric("Vector Memory Size", safe_len(vector_mem))
with c3:
    st.metric("Scheduled Goals", safe_len(schedule))

# ---------- TAG CLUSTERING ----------
st.markdown("---")
st.subheader("🏷️ Vector Memory Clusters (by Tag)")

if vector_mem:
    rows = []
    for item in vector_mem:
        text = item.get("text", "")
        tags = extract_tags(text)
        for t in tags:
            rows.append({"tag": t, "text": text})

    if rows:
        df = pd.DataFrame(rows)

        # Cluster counts
        counts = df.groupby("tag").size().reset_index(name="count")
        st.bar_chart(counts.set_index("tag"))

        # Filter
        st.subheader("🔎 Filter by Tag")
        selected = st.selectbox("Choose a tag", sorted(counts["tag"].tolist()))
        filtered = df[df["tag"] == selected]["text"].unique().tolist()

        for t in filtered[:10]:
            st.code(t[:800])
    else:
        st.info("No tags found in vector memory.")
else:
    st.info("Vector memory is empty.")

# ---------- STATUS ----------
st.markdown("---")
st.subheader("🔒 System Status")
st.success("System is running normally.")
