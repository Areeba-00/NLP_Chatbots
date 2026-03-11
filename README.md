# 🤖 StudyBot — NLP Course Assistant

An AI-powered study assistant for the **NUTECH AI-23 NLP Course**, built with Flask + NLTK (backend) and React + Vite (frontend), fully containerized with Docker.

---

## ✨ Features

- 💬 Interactive chat interface with intent-based responses
- 📚 Covers **Edit Distance**, **Regex**, **Tokenization**, **Stemming**, **Noisy Channel Model** and more
- 🔍 Built-in **spell correction** using Levenshtein distance
- 🧹 Full **NLP preprocessing pipeline** (tokenization → stop word removal → spell correction)
- 🚀 NLP career guidance and lab assignment help
- 🐳 Fully Dockerized — one command to run

---

## 🚀 Quick Start

### Prerequisites

Make sure you have installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Git](https://git-scm.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Areeba-00/NLP_Chatbots.git
cd NLP_Chatbots
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

That's it! 🎉

---

### 3. Open in Browser

Once you see this in the terminal:

```
studybot-frontend  |   ➜  Local:   http://localhost:5173/
studybot-backend   |  * Running on http://0.0.0.0:5000
```

Open your browser and go to:

```
http://localhost:5173
```

---

## 🛑 Stopping the App

Press `Ctrl + C` in the terminal, then run:

```bash
docker compose down
```

---

## 🗂️ Project Structure

```
NLP_Chatbots/
├── backend/
│   ├── app.py              # Flask API + NLP logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/                # React components
│   ├── vite.config.js      # Vite + proxy config
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🧠 NLP Techniques Used

| Technique | Lecture | Description |
|-----------|---------|-------------|
| Regular Expressions | Lecture 2 | Intent classification via `re` patterns |
| Tokenization | Lecture 2 | NLTK `word_tokenize` |
| Stop Word Removal | Lecture 2 | NLTK stopwords corpus |
| Edit Distance | Lecture 3 | Levenshtein dynamic programming algorithm |
| Noisy Channel Model | Lecture 3 | Bayesian spell correction |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send a message, get a response |
| `GET` | `/api/health` | Health check |

**Example request:**
```json
POST /api/chat
{ "message": "Explain edit distance" }
```

---

## 👨‍💻 Built With

- **Backend:** Python, Flask, NLTK, Flask-CORS
- **Frontend:** React, Vite, Tailwind CSS
- **Infrastructure:** Docker, Docker Compose
