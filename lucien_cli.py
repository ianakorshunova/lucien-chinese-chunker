from lucien_core import (
    analyze_sentence,
    generate_explanation,
    generate_explanation_zh,
)


def print_pretty(result):
    print(f"🧠 Sentence: {result['sentence']}")
    print(f"👉 Meaning: {generate_explanation(result)}")
    print(f"👉 中文解释: {generate_explanation_zh(result)}")

    state_phrase = None
    for item in result["merged_phrases"]:
        if item["label"] == "state_phrase":
            state_phrase = item
            break

    if state_phrase:
        print(f"🎭 Tone: {state_phrase['tone']}")

    syntax = result["syntax"]
    print(f"🔹 Structure: {syntax['subject']} + {syntax['time']} + {syntax['predicate']}")
    print()


if __name__ == "__main__":
    sentences = [
        "我今天一点也不累",
        "我今天一点儿也不累",
    ]

    for sentence in sentences:
        result = analyze_sentence(sentence)
        print_pretty(result)