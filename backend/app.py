"""
StudyBot — NLP Course Assistant
Backend: Flask + NLTK
Techniques used from lectures:
  - Regular Expressions (Lecture 2)
  - Tokenization & Preprocessing (Lecture 2)
  - Edit Distance / Levenshtein (Lecture 3)
  - Noisy Channel Model / Spell Correction (Lecture 3)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import re, random, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from typing import Tuple, List

app = Flask(__name__)
CORS(app)

# ── Download NLTK data ────────────────────────────────────────────────────────
for res in ["punkt", "punkt_tab", "stopwords"]:
    nltk.download(res, quiet=True)

_stop_words = set(stopwords.words("english"))

# ══════════════════════════════════════════════════════════════════════════════
# EDIT DISTANCE  (Lecture 3 — Minimum Edit Distance, Levenshtein)
# ══════════════════════════════════════════════════════════════════════════════
def edit_distance(s1: str, s2: str) -> int:
    """
    Classic Levenshtein distance.
    Costs: insertion=1, deletion=1, substitution=2
    Uses dynamic programming (DP table from lecture).
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]          # match — free
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,                  # deletion
                    dp[i][j - 1] + 1,                  # insertion
                    dp[i - 1][j - 1] + 2,              # substitution
                )
    return dp[m][n]


# ══════════════════════════════════════════════════════════════════════════════
# SPELL CORRECTION  (Lecture 3 — Noisy Channel Model)
# ══════════════════════════════════════════════════════════════════════════════
_VOCAB = [
    "tokenization", "stemming", "lemmatization", "regex", "regular", "expression",
    "corpus", "preprocessing", "stopwords", "nlp", "natural", "language", "processing",
    "edit", "distance", "levenshtein", "noisy", "channel", "spell", "correction",
    "nltk", "python", "machine", "learning", "neural", "network", "transformer",
    "embedding", "vector", "classification", "sentiment", "analysis", "chatbot",
    "bigram", "trigram", "ngram", "token", "word", "sentence", "paragraph",
    "accuracy", "precision", "recall", "confusion", "matrix", "training",
    "attention", "bert", "gpt", "sequence", "generation", "extraction",
    "dynamic", "programming", "backtrace", "alignment", "substitution",
    "insertion", "deletion", "candidate", "prior", "bayesian", "inference",
]

def spell_correct(word: str) -> str:
    """Noisy-channel-style correction — pick closest vocabulary word."""
    w = word.lower()
    if w in _VOCAB:
        return w
    best, best_dist = w, float("inf")
    for v in _VOCAB:
        d = edit_distance(w, v)
        if d < best_dist:
            best_dist, best = d, v
    return best if best_dist <= 3 else w


# ══════════════════════════════════════════════════════════════════════════════
# TEXT PREPROCESSING PIPELINE  (Lecture 2)
# ══════════════════════════════════════════════════════════════════════════════
def preprocess(text: str) -> List[str]:
    """Lower → strip punct → tokenize → remove stops → spell-correct."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)           # remove punctuation
    tokens = word_tokenize(text)                    # NLTK word tokenizer
    tokens = [
        spell_correct(t)
        for t in tokens
        if t not in _stop_words and len(t) > 1
    ]
    return tokens


# ══════════════════════════════════════════════════════════════════════════════
# INTENT PATTERNS  (Regular Expressions — Lecture 2)
# Every pattern uses re syntax taught in class.
# ══════════════════════════════════════════════════════════════════════════════
INTENTS = {
    # ── Greetings ─────────────────────────────────────────────────────────────
    "greeting": {
        "patterns": [
            r"\b(hi|hello|hey|howdy|greetings|salaam|assalam)\b",
            r"\bgood\s+(morning|afternoon|evening|day)\b",
        ],
        "responses": [
            "Hello! 👋 I'm **StudyBot**, your NLP course assistant.\n\nI can help you with:\n- **Edit Distance & Spell Correction** (Lecture 3)\n- **Regular Expressions** (Lecture 2)\n- **Tokenization & Preprocessing** (Lecture 2)\n- **NLTK Code Examples** and Lab tasks\n- **NLP Career Guidance**\n\nWhat would you like to explore?",
            "Hey there! Great to see you. Ask me anything about your NLP course — theory, code, or career paths! 🚀",
        ],
    },

    # ── Edit Distance ──────────────────────────────────────────────────────────
    "edit_distance": {
        "patterns": [
            r"\b(edit\s+distance|levenshtein|minimum\s+edit)\b",
            r"\b(string\s+similarity|string\s+distance)\b",
            r"\bhow\s+(similar|close)\s+are\s+(two\s+)?strings\b",
        ],
        "responses": [
            "## ✏️ Edit Distance (Levenshtein)\n\n**Definition:** Minimum number of edit operations to transform one string into another.\n\n**Three operations:**\n| Operation | Cost |\n|-----------|------|\n| Insertion | 1 |\n| Deletion | 1 |\n| Substitution | 2 |\n\n**Classic example from lecture:** `INTENTION → EXECUTION`\n\n```python\ndef edit_distance(s1, s2):\n    m, n = len(s1), len(s2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n\n    # Base cases\n    for i in range(m+1): dp[i][0] = i\n    for j in range(n+1): dp[0][j] = j\n\n    # Fill DP table\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if s1[i-1] == s2[j-1]:\n                dp[i][j] = dp[i-1][j-1]  # no cost\n            else:\n                dp[i][j] = min(\n                    dp[i-1][j]   + 1,  # delete\n                    dp[i][j-1]   + 1,  # insert\n                    dp[i-1][j-1] + 2   # substitute\n                )\n    return dp[m][n]\n\nprint(edit_distance('graffe', 'giraffe'))  # → 2\n```\n\n💡 **Key insight:** Dynamic programming avoids recomputing sub-problems — exactly what was shown in Figure 2.18 of your lecture!",
        ],
    },

    # ── Noisy Channel ─────────────────────────────────────────────────────────
    "noisy_channel": {
        "patterns": [
            r"\b(noisy\s+channel|noise\s+channel)\b",
            r"\b(spell\s+(check|correction|corrector))\b",
            r"\b(bayes|bayesian)\s+(spell|correction|inference)\b",
            r"\bchannel\s+model\b",
        ],
        "responses": [
            "## 📡 Noisy Channel Model\n\n**Idea:** A misspelled word is an original word 'corrupted' by a noisy channel.\n\nWe recover the most likely original word `w` given the observed (noisy) word `x`:\n\n```\nŵ = argmax P(w|x)\n       w\n\n   = argmax P(x|w) × P(w)    ← Bayes' Rule\n       w    ─────────────────────\n           Channel    Language\n           Model      Model\n           (error     (word\n           probs)     frequency)\n```\n\n**P(x|w)** — how likely is this typo given the correct word?\n→ Use a confusion matrix (del[], ins[], sub[], trans[])\n\n**P(w)** — how frequent is this word?\n→ Count from a corpus: `P(w) = count(w) / N`\n\n**Example:** 'acress' → candidates scored:\n| Candidate | P(x|w) | P(w) | Final Score |\n|-----------|--------|------|-------------|\n| actress | 0.000117 | 0.0000231 | **2.7** ✅ |\n| across | 0.0000093 | 0.000299 | 2.8 |\n\n```python\n# Simplified implementation\ndef noisy_channel_correct(word, vocab, corpus_freq):\n    candidates = [w for w in vocab\n                  if edit_distance(word, w) <= 1]\n    return max(candidates,\n               key=lambda w: channel_prob(word, w) * corpus_freq[w])\n```\n\n💡 **Context matters!** Using a bigram language model P(w|prev_word) dramatically improves accuracy.",
        ],
    },

    # ── Regular Expressions ────────────────────────────────────────────────────
    "regex": {
        "patterns": [
            r"\b(regex|regular\s+expression|regexp)\b",
            r"\bpattern\s+match(ing)?\b",
            r"\bre\.(sub|search|findall|match|compile)\b",
        ],
        "responses": [
            "## 🔍 Regular Expressions\n\n**Core operators from Lecture 2:**\n\n| Operator | Meaning | Example | Matches |\n|----------|---------|---------|--------|\n| `.` | Any char | `b.g` | bag, big, bug |\n| `*` | 0 or more | `go*d` | gd, god, good |\n| `+` | 1 or more | `go+d` | god, good |\n| `?` | Optional | `colou?r` | color, colour |\n| `[abc]` | Char class | `[aeiou]` | a, e, i, o, u |\n| `[^abc]` | Negation | `[^0-9]` | non-digit |\n| `^` | Start | `^Hello` | line starts with Hello |\n| `$` | End | `done$` | line ends with done |\n| `\\d` | Digit | `\\d{4}` | 2024 |\n| `\\w` | Word char | `\\w+` | words |\n| `\\b` | Word boundary | `\\bthe\\b` | exact 'the' |\n\n**Python examples:**\n```python\nimport re\n\n# Extract emails\ntext = 'Contact info@gmail.com or support@yahoo.com'\nemails = re.findall(r'\\S+@\\S+', text)\nprint(emails)  # ['info@gmail.com', 'support@yahoo.com']\n\n# Remove punctuation\nclean = re.sub(r'[^\\w\\s]', '', 'Hello, world!')\nprint(clean)   # 'Hello world'\n\n# Detect phone numbers\nnums = re.findall(r'\\d{4}-\\d{7}', '0301-1234567')\n\n# ELIZA-style chatbot rule\nif re.search(r'.* I AM (DEPRESSED|SAD) .*', text):\n    print('I AM SORRY TO HEAR YOU ARE', match.group(1))\n```\n\n💡 **Capture groups** `(.*)` let you extract and reuse matched text — the core trick behind ELIZA!",
        ],
    },

    # ── Tokenization ──────────────────────────────────────────────────────────
    "tokenization": {
        "patterns": [
            r"\btokeniz(e|ation|ing|er)\b",
            r"\b(word|sentence|ngram|n-gram)\s+tokeniz\w*\b",
            r"\bsplit\s+(text|sentence|words)\b",
            r"\bsent_tokenize|word_tokenize\b",
        ],
        "responses": [
            "## 🔤 Tokenization\n\nTokenization splits text into smaller units (tokens) for analysis.\n\n**Hierarchy:** `Corpus → Documents → Sentences → Words`\n\n---\n\n**1. Sentence Tokenization**\n```python\nfrom nltk.tokenize import sent_tokenize\n\ntext = 'NLP is fascinating. I love it!'\nsentences = sent_tokenize(text)\n# ['NLP is fascinating.', 'I love it!']\n```\n\n**2. Word Tokenization**\n```python\nfrom nltk.tokenize import word_tokenize\n\ntokens = word_tokenize('Hi Mr. Smith! I\\'m going.')\n# ['Hi', 'Mr.', 'Smith', '!', 'I', \"'m\", 'going', '.']\n# Note: handles abbreviations and contractions!\n```\n\n**3. N-gram Tokenization**\n```python\nfrom nltk.util import ngrams\n\ntokens = word_tokenize('I love NLP')\nbigrams = list(ngrams(tokens, 2))\n# [('I', 'love'), ('love', 'NLP')]\n\ntrigrams = list(ngrams(tokens, 3))\n# [('I', 'love', 'NLP')]\n```\n\n💡 **Bigrams** are essential for language models — each word's probability depends on the previous word: `P(word | prev_word)`",
        ],
    },

    # ── Stemming & Lemmatization ───────────────────────────────────────────────
    "stemming": {
        "patterns": [
            r"\b(stem(ming|mer)?|lemma(tization|tize|tizer)?)\b",
            r"\broot\s+(form|word)\b",
            r"\bmorpholog(y|ical)\b",
            r"\bporter\s+stemmer\b",
        ],
        "responses": [
            "## 🌱 Stemming vs Lemmatization\n\n| Feature | Stemming | Lemmatization |\n|---------|----------|---------------|\n| Method | Chop affixes | Morphological parse |\n| Speed | ⚡ Fast | 🐢 Slower |\n| Accuracy | Lower | Higher |\n| Output | Root (may not be real word) | Actual dictionary word |\n| Example | `automat` | `automate` |\n\n**Stemming (Porter / Lancaster):**\n```python\nfrom nltk.stem.lancaster import LancasterStemmer\n\nstemmer = LancasterStemmer()\nwords = ['Running', 'runs', 'runner', 'Easily']\nprint([stemmer.stem(w) for w in words])\n# ['run', 'run', 'run', 'easy']\n\n# Porter rules (from lecture):\n# ATIONAL → ATE  (relational → relate)\n# ING → ε         (motoring → motor)\n# SSES → SS       (grasses → grass)\n```\n\n**Lemmatization:**\n```python\nfrom nltk.stem import WordNetLemmatizer\nnltk.download('wordnet')\n\nlemmatizer = WordNetLemmatizer()\nprint(lemmatizer.lemmatize('better', pos='a'))  # good\nprint(lemmatizer.lemmatize('running', pos='v')) # run\n```\n\n💡 For **search engines** → use stemming (speed matters). For **chatbots / NLU** → use lemmatization (meaning matters)!",
        ],
    },

    # ── Dynamic Programming ────────────────────────────────────────────────────
    "dynamic_programming": {
        "patterns": [
            r"\bdynamic\s+programm(ing|er)\b",
            r"\bdp\s+(table|matrix|approach)\b",
            r"\bmemoiz(e|ation)\b",
            r"\bbacktrace|back\s+trace\b",
        ],
        "responses": [
            "## 📊 Dynamic Programming in NLP\n\n**Core principle (from lecture):** If node X is on the optimal path A→B, then the path A→X must also be optimal.\n\n→ **Store** sub-problem solutions instead of recomputing them!\n\n**DP Table for Edit Distance:**\n```\n      #  e  x  e  c  u  t  i  o  n\n  #   0  1  2  3  4  5  6  7  8  9\n  i   1  2  3  4  5  6  7  6  7  8\n  n   2  3  4  5  6  7  8  7  8  7\n  t   3  4  5  6  7  8  7  8  9  8\n  e   4  3  4  5  6  7  8  9 10  9\n  ...\n  n   9  8  9 10 11 12 11 10  9  8 ← answer!\n```\n\n**Recurrence relation:**\n```python\nif s1[i-1] == s2[j-1]:\n    dp[i][j] = dp[i-1][j-1]        # diagonal — match, free!\nelse:\n    dp[i][j] = min(\n        dp[i-1][j]   + 1,           # ↑ deletion\n        dp[i][j-1]   + 1,           # ← insertion\n        dp[i-1][j-1] + 2            # ↖ substitution\n    )\n```\n\n**Backtrace** — follow arrows from `dp[m][n]` back to `dp[0][0]` to reconstruct the actual edit path (Figure 2.19 in your lecture)!\n\n💡 Also used in: Viterbi (HMM), CYK parsing, sequence alignment in bioinformatics!",
        ],
    },

    # ── Stop Words ────────────────────────────────────────────────────────────
    "stopwords": {
        "patterns": [
            r"\bstop\s*words?\b",
            r"\b(remove|filter|eliminate)\s+(common|frequent)\s+words?\b",
        ],
        "responses": [
            "## 🛑 Stop Words\n\n**Stop words** are frequent, low-semantic-value words — removing them reduces noise.\n\n**Examples:** `is, the, and, in, of, to, a, an, was, were...` (~179 in NLTK)\n\n```python\nfrom nltk.corpus import stopwords\nfrom nltk.tokenize import word_tokenize\n\nstop_words = set(stopwords.words('english'))\nprint(f'Stop word count: {len(stop_words)}')\n\ntext = 'This movie is very good and interesting'\ntokens = word_tokenize(text)\nfiltered = [w for w in tokens\n            if w.lower() not in stop_words]\nprint(filtered)  # ['movie', 'good', 'interesting']\n```\n\n⚠️ **When NOT to remove stop words:**\n| Task | Reason |\n|------|--------|\n| Sentiment Analysis | 'not bad' — 'not' is critical! |\n| Question Answering | 'who', 'what', 'when' carry meaning |\n| Machine Translation | Every word matters |\n\n💡 Consider creating **domain-specific** stop word lists — for medical text, generic lists may remove important clinical terms!",
        ],
    },

    # ── NLTK Setup ────────────────────────────────────────────────────────────
    "nltk_setup": {
        "patterns": [
            r"\b(how\s+to\s+(install|setup|use|import)\s+nltk)\b",
            r"\bnltk\.download\b",
            r"\b(install|setup)\s+nltk\b",
        ],
        "responses": [
            "## 🛠️ NLTK Setup Guide\n\n**Step 1: Install**\n```bash\npip install nltk\n```\n\n**Step 2: Download corpora**\n```python\nimport nltk\n\nresources = ['punkt', 'punkt_tab', 'stopwords',\n             'wordnet', 'twitter_samples']\nfor r in resources:\n    nltk.download(r)\n```\n\n**Step 3: Full preprocessing pipeline**\n```python\nimport re, nltk\nfrom nltk.tokenize import word_tokenize, sent_tokenize\nfrom nltk.corpus import stopwords\nfrom nltk.stem.lancaster import LancasterStemmer\n\nstop_words = set(stopwords.words('english'))\nstemmer = LancasterStemmer()\n\ndef full_pipeline(text):\n    # 1. Remove HTML tags\n    text = re.sub(r'<.*?>', '', text)\n    # 2. Remove special characters\n    text = re.sub(r'[^\\w\\s]', '', text)\n    # 3. Lowercase\n    text = text.lower()\n    # 4. Tokenize\n    tokens = word_tokenize(text)\n    # 5. Remove stop words + stem\n    clean = [stemmer.stem(t) for t in tokens\n             if t not in stop_words and len(t) > 1]\n    return clean\n\nprint(full_pipeline('NLP is amazing! I love learning it.'))\n# ['nlp', 'amaz', 'lov', 'learn']\n```\n\n💡 Google Colab = zero install headaches. Run `!pip install nltk` and start immediately!",
        ],
    },

    # ── Assignment / Lab Help ─────────────────────────────────────────────────
    "assignment_help": {
        "patterns": [
            r"\b(assignment|homework|lab|task|project)\b",
            r"\bpost\s+lab\b",
            r"\bimdb\s+(dataset|reviews?)\b",
            r"\beliza\s+chatbot\b",
        ],
        "responses": [
            "## 📝 Lab Assignment Help\n\n**Lab 2 — IMDB Dataset Processing:**\n\n```python\nimport os, re\nfrom nltk.tokenize import word_tokenize\nfrom nltk.corpus import stopwords\nfrom nltk.stem import LancasterStemmer\nimport urllib.request, tarfile\n\n# Step 1: Download IMDB dataset\nurl = 'https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz'\nurllib.request.urlretrieve(url, 'imdb.tar.gz')\nwith tarfile.open('imdb.tar.gz') as tar:\n    tar.extractall()\n\n# Step 2: Preprocessing pipeline\nstop_words = set(stopwords.words('english'))\nstemmer = LancasterStemmer()\n\ndef preprocess(text):\n    text = re.sub(r'<.*?>', '', text)    # strip HTML\n    text = re.sub(r'[^\\w\\s]', '', text)  # remove punct\n    text = text.lower()\n    tokens = word_tokenize(text)\n    return [stemmer.stem(t) for t in tokens\n            if t not in stop_words and len(t) > 2]\n\n# Step 3: Extract opinion phrases (task from lecture!)\ndef extract_opinions(text):\n    loves = re.findall(r'i love (.*?)[\\.!,]', text, re.I)\n    hates = re.findall(r'i hate (.*?)[\\.!,]', text, re.I)\n    return {'loves': loves, 'hates': hates}\n\n# Step 4: Dataset statistics\ndef dataset_stats(folder):\n    files = os.listdir(folder)\n    lengths = []\n    for f in files[:100]:  # sample 100\n        with open(f'{folder}/{f}', encoding='utf-8') as fp:\n            lengths.append(len(fp.read().split()))\n    print(f'Avg review length: {sum(lengths)/len(lengths):.0f} words')\n```\n\nNeed help with a specific part? Ask me!",
        ],
    },

    # ── Evaluation Metrics ────────────────────────────────────────────────────
    "evaluation": {
        "patterns": [
            r"\b(precision|recall|f1|f-score|accuracy)\b",
            r"\bconfusion\s+matrix\b",
            r"\b(evaluat(e|ion)|benchmark)\s+(model|classifier|nlp)\b",
        ],
        "responses": [
            "## 📊 NLP Evaluation Metrics\n\n**Confusion Matrix:**\n```\n            Predicted\n            Pos    Neg\nActual Pos [  TP |  FN ]\n       Neg [  FP |  TN ]\n```\n\n**Metrics:**\n```python\n# Accuracy — overall correct predictions\naccuracy  = (TP + TN) / (TP + TN + FP + FN)\n\n# Precision — of predicted positives, how many right?\nprecision = TP / (TP + FP)\n\n# Recall (Sensitivity) — of actual positives, how many found?\nrecall    = TP / (TP + FN)\n\n# F1 Score — harmonic mean (balances precision & recall)\nf1 = 2 * (precision * recall) / (precision + recall)\n```\n\n**Confusion matrix in sklearn:**\n```python\nfrom sklearn.metrics import classification_report, confusion_matrix\n\nprint(classification_report(y_true, y_pred,\n      target_names=['negative', 'positive']))\n```\n\n💡 **Which metric to prioritize?**\n| Scenario | Metric |\n|----------|--------|\n| Spam detection | Precision (don't block legit emails) |\n| Cancer diagnosis | Recall (don't miss cases) |\n| Balanced | F1 Score |",
        ],
    },

    # ── Career Guidance ───────────────────────────────────────────────────────
    "career": {
        "patterns": [
            r"\b(career|job|internship)\s+(in\s+)?(nlp|ai|ml|data\s+science)\b",
            r"\bhow\s+to\s+become\s+an?\s+(nlp|ai|ml)\b",
            r"\bskills?\s+(for|needed|required)\s+(nlp|ai|ml)\b",
            r"\bjob\s+market\s+(for\s+)?nlp\b",
        ],
        "responses": [
            "## 🚀 NLP Career Roadmap\n\n**Foundation Skills:**\n```\nPython → NLTK/spaCy → ML (scikit-learn) → DL (PyTorch)\n   ↓                                              ↓\nText Processing                        Transformers (BERT, GPT)\n```\n\n**Build These Portfolio Projects:**\n1. 🎬 **Sentiment Analyzer** — IMDB reviews (you're doing this in lab!)\n2. 📄 **Resume Parser** — NER to extract name, skills, education\n3. 🤖 **Fine-tuned BERT** — question answering on custom dataset\n4. 🔍 **Semantic Search** — sentence embeddings + cosine similarity\n5. 💬 **Chatbot** — rule-based (you're doing this!) + ML-based\n\n**Top Companies Hiring NLP Engineers:**\n`OpenAI` · `Google DeepMind` · `Anthropic` · `HuggingFace` · `Microsoft` · `Amazon` · `Meta AI`\n\n**Salary Ranges (2024):**\n| Role | Range |\n|------|-------|\n| NLP Engineer | $120k–$200k |\n| Research Scientist | $150k–$300k |\n| ML Engineer | $130k–$220k |\n\n💡 **Best signal:** Open-source contributions on GitHub. Even small PRs to HuggingFace Transformers stand out!",
        ],
    },

    # ── What is NLP ───────────────────────────────────────────────────────────
    "what_is_nlp": {
        "patterns": [
            r"\bwhat\s+is\s+nlp\b",
            r"\bwhat\s+is\s+natural\s+language\s+processing\b",
            r"\b(explain|define|describe)\s+nlp\b",
            r"\bintroduction\s+to\s+nlp\b",
        ],
        "responses": [
            "## 🧠 What is NLP?\n\n**Natural Language Processing** is a field of AI that enables computers to understand, analyze, and generate human language — text or speech.\n\n**It combines:**\n- 📚 **Linguistics** — grammar, semantics, pragmatics\n- 🤖 **Machine Learning** — statistical models\n- 💻 **Computer Science** — algorithms & data structures\n\n**Real-world applications:**\n| Application | Examples |\n|-------------|----------|\n| 💬 Chatbots | ChatGPT, Siri, Alexa |\n| 🌐 Translation | Google Translate |\n| 😊 Sentiment | Amazon review analysis |\n| 📧 Spam Filter | Gmail |\n| 🔍 Search | Google, Bing |\n| 📝 Summarization | News apps |\n| 🎤 Speech | Siri, Google Assistant |\n\n**Standard NLP Pipeline:**\n```\nRaw Text\n   ↓  Cleaning (regex, HTML removal)\nPreprocessed Text\n   ↓  Tokenization + Stop word removal + Stemming\nTokens\n   ↓  Feature Extraction (TF-IDF, Embeddings)\nVectors\n   ↓  Model (Naive Bayes, BERT, GPT)\nPrediction / Output\n```\n\n💡 **Fun fact:** ELIZA (1966) — the first chatbot — used simple regex substitutions, exactly like what you built in Lab 2!",
        ],
    },

    # ── Help ──────────────────────────────────────────────────────────────────
    "help": {
        "patterns": [
            r"\b(help|assist|guide|support)\b",
            r"\bwhat\s+can\s+you\s+do\b",
            r"\bwhat\s+do\s+you\s+know\b",
            r"\btopics?\b",
        ],
        "responses": [
            "## 📚 StudyBot — What I Can Help With\n\n**📖 NLP Theory (from your lectures)**\n- Edit Distance & Levenshtein Algorithm\n- Noisy Channel Model & Spell Correction\n- Regular Expressions with examples\n- Tokenization (word, sentence, n-grams)\n- Stemming & Lemmatization\n- Stop Words & Preprocessing Pipeline\n- Dynamic Programming for NLP\n\n**💻 Code & Tools**\n- NLTK setup and full usage guide\n- Python NLP code examples\n- IMDB dataset processing\n- Building chatbots with regex\n- Evaluation metrics with sklearn\n\n**🎓 Academic Support**\n- Lab 1 & Lab 2 help\n- Assignment walkthrough\n- Concept explanations with examples\n\n**🚀 Career & Industry**\n- NLP career paths & salaries\n- Portfolio project ideas\n- Top companies & skills needed\n\n*Try asking:* **'Explain edit distance with code'** or **'Help me with the IMDB assignment'**",
        ],
    },

    # ── Thanks ────────────────────────────────────────────────────────────────
    "thanks": {
        "patterns": [
            r"\b(thanks|thank\s+you|thankyou|thx|ty)\b",
            r"\b(helpful|great|awesome|perfect|brilliant)\b",
        ],
        "responses": [
            "You're welcome! 😊 Keep experimenting — the best NLP engineers learn by building. Need anything else?",
            "Glad that helped! 🚀 Remember: every line of code you write is progress. Anything else on your mind?",
            "Happy to help! NLP is a fantastic field — you're learning the foundations that power ChatGPT and Google Translate. Keep going! 💪",
        ],
    },

    # ── Bye ───────────────────────────────────────────────────────────────────
    "bye": {
        "patterns": [
            r"\b(bye|goodbye|see\s+you|take\s+care|quit|exit|later|cya)\b",
        ],
        "responses": [
            "Goodbye! Best of luck with your NLP journey! 👋 *Every expert was once a beginner.*",
            "See you! Keep coding, keep learning. NLP is the future — and you're part of it! 🌟",
        ],
    },
}

# ── Fallbacks ─────────────────────────────────────────────────────────────────
FALLBACKS = [
    "Hmm, I'm not sure about that one. Try asking about:\n\n- **Edit distance** or spell correction\n- **Regular expressions** with Python examples\n- **Tokenization** and preprocessing\n- **Stemming** vs lemmatization\n- **NLP career guidance**\n\nOr type **'help'** to see everything I can do!",
    "That's outside my current knowledge. Try rephrasing, or ask about NLP topics like **regex**, **edit distance**, or **NLTK setup**!",
    "I specialize in NLP course topics! Ask me about **tokenization**, **noisy channel model**, or **Python NLTK code** — I'll give a detailed answer with examples.",
]

# ── Suggestions map ───────────────────────────────────────────────────────────
SUGGESTIONS = {
    "greeting":          ["What is NLP?", "Explain edit distance", "Show regex examples", "NLP career path"],
    "edit_distance":     ["Noisy channel model", "Dynamic programming", "Spell correction example", "Tokenization"],
    "noisy_channel":     ["Edit distance algorithm", "Confusion matrix", "Regex pattern matching", "Evaluation metrics"],
    "regex":             ["Python re module", "Build chatbot with regex", "Text preprocessing pipeline", "Capture groups"],
    "tokenization":      ["Stop word removal", "Stemming vs lemmatization", "N-gram models", "Preprocessing pipeline"],
    "stemming":          ["Tokenization methods", "Stop words", "Lemmatization vs stemming", "NLTK setup"],
    "dynamic_programming": ["Edit distance code", "Backtrace algorithm", "Noisy channel model"],
    "stopwords":         ["Tokenization", "Stemming", "Full preprocessing pipeline", "NLTK setup"],
    "nltk_setup":        ["Tokenization guide", "Stemming code", "IMDB dataset task", "Stop words"],
    "assignment_help":   ["IMDB preprocessing", "Regex for chatbot", "Spell correction code", "Evaluation metrics"],
    "evaluation":        ["Classification metrics", "Confusion matrix code", "NLP career paths"],
    "career":            ["Portfolio projects", "NLTK setup guide", "Assignment help", "What is NLP?"],
    "what_is_nlp":       ["NLP applications", "Text preprocessing", "Edit distance", "NLP career path"],
    "help":              ["Edit distance", "Regular expressions", "Tokenization", "Career guidance"],
}
DEFAULT_SUGGESTIONS = ["Edit distance", "Regular expressions", "Tokenization", "NLP career"]


# ══════════════════════════════════════════════════════════════════════════════
# INTENT CLASSIFICATION  (regex-first, then keyword fallback)
# ══════════════════════════════════════════════════════════════════════════════
def classify_intent(text: str) -> Tuple[str, float]:
    text_lower = text.lower()

    # Primary: direct regex match on raw input
    for intent, data in INTENTS.items():
        for pat in data["patterns"]:
            if re.search(pat, text_lower):
                return intent, 1.0

    # Fallback: preprocess then try again
    tokens = preprocess(text)
    joined = " ".join(tokens)
    for intent, data in INTENTS.items():
        for pat in data["patterns"]:
            if re.search(pat, joined):
                return intent, 0.75

    return "unknown", 0.0


def get_response(user_text: str) -> dict:
    intent, confidence = classify_intent(user_text)

    if intent != "unknown":
        message = random.choice(INTENTS[intent]["responses"])
        suggestions = SUGGESTIONS.get(intent, DEFAULT_SUGGESTIONS)
    else:
        message = random.choice(FALLBACKS)
        suggestions = DEFAULT_SUGGESTIONS

    return {
        "message": message,
        "intent": intent,
        "confidence": round(confidence, 2),
        "suggestions": suggestions,
    }


# ══════════════════════════════════════════════════════════════════════════════
# API ROUTES
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    return jsonify(get_response(user_message))


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "bot": "StudyBot — NLP Course Assistant"})


# Fixed — listens on all interfaces, reachable from frontend container
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
