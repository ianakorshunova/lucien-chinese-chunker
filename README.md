# Lucien 🧩

Lucien is a lightweight rule-based Chinese sentence chunker.

It breaks simple Chinese sentences into meaningful chunks, labels their basic functions, identifies simple state phrases, and provides short learner-friendly explanations.

## 📌 Overview

Lucien is designed as an educational NLP prototype for Chinese sentence analysis.

It currently focuses on simple sentences with:

* pronouns
* time expressions
* degree words
* negation
* emphatic negation
* state adjectives
* basic predicate structure

Example sentence: `我今天一点儿也不累`

Lucien can identify:

* Subject: `我`
* Time: `今天`
* Predicate: `一点儿也不累`

It can also generate a short English and Chinese explanation of the sentence meaning.

## 💡 Why this project?

Chinese learners often struggle not only with vocabulary, but also with how meaning is built through small function words such as:

* `很`
* `不`
* `不太`
* `有点`
* `一点也不`
* `一点儿也不`

Lucien explores how a transparent rule-based system can identify and explain these patterns.

The project is useful for:

* Chinese language learning
* educational technology experiments
* rule-based NLP practice
* language-focused portfolio work

## 🚀 Features

* Splits simple Chinese sentences into chunks
* Labels chunks by function
* Detects basic syntax roles: subject, time, predicate
* Detects state phrases
* Identifies polarity and intensity
* Generates English explanations
* Generates Chinese explanations
* Provides structured JSON-style output
* Includes a Streamlit web interface
* Includes pytest tests for core behavior

## 🖥️ Streamlit App

Run the local Streamlit app:

`python3 -m streamlit run app.py`

The app allows users to:

* choose sample sentences
* enter their own Chinese sentence
* view chunks
* inspect basic syntax
* read English and Chinese explanations
* inspect structured JSON output

## 🧪 Run Tests

Install dependencies:

`python3 -m pip install -r requirements.txt`

Run tests:

`python3 -m pytest`

## ▶️ Console Version

Run the console demo:

`python3 lucien_cli.py`

## 🧠 Approach

Lucien uses a rule-based NLP approach:

* small dictionaries of known words and patterns
* pattern matching
* iterative chunk refinement
* simple phrase merging
* transparent syntax extraction

The project prioritizes explainability and learner-friendly output over broad language coverage.

## 🧪 Examples

### Basic state sentence

Input: `我今天很累`

Output:

* Subject: `我`
* Time: `今天`
* Predicate: `很累`

### Negative state sentence

Input: `我今天不累`

Output:

* Subject: `我`
* Time: `今天`
* Predicate: `不累`

### Mild state sentence

Input: `我今天有点累`

Output:

* Subject: `我`
* Time: `今天`
* Predicate: `有点累`

### Emphatic negation

Input: `我今天一点儿也不累`

Output:

* Subject: `我`
* Time: `今天`
* Predicate: `一点儿也不累`

## 📊 Output Format

Lucien returns structured output with fields such as:

* `sentence`
* `refined_chunks`
* `labeled_chunks`
* `merged_phrases`
* `syntax`

Example:

* Sentence: `我今天一点儿也不累`
* Refined chunks: `我`, `今天`, `一点儿也`, `不`, `累`
* Subject: `我`
* Time: `今天`
* Predicate: `一点儿也不累`

## 🗂️ Project Structure

lucien/

* `app.py` — Streamlit web interface
* `lucien_core.py` — core sentence analysis logic
* `lucien_cli.py` — console demo
* `requirements.txt` — dependencies
* `tests/test_lucien_core.py` — pytest tests
* `.gitignore` — ignored local files
* `README.md` — project documentation

## 🛠️ Tech Stack

* Python
* Streamlit
* pytest
* rule-based NLP
* JSON-style structured output

## 🧠 Design Decisions

* Chose a rule-based approach for transparency and explainability
* Focused on a small set of learner-relevant sentence patterns
* Separated core logic from the Streamlit interface
* Kept console output separate from the core analysis module
* Added tests to protect core behavior during future changes

## ⚠️ Current Limitations

Lucien is an educational prototype, not a full Chinese parser.

Current limitations:

* small vocabulary
* limited sentence patterns
* no full Chinese word segmentation
* no dependency parsing
* no machine learning component
* explanations are simplified and may not capture all contextual nuance

## 🔮 Future Improvements

* Expand vocabulary and phrase patterns
* Add more sentence structures
* Add Russian-language explanations
* Support emotional and idiomatic expressions, such as `累死我了`
* Improve intensity labels for degree words such as `很`
* Add pinyin support
* Deploy the Streamlit app online

## 📌 Status

Current version: rule-based MVP with a local Streamlit interface and pytest tests.