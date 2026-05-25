import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(120, 40, 255, 0.25), transparent),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0, 200, 150, 0.1), transparent);
    min-height: 100vh;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}

.hero-badge {
    display: inline-block;
    background: rgba(120, 40, 255, 0.15);
    border: 1px solid rgba(120, 40, 255, 0.4);
    color: #a855f7;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-size: clamp(2.2rem, 6vw, 3.5rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin: 0 0 0.6rem;
    letter-spacing: -0.03em;
}

.hero-title span {
    background: linear-gradient(135deg, #a855f7 0%, #06d6a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    color: rgba(255,255,255,0.45);
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.02em;
}

/* ── Card ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem 2rem 1.5rem;
    margin: 2rem 0 1.5rem;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(168,85,247,0.3), rgba(6,214,160,0.15), transparent);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}

.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(168,85,247,0.7);
    margin-bottom: 0.75rem;
}

/* ── Result Boxes ── */
.result-spam {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(220,38,38,0.05));
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    animation: fadeSlide 0.5s ease;
}

.result-ham {
    background: linear-gradient(135deg, rgba(6,214,160,0.12), rgba(16,185,129,0.05));
    border: 1px solid rgba(6,214,160,0.35);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    animation: fadeSlide 0.5s ease;
}

.result-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.result-label {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0.3rem 0 0.5rem;
}

.result-spam .result-label { color: #f87171; }
.result-ham  .result-label { color: #34d399; }

.result-desc {
    font-size: 0.9rem;
    font-family: 'Space Mono', monospace;
    opacity: 0.55;
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align: center;
}

.stat-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: #a855f7;
    letter-spacing: -0.02em;
    line-height: 1;
}

.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: rgba(255,255,255,0.3);
    margin-top: 0.3rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.18);
}

/* ── Animations ── */
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Override Streamlit Textarea ── */
textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}
textarea:focus {
    border-color: rgba(168,85,247,0.5) !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.1) !important;
}

/* ── Override Streamlit Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 24px rgba(120,40,255,0.35) !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(120,40,255,0.5) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 720px; }

/* ── Text area label ── */
label { color: rgba(255,255,255,0.5) !important; font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── NLTK Downloads ───────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def download_nltk():
    nltk.download("punkt",       quiet=True)
    nltk.download("punkt_tab",   quiet=True)
    nltk.download("stopwords",   quiet=True)

download_nltk()

# ─── Load Model & Vectorizer ──────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    tfidf = pickle.load(open("vectorizer.pkl", "rb"))
    model = pickle.load(open("model.pkl",      "rb"))
    return tfidf, model

tfidf, model = load_artifacts()

# ─── Text Preprocessing ───────────────────────────────────────────────────────
ps = PorterStemmer()

def transform_text(text: str) -> str:
    text   = text.lower()
    tokens = nltk.word_tokenize(text)
    stops  = set(stopwords.words("english"))
    puncts = set(string.punctuation)

    cleaned = [
        ps.stem(tok)
        for tok in tokens
        if tok.isalnum() and tok not in stops and tok not in puncts
    ]
    return " ".join(cleaned)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🛡️ &nbsp; AI-Powered Detection</div>
  <h1 class="hero-title">SMS <span>Spam</span> Detector</h1>
  <p class="hero-sub">Paste any message — know instantly if it's spam or safe.</p>
</div>
""", unsafe_allow_html=True)

# ─── Input Card ───────────────────────────────────────────────────────────────
st.markdown('<div class="card"><p class="card-label">📩 &nbsp; Message Input</p>', unsafe_allow_html=True)

sms_input = st.text_area(
    label="Enter your SMS message below",
    placeholder="Type or paste an SMS message here…\n\nExample: Congratulations! You've won a FREE iPhone. Click now to claim your prize!",
    height=160,
    label_visibility="collapsed",
)

analyze = st.button("Analyze Message →")
st.markdown("</div>", unsafe_allow_html=True)

# ─── Result ───────────────────────────────────────────────────────────────────
if analyze:
    if not sms_input.strip():
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing…"):
            transformed  = transform_text(sms_input)
            vectorized   = tfidf.transform([transformed])
            prediction   = model.predict(vectorized)[0]
            proba        = model.predict_proba(vectorized)[0]

        spam_conf = round(proba[1] * 100, 1)
        ham_conf  = round(proba[0] * 100, 1)
        word_cnt  = len(sms_input.split())
        char_cnt  = len(sms_input)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-spam">
                <div class="result-icon">🚨</div>
                <div class="result-label">SPAM</div>
                <div class="result-desc">Confidence: {spam_conf}% spam probability</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-ham">
                <div class="result-icon">✅</div>
                <div class="result-label">NOT SPAM</div>
                <div class="result-desc">Confidence: {ham_conf}% legitimate probability</div>
            </div>
            """, unsafe_allow_html=True)

        # Stats chips
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-chip">
                <div class="stat-value">{spam_conf}%</div>
                <div class="stat-label">Spam Score</div>
            </div>
            <div class="stat-chip">
                <div class="stat-value">{ham_conf}%</div>
                <div class="stat-label">Safe Score</div>
            </div>
            <div class="stat-chip">
                <div class="stat-value">{word_cnt}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-chip">
                <div class="stat-value">{char_cnt}</div>
                <div class="stat-label">Chars</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Powered by Multinomial Naive Bayes · TF-IDF Vectorizer · NLTK
</div>
""", unsafe_allow_html=True)