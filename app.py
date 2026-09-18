from flask import Flask, request, render_template_string
import re
from collections import Counter

app = Flask(__name__)

# Single-file HTML + CSS Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Smart Text Summarizer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #f0f2f5; color: #1c1e21; padding: 40px 15px; }
        .container { max-width: 850px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
        h1 { color: #1a73e8; font-size: 26px; margin-bottom: 8px; text-align: center; }
        p.subtitle { text-align: center; color: #5f6368; margin-bottom: 25px; font-size: 14px; }
        label { font-weight: 600; display: block; margin-bottom: 8px; font-size: 14px; }
        textarea { width: 100%; height: 160px; padding: 12px; border: 1px solid #dadce0; border-radius: 8px; font-size: 14px; outline: none; resize: vertical; }
        textarea:focus { border-color: #1a73e8; }
        .controls { display: flex; justify-content: space-between; align-items: center; margin-top: 15px; flex-wrap: wrap; gap: 10px; }
        select { padding: 8px 12px; border: 1px solid #dadce0; border-radius: 6px; outline: none; background: white; }
        button { background-color: #1a73e8; color: white; border: none; padding: 10px 24px; font-size: 15px; font-weight: 600; border-radius: 6px; cursor: pointer; transition: 0.2s; }
        button:hover { background-color: #1557b0; }
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 25px; }
        .stat-card { background: #f8f9fa; border: 1px solid #e8eaed; padding: 12px; border-radius: 8px; text-align: center; }
        .stat-card span { font-size: 20px; font-weight: bold; color: #1a73e8; display: block; }
        .stat-card label { font-size: 12px; color: #5f6368; margin-top: 4px; }
        .result-box { margin-top: 25px; padding: 20px; background-color: #e8f0fe; border-left: 5px solid #1a73e8; border-radius: 8px; }
        .result-box h3 { color: #174ea6; margin-bottom: 8px; font-size: 16px; }
        .result-box p { line-height: 1.6; font-size: 14.5px; color: #202124; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Summarizer & Analyzer</h1>
        <p class="subtitle">NLP-powered text reduction and key insights extractor</p>

        <form method="POST">
            <label for="input_text">Paste Text / Article below:</label>
            <textarea name="input_text" id="input_text" placeholder="Paste your article or long paragraph here..." required>{{ original_text }}</textarea>

            <div class="controls">
                <div>
                    <label style="display:inline; margin-right: 8px;">Summary Length:</label>
                    <select name="sentence_count">
                        <option value="2" {% if sentence_count == 2 %}selected{% endif %}>Short (2 Sentences)</option>
                        <option value="3" {% if sentence_count == 3 %}selected{% endif %}>Medium (3 Sentences)</option>
                        <option value="5" {% if sentence_count == 5 %}selected{% endif %}>Detailed (5 Sentences)</option>
                    </select>
                </div>
                <button type="submit">Analyze & Summarize</button>
            </div>
        </form>

        {% if summary %}
        <div class="stats-grid">
            <div class="stat-card">
                <span>{{ word_count }}</span>
                <label>Words Count</label>
            </div>
            <div class="stat-card">
                <span>{{ reading_time }} min</span>
                <label>Est. Reading Time</label>
            </div>
            <div class="stat-card">
                <span>{{ compression_ratio }}%</span>
                <label>Text Reduction</label>
            </div>
        </div>

        <div class="result-box">
            <h3>Generated Summary:</h3>
            <p>{{ summary }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def extract_summary(text, top_n=3):
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) <= top_n:
        return text
    
    # Common English stop words
    stop_words = set([
        "the", "is", "in", "and", "to", "a", "of", "it", "that", "on", "for", 
        "as", "are", "with", "this", "by", "at", "from", "be", "was", "an"
    ])
    
    # Word frequency calculation
    words = re.findall(r'\w+', text.lower())
    words = [w for w in words if w not in stop_words and len(w) > 2]
    freq = Counter(words)
    
    # Score sentences based on word frequency
    sentence_scores = {}
    for i, s in enumerate(sentences):
        score = 0
        s_words = re.findall(r'\w+', s.lower())
        for w in s_words:
            score += freq.get(w, 0)
        sentence_scores[i] = score / (len(s_words) + 1)
        
    # Get top sentences and keep original order
    top_indices = sorted(sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n])
    return " ".join([sentences[i] for i in top_indices])

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = ""
    original_text = ""
    sentence_count = 3
    word_count = 0
    reading_time = 0
    compression_ratio = 0
    
    if request.method == 'POST':
        original_text = request.form.get('input_text', '')
        sentence_count = int(request.form.get('sentence_count', 3))
        
        if original_text.strip():
            words = re.findall(r'\w+', original_text)
            word_count = len(words)
            reading_time = max(1, round(word_count / 200))
            
            summary = extract_summary(original_text, top_n=sentence_count)
            summary_words = len(re.findall(r'\w+', summary))
            compression_ratio = round((1 - (summary_words / max(word_count, 1))) * 100)

    return render_template_string(
        HTML_TEMPLATE, 
        original_text=original_text, 
        summary=summary, 
        sentence_count=sentence_count,
        word_count=word_count,
        reading_time=reading_time,
        compression_ratio=compression_ratio
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)