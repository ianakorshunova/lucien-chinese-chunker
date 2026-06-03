import json

# Lucien dictionaries

PRONOUNS = ["我", "你", "他", "她", "它", "我们", "你们", "他们", "她们"]
TIME_WORDS = ["今天", "昨天", "明天"]
CONNECTORS = ["但是", "因为", "所以"]
LOCATION_MARKER = "在"
VERBS = ["学习", "吃", "喝", "看", "说", "去", "来", "写", "听", "读"]
STATES = ["累", "饿", "困", "忙", "冷", "热"]
DESCRIPTIONS = ["美丽", "漂亮", "帅", "高", "矮", "大", "小"]
DEGREE_WORDS = ["很", "非常", "太", "真", "特别", "有点", "超", "有一点", "一点也", "一点都"]
NEGATIONS = ["不", "没", "没有", "无"]
STRONG_NEGATIONS = ["毫无"]
LITERARY_NEGATIONS = ["莫"]
EMPHATIC_NEGATIONS = ["一点也", "一点都", "一点儿也", "一点儿都"]

# Small helper functions
def split_location(chunk):
    if not chunk.startswith("在"):
        return [chunk]

    if len(chunk) <= 2:
        return [chunk]

    location_part = chunk[:3]
    rest_part = chunk[3:]

    if rest_part:
        return [location_part, rest_part]
    else:
        return [location_part]

def split_connector(chunk):
    for connector in CONNECTORS:
        if chunk.startswith(connector) and len(chunk) > len(connector):
            rest_part = chunk[len(connector):]
            return [connector, rest_part]

    return [chunk]

def split_negation(chunk):
    for neg in NEGATIONS:
        if chunk.startswith(neg) and len(chunk) > 1:
            return [neg, chunk[len(neg):]]
    return [chunk]

def split_degree_phrase(chunk):
    for degree in DEGREE_WORDS:
        if chunk.startswith(degree) and len(chunk) > len(degree):
            rest_part = chunk[len(degree):]
            return [degree, rest_part]

    return [chunk]

def split_time(chunk):
    for time_word in TIME_WORDS:
        if chunk.startswith(time_word) and len(chunk) > len(time_word):
            return [time_word, chunk[len(time_word):]]
    return [chunk]

def split_emphasis_negation(chunk):
    for phrase in EMPHATIC_NEGATIONS:
        if chunk.startswith(phrase) and len(chunk) > len(phrase):
            rest_part = chunk[len(phrase):]
            return [phrase, rest_part]

    return [chunk]

def split_pronoun(chunk):
    for pronoun in PRONOUNS:
        if chunk.startswith(pronoun) and len(chunk) > len(pronoun):
            rest_part = chunk[len(pronoun):]
            return [pronoun, rest_part]
    return [chunk]

def get_semantics(parts):
    labels = [p["label"] for p in parts]
    chunks = [p["chunk"] for p in parts]

    polarity = "positive"
    intensity = "neutral"

    # polarity
    if "negation" in labels:
        polarity = "negative"

    # special case: 一点也不 / 一点都不
    if any(word in chunks for word in EMPHATIC_NEGATIONS) and "negation" in labels:
        polarity = "negative"
        intensity = "high"

    # special case: 不太
    elif "negation" in labels and "太" in chunks:
        intensity = "low"

    # special case: 有点 / 有一点
    elif "有点" in chunks or "有一点" in chunks:
        polarity = "positive"
        intensity = "low"

    # normal degree
    elif "degree" in labels:
        if any(word in chunks for word in ["非常", "特别", "超"]):
            intensity = "very_high"
        elif "很" in chunks:
            intensity = "high"
        elif "太" in chunks:
            intensity = "too_high"
        else:
            intensity = "medium"

    return polarity, intensity

def get_tone(parts):
    labels = [p["label"] for p in parts]
    chunks = [p["chunk"] for p in parts]

    # super strong negative
    if any(word in chunks for word in EMPHATIC_NEGATIONS) and "negation" in labels:
      return "strong_negative"

    # mild negative
    if "negation" in labels and "太" in chunks:
        return "mild_negative"

    # mild
    if "有点" in chunks or "有一点" in chunks:
        return "mild"

    # very strong
    if any(word in chunks for word in ["非常", "特别", "超"]):
        return "very_strong"

    # strong
    if "很" in chunks:
        return "strong"

    # default negative
    if "negation" in labels:
        return "negative"

    return "neutral"

# main pipeline stages
def chunk_sentence(sentence):
    chunked = sentence

    # Step 0: normalize punctuation
    chunked = chunked.replace("，", " ")

    # Step 1: time words
    for word in TIME_WORDS:
        chunked = chunked.replace(word, "/" + word)

    # Step 2: connectors
    for word in CONNECTORS:
        chunked = chunked.replace(word, "/" + word)

    # Step 3: location
    chunked = chunked.replace(LOCATION_MARKER, "/" + LOCATION_MARKER)

    # Step 4: clean start
    if chunked.startswith("/"):
        chunked = chunked[1:]

    # Step 5: split into chunks
    chunks = chunked.split("/")

    # Step 6: clean each chunk
    clean_chunks = []
    for chunk in chunks:
        chunk = chunk.strip()
        if chunk:
            clean_chunks.append(chunk)

    return clean_chunks

def refine_chunks(chunks):
    refined = []

    for chunk in chunks:
        chunk = chunk.strip()

        # 0. pronoun
        if any(chunk.startswith(pronoun) for pronoun in PRONOUNS):
            parts = split_pronoun(chunk)
            refined.extend(parts)

        # 1. time
        elif any(chunk.startswith(time_word) for time_word in TIME_WORDS):
            parts = split_time(chunk)
            refined.extend(parts)

        # 2. location
        elif chunk.startswith("在"):
            parts = split_location(chunk)
            refined.extend(parts)

        # 3. connector
        elif any(chunk.startswith(connector) for connector in CONNECTORS):
            parts = split_connector(chunk)
            refined.extend(parts)

        else:
            # first: emphatic negation
            parts = split_emphasis_negation(chunk)

            temp = []
            for part in parts:
                neg_parts = split_negation(part)

                for neg_part in neg_parts:
                    temp.extend(split_degree_phrase(neg_part))

            refined.extend(temp)

    # cleanup
    clean_refined = []
    for item in refined:
        item = item.strip()
        if item:
            clean_refined.append(item)

    return clean_refined

def label_chunks(chunks):
    labeled_chunks = []

    for chunk in chunks:
        chunk = chunk.strip()

        if chunk in PRONOUNS:
            label = "pronoun"
        elif chunk in TIME_WORDS:
            label = "time"
        elif chunk.startswith(LOCATION_MARKER):
            label = "location_phrase"
        elif chunk in CONNECTORS:
            label = "connector"
        elif chunk in EMPHATIC_NEGATIONS:
            label = "emphatic_negation"
        elif chunk in NEGATIONS:
            label = "negation"
        elif chunk in VERBS:
            label = "verb"
        elif chunk in DEGREE_WORDS:
            label = "degree"
        elif any(state in chunk for state in STATES):
            label = "state"
        elif any(desc in chunk for desc in DESCRIPTIONS):
            label = "description"
        else:
            label = "unknown"

        labeled_chunks.append({
            "chunk": chunk,
            "label": label
        })

    return labeled_chunks

def merge_phrases(chunks):
    merged = []
    i = 0

    while i < len(chunks):

        # 1️⃣ negation + degree + state
        if (
            i + 2 < len(chunks)
            and chunks[i] in NEGATIONS
            and chunks[i + 1] in DEGREE_WORDS
            and chunks[i + 2] in STATES
        ):
            parts = [
                {"chunk": chunks[i], "label": "negation"},
                {"chunk": chunks[i + 1], "label": "degree"},
                {"chunk": chunks[i + 2], "label": "state"}
            ]

            polarity, intensity = get_semantics(parts)
            tone = get_tone(parts)

            merged.append({
                "text": chunks[i] + chunks[i + 1] + chunks[i + 2],
                "label": "state_phrase",
                "polarity": polarity,
                "intensity": intensity,
                "tone": tone,
                "parts": parts
            })

            i += 3
            continue

        # emphatic negation + negation + state
        if (
            i + 2 < len(chunks)
            and chunks[i] in EMPHATIC_NEGATIONS
            and chunks[i + 1] in NEGATIONS
            and chunks[i + 2] in STATES
        ):
            parts = [
                {"chunk": chunks[i], "label": "emphasis"},
                {"chunk": chunks[i + 1], "label": "negation"},
                 {"chunk": chunks[i + 2], "label": "state"}
            ]

            polarity, intensity = get_semantics(parts)
            tone = get_tone(parts)

            merged.append({
                "text": chunks[i] + chunks[i + 1] + chunks[i + 2],
                "label": "state_phrase",
                "polarity": polarity,
                "intensity": intensity,
                "tone": tone,
                "parts": parts
            })

            i += 3
            continue

        # 2️⃣ negation + state
        if (
            i + 1 < len(chunks)
            and chunks[i] in NEGATIONS
            and chunks[i + 1] in STATES
        ):
            parts = [
                {"chunk": chunks[i], "label": "negation"},
                {"chunk": chunks[i + 1], "label": "state"}
            ]

            polarity, intensity = get_semantics(parts)
            tone = get_tone(parts)

            merged.append({
                "text": chunks[i] + chunks[i + 1],
                "label": "state_phrase",
                "polarity": polarity,
                "intensity": intensity,
                "tone": tone,
                "parts": parts
            })

            i += 2
            continue

        # 3️⃣ degree + state
        if (
            i + 1 < len(chunks)
            and chunks[i] in DEGREE_WORDS
            and chunks[i + 1] in STATES
        ):
            parts = [
                {"chunk": chunks[i], "label": "degree"},
                {"chunk": chunks[i + 1], "label": "state"}
            ]

            polarity, intensity = get_semantics(parts)
            tone = get_tone(parts)

            merged.append({
                "text": chunks[i] + chunks[i + 1],
                "label": "state_phrase",
                "polarity": polarity,
                "intensity": intensity,
                "tone": tone,
                "parts": parts
            })

            i += 2
            continue

        # 4️⃣ fallback
        merged.append({
            "text": chunks[i],
            "label": "single"
        })

        i += 1

    return merged

def extract_syntax(result):
    subject = None
    time = None
    predicate = None

    for item in result["labeled_chunks"]:
        if item["label"] == "pronoun" and subject is None:
            subject = item["chunk"]
        elif item["label"] == "time" and time is None:
            time = item["chunk"]

    for item in result["merged_phrases"]:
        if item["label"] == "state_phrase":
            predicate = item["text"]
            break

    return {
        "subject": subject,
        "time": time,
        "predicate": predicate
    }


def analyze_syntax(labeled_chunks):
    syntax_roles = []

    for item in labeled_chunks:
        chunk = item["chunk"]
        label = item["label"]

        if label == "pronoun":
            role = "possible_subject"
        elif label == "time":
            role = "time_modifier"
        elif label == "location_phrase":
            role = "place_modifier"
        elif label == "verb":
            role = "predicate"
        elif label == "state":
            role = "state"
        elif label == "connector":
            role = "connector"
        else:
            role = "other"

        syntax_roles.append({
            "chunk": chunk,
            "label": label,
            "syntax_role": role
        })

    return syntax_roles

def analyze_sentence(sentence):
  chunks = chunk_sentence(sentence)
  refined_once = refine_chunks(chunks)
  refined_twice = refine_chunks(refined_once)
  labeled = label_chunks(refined_twice)
  merged = merge_phrases(refined_twice)

  return {
      "sentence": sentence,
      "refined_chunks": refined_twice,
      "labeled_chunks": labeled,
      "merged_phrases": merged,
      "syntax": extract_syntax({
          "labeled_chunks": labeled,
          "merged_phrases": merged
      })
  }

def generate_explanation(result):
    subject = None
    time = None
    state_phrase = None

    for item in result["labeled_chunks"]:
        if item["label"] == "pronoun":
            subject = item["chunk"]
        elif item["label"] == "time":
            time = item["chunk"]

    for item in result["merged_phrases"]:
        if item["label"] == "state_phrase":
            state_phrase = item
            break

    if not state_phrase:
        return "No clear state expression identified."

    polarity = state_phrase.get("polarity", "neutral")
    intensity = state_phrase.get("intensity", "neutral")

    if polarity == "negative" and intensity == "low":
        state_meaning = "not very tired"
        summary = "a mildly negative state"
    elif polarity == "negative" and intensity == "neutral":
        state_meaning = "not tired"
        summary = "a negative state"
    elif polarity == "positive" and intensity == "high":
        state_meaning = "very tired"
        summary = "a strong state"
    elif polarity == "positive" and intensity == "low":
        state_meaning = "a bit tired"
        summary = "a mild state"
    elif polarity == "positive" and intensity == "neutral":
        state_meaning = "tired"
        summary = "a state"
    elif polarity == "positive" and intensity == "very_high":
      state_meaning = "extremely tired"
      summary = "a very strong state"
    elif polarity == "negative" and intensity == "high":
      state_meaning = "not tired at all"
      summary = "a strong negative state"
    else:
        state_meaning = "in a certain state"
        summary = "a state"

    sentence = "The sentence suggests that "

    if subject == "我":
        sentence += "the speaker is "
    else:
        sentence += "someone is "

    sentence += state_meaning

    if time == "今天":
        sentence += " today"

    sentence += f". This expresses {summary}."

    return sentence

def generate_explanation_zh(result):
    subject = None
    time = None
    state_phrase = None

    for item in result["labeled_chunks"]:
        if item["label"] == "pronoun":
            subject = item["chunk"]
        elif item["label"] == "time":
            time = item["chunk"]

    for item in result["merged_phrases"]:
        if item["label"] == "state_phrase":
            state_phrase = item
            break

    if not state_phrase:
        return "没有识别出明确的状态短语。"

    polarity = state_phrase.get("polarity", "neutral")
    intensity = state_phrase.get("intensity", "neutral")
    original_sentence = result["sentence"]

    if any(word in original_sentence for word in ["一点儿也", "一点儿都"]):
      emphasis_form = "一点儿"
    elif any(word in original_sentence for word in ["一点也", "一点都"]):
      emphasis_form = "一点"
    else:
      emphasis_form = None

    if polarity == "negative" and intensity == "low":
        state_meaning = "不太累"
        summary = "轻微否定状态"
    elif polarity == "negative" and intensity == "neutral":
        state_meaning = "不累"
        summary = "否定状态"
    elif polarity == "positive" and intensity == "high":
        state_meaning = "很累"
        summary = "强烈状态"
    elif polarity == "positive" and intensity == "low":
        state_meaning = "有点累"
        summary = "轻微状态"
    elif polarity == "positive" and intensity == "neutral":
        state_meaning = "累"
        summary = "状态"
    elif polarity == "positive" and intensity == "very_high":
      state_meaning = "非常累"
      summary = "很强烈的状态"
    elif polarity == "negative" and intensity == "high":
      if emphasis_form == "一点儿":
        state_meaning = "一点儿也不累"
      else:
        state_meaning = "一点也不累"

      summary = "强烈否定状态"

    else:
        state_meaning = state_phrase.get("text", "")
        summary = "状态"

    sentence = "这句话表示"

    if subject == "我":
        sentence += "说话人"

    if time == "今天":
        sentence += "今天"

    sentence += state_meaning + "。"
    sentence += f" 这是一个{summary}。"

    return sentence