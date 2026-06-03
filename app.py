import streamlit as st

from lucien_core import (
    analyze_sentence,
    generate_explanation,
    generate_explanation_zh,
)


st.set_page_config(page_title="Lucien", page_icon="🧩", layout="centered")

st.title("Lucien 🧩")
st.subheader("Chinese Sentence Chunker")

st.write(
    "Lucien is a small rule-based tool that breaks simple Chinese sentences "
    "into meaningful chunks and explains their basic structure."
)

st.markdown("### Try an example")

example = st.selectbox(
    "Choose a sample sentence:",
    [
        "我今天很累",
        "我今天不累",
        "我今天不太累",
        "我今天有点累",
        "我今天一点也不累",
        "我今天一点儿也不累",
    ],
)

sentence = st.text_input("Or enter your own Chinese sentence:", example)

if sentence:
    result = analyze_sentence(sentence)

    st.markdown("### Sentence")
    st.success(result["sentence"])

    st.markdown("### Chunks")
    st.write(" | ".join(result["refined_chunks"]))

    st.markdown("### Basic syntax")

    syntax = result["syntax"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Subject", syntax.get("subject") or "—")

    with col2:
        st.metric("Time", syntax.get("time") or "—")

    with col3:
        st.metric("Predicate", syntax.get("predicate") or "—")

    st.markdown("### Meaning")
    st.write(generate_explanation(result))

    st.markdown("### 中文解释")
    st.write(generate_explanation_zh(result))

    st.markdown("### Labeled chunks")

    for item in result["labeled_chunks"]:
        st.markdown(f"**{item['chunk']}** — `{item['label']}`")

    st.markdown("### Merged phrases")

    for item in result["merged_phrases"]:
        label = item.get("label", "unknown")
        text = item.get("text", "")

        st.markdown(f"**{text}** — `{label}`")

        if label == "state_phrase":
            st.write(f"Polarity: `{item.get('polarity')}`")
            st.write(f"Intensity: `{item.get('intensity')}`")
            st.write(f"Tone: `{item.get('tone')}`")

    with st.expander("Structured JSON output"):
        st.json(result)

st.markdown("---")
st.caption(
    "Current version: rule-based MVP. Lucien supports a small set of sentence patterns, "
    "state phrases, degree words, and negation structures."
)