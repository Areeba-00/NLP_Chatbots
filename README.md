# 🤖 StudyBot — NLP Course Assistant

A rule-based chatbot built for the NLP course (AI-23, NUTECH).
Demonstrates techniques from **Lecture 2** (Regex, Tokenization, Preprocessing)
and **Lecture 3** (Edit Distance, Noisy Channel Spell Correction).

---

## 🎯 Use Case

**StudyBot** is an AI academic assistant that helps NLP students understand:
- Edit Distance & Levenshtein Algorithm
- Noisy Channel Model & Spell Correction
- Regular Expressions (with Python examples)
- Tokenization (word, sentence, n-grams)
- Stemming & Lemmatization
- Stop Words & Preprocessing Pipeline
- Dynamic Programming for NLP
- NLTK setup & usage
- Assignment & Lab help
- NLP Career Guidance

---

## 🏗️ Architecture

```
studybot/
├── backend/
│   ├── app.py          ← Flask API + NLP logic
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx     ← React chat UI
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🚀 Setup & Run

### Backend (Flask)

```bash
cd backend

# Install dependencies
pip install flask flask-cors nltk

# Run the server
python app.py
# → Running on http://localhost:5000
```

### Frontend (React)

```bash
cd frontend

# Install node dependencies
npm install

# Start dev server
npm run dev
# → Running on http://localhost:3000
```

Open **http://localhost:3000** in your browser.

---

## 🧠 NLP Techniques Used

### 1. Edit Distance (Lecture 3)
```python
def edit_distance(s1, s2):
    # DP table — O(m×n) time, O(m×n) space
    # Insert/Delete cost = 1, Substitute cost = 2
    dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+2)
```

### 2. Noisy Channel Spell Correction (Lecture 3)
```python
# ŵ = argmax P(x|w) × P(w)
#         Channel    Language
#          Model      Model
def spell_correct(word):
    return min(VOCAB, key=lambda w: edit_distance(word, w))
```

### 3. Regular Expressions (Lecture 2)
```python
# Intent detection via regex patterns
re.search(r'\b(edit\s+distance|levenshtein)\b', text)
re.search(r'\b(tokeniz|ngram|n-gram)\b', text)
```

### 4. Text Preprocessing Pipeline (Lecture 2)
```python
# Lowercase → Remove punct → Tokenize → Remove stops → Spell-correct
text.lower() → re.sub() → word_tokenize() → [w for w not in stops]
```

---

## 💬 API

### POST /api/chat
```json
Request:  { "message": "explain edit distance" }
Response: {
  "message": "## Edit Distance...\n...",
  "intent": "edit_distance",
  "confidence": 1.0,
  "suggestions": ["Noisy channel model", "Dynamic programming", ...]
}
```

### GET /api/health
```json
{ "status": "ok", "bot": "StudyBot — NLP Course Assistant" }
```

---

## 💡 Example Conversations

| You say | Bot responds |
|---------|-------------|
| "explain edit distance" | Full explanation with DP table + Python code |
| "what is noisy channel" | Bayes formula, confusion matrix, example |
| "show me regex" | All operators with examples |
| "help with imdb assignment" | Full preprocessing code walkthrough |
| "nlp career advice" | Roadmap, projects, top companies |
| "setup nltk" | Step-by-step install + code pipeline |

---

## 🎨 Features

- ✅ Markdown rendering (headers, code blocks, tables, lists)
- ✅ Typing indicator animation
- ✅ Quick-reply suggestion buttons
- ✅ Intent badge on each response
- ✅ Backend connectivity status
- ✅ Dark terminal-inspired UI
- ✅ Responsive & scrollable chat history
- ✅ Keyboard shortcuts (Enter to send)
