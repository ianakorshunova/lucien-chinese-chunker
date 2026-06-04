import streamlit as st

from lucien_core import (
    analyze_sentence,
    generate_explanation,
    generate_explanation_zh,
)


st.set_page_config(page_title="Lucien", page_icon="🧩", layout="centered")

EXAMPLES = {
    "Degree + state: 我今天很累": "我今天很累",
    "Negative state: 我今天不累": "我今天不累",
    "Mild negative: 我今天不太累": "我今天不太累",
    "Mild state: 我今天有点累": "我今天有点累",
    "Emphatic negation: 我今天一点也不累": "我今天一点也不累",
    "Emphatic negation with 儿: 我今天一点儿也不累": "我今天一点儿也不累",
}


with st.sidebar:
    st.title("Lucien 🧩")
    st.markdown("**Chinese sentence chunker**")

    st.markdown("### What it analyzes")
    st.write("• Sentence chunks")
    st.write("• Basic syntax roles")
    st.write("• State phrases")
    st.write("• Polarity and intensity")
    st.write("• English + 中文 explanations")

    st.markdown("### Current scope")
    st.caption(
        "Lucien is a small educational NLP prototype. "
        "It supports a limited set of simple Chinese sentence patterns."
    )

    st.markdown("### Tech")
    st.caption("Python · Streamlit · pytest · Rule-based NLP")

    st.markdown("### Note")
    st.caption(
        "Lucien is a prototype and does not perform full Chinese parsing or word segmentation."
    )


st.title("Lucien 🧩")
st.markdown("## Chinese Sentence Chunker")

st.write(
    "Lucien breaks simple Chinese sentences into meaningful chunks, identifies "
    "basic syntax roles, and explains state expressions in a learner-friendly way."
)

st.markdown("---")

st.markdown("### Try an example")

example_label = st.selectbox(
    "Choose a sample sentence:",
    list(EXAMPLES.keys()),
)

default_sentence = EXAMPLES[example_label]

sentence = st.text_input(
    "Or enter your own Chinese sentence:",
    value=default_sentence,
)

if sentence:
    result = analyze_sentence(sentence)

    st.markdown("### Sentence")
    st.success(result["sentence"])

    st.markdown("### Chunks")
    chunk_html = " <span style='color: #777;'>→</span> ".join(
        [
            f"<span style='font-size: 28px; padding: 6px 10px; "
            f"background-color: #f5f5f5; border-radius: 8px;'>{chunk}</span>"
            for chunk in result["refined_chunks"]
        ]
    )
    
    st.markdown(chunk_html, unsafe_allow_html=True)

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

    with st.container(border=True):
        st.markdown("**English explanation**")
        st.write(generate_explanation(result))

    with st.container(border=True):
        st.markdown("**中文解释**")
        st.write(generate_explanation_zh(result))

    st.markdown("### Analysis details")

    tab1, tab2 = st.tabs(["Labeled chunks", "Merged phrases"])

    with tab1:
        for item in result["labeled_chunks"]:
            st.markdown(f"**{item['chunk']}** — `{item['label']}`")

    with tab2:
        for item in result["merged_phrases"]:
            label = item.get("label", "unknown")
            text = item.get("text", "")

            with st.container(border=True):
                st.markdown(f"**{text}** — `{label}`")

                if label == "state_phrase":
                    st.markdown(
                        f"""
                        <div style="font-size: 18px; line-height: 1.8;">
                            <strong>Polarity:</strong> <code>{item.get("polarity") or "—"}</code><br>
                            <strong>Intensity:</strong> <code>{item.get("intensity") or "—"}</code><br>
                            <strong>Tone:</strong> <code>{item.get("tone") or "—"}</code>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with st.expander("Structured JSON output"):
        st.json(result)

st.markdown("---")
st.caption(
    "Current version: rule-based MVP. Lucien supports a small set of sentence patterns, "
    "state phrases, degree words, and negation structures."
)