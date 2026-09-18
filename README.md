# 📝 Smart Text Summarizer & Content Analytics Web App

An end-to-end NLP-driven web application built with **Python (Flask)**, **HTML5**, and **CSS3** that performs extractive text summarization and content readability analytics on long-form articles.

![Project Status](https://img.shields.io/badge/Status-Live-success)
![Python Version](https://img.shields.io/badge/Python-3.x-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-black)

---

## 🌟 Key Features
- **Extractive Text Summarization:** Condenses long paragraphs into concise 2, 3, or 5-sentence summaries using frequency-based NLP scoring.
- **Content Metrics & Analytics:** Automatically computes word count, estimated reading time, and text compression percentage.
- **Dynamic User Interface:** Clean, responsive, and minimalist UI designed with custom CSS.
- **Production Deployment:** Containerized logic configured with Gunicorn for zero-downtime cloud hosting.

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **NLP Techniques:** Regular Expressions (Regex), Tokenization, Stop-word Filtering, Sentence Frequency Scoring
- **Frontend:** HTML5, Modern CSS3
- **Hosting & Deployment:** Render Cloud Platform

---

## 🚀 How It Works
1. **Preprocessing:** Strips common English stop-words and tokenizes the raw text into distinct sentences and words.
2. **Frequency Scoring:** Builds a normalized term-frequency map for key contextual words.
3. **Sentence Ranking:** Scores sentences based on keyword concentration and returns the highest-ranking sentences in sequential order.

---

## 💻 Local Setup & Installation

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/NLP--text-summarizer.git](https://github.com/YOUR_GITHUB_USERNAME/NLP--text-summarizer.git)

# 2. Navigate to project directory
cd NLP--text-summarizer

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
