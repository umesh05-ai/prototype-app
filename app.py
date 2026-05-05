import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
import re

# Page config
st.set_page_config(page_title="AI Plagiarism Detector", layout="centered")

st.title("📄 Plagiarism & AI Content Detector")

# Input options
option = st.radio("Choose input type:", ["Paste Text", "Upload File"])

text = ""

# --- INPUT SECTION ---
if option == "Paste Text":
    text = st.text_area("Enter your text here:")
else:
    file = st.file_uploader("Upload file (.txt or .docx)", type=["txt", "docx"])

    if file:
        # Handle TXT
        if file.type == "text/plain":
            text = file.read().decode("utf-8")

        # Handle DOCX
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])

# --- ANALYZE BUTTON ---
if st.button("🔍 Analyze"):
    if text:

        # -------------------------
        # 🔍 PLAGIARISM DETECTION
        # -------------------------
        reference_texts = [
            "Artificial Intelligence is transforming the world.",
            "Machine learning is a subset of AI.",
            "Plagiarism is unethical in academics.",
            "Data science involves statistics and programming."
        ]

        documents = [text] + reference_texts

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(documents)

        similarity_matrix = cosine_similarity(vectors)
        plagiarism_score = round(max(similarity_matrix[0][1:]) * 100, 2)
        originality_score = round(100 - plagiarism_score, 2)

        # -------------------------
        # 🤖 AI DETECTION
        # -------------------------
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        avg_len = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        repetition_ratio = len(set(sentences)) / max(len(sentences), 1)

        if avg_len > 15 and repetition_ratio < 0.7:
            ai_result = "⚠️ High probability of AI-generated content"
        elif avg_len > 10:
            ai_result = "⚠️ Medium probability of AI-generated content"
        else:
            ai_result = "✅ Low probability of AI-generated content"

        # -------------------------
        # ⚠️ SUSPICIOUS SENTENCES
        # -------------------------
        suspicious = [s for s in sentences if sentences.count(s) > 1]

        # -------------------------
        # 📊 OUTPUT
        # -------------------------
        st.subheader("📊 Results")

        col1, col2 = st.columns(2)
        col1.metric("Plagiarism %", f"{plagiarism_score}%")
        col2.metric("Originality %", f"{originality_score}%")

        # Progress bar (cool UI)
        st.progress(int(plagiarism_score))

        st.subheader("🤖 AI Detection")
        st.write(ai_result)

        st.subheader("⚠️ Suspicious Sentences")
        if suspicious:
            for s in set(suspicious):
                st.error(s)
        else:
            st.success("No major repetition detected")

        # Show extracted text (optional for demo)
        with st.expander("📄 View Processed Text"):
            st.write(text)

    else:
        st.warning("Please enter or upload text")