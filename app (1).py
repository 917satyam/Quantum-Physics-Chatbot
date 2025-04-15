import streamlit as st
from helper import get_explanation
from fpdf import FPDF
from streamlit.components.v1 import html
import random
import re

# Clean text for PDF: Remove characters not in Latin-1
def clean_text_for_pdf(text):
    return re.sub(r'[^\x00-\xFF]', '', text)

# --- Page Configuration ---
st.set_page_config(page_title="Quantum Physics AI Explainer", layout="wide")

# --- Light/Dark Mode Toggle ---
theme = st.toggle("🌓 Toggle Light/Dark Mode")

# Apply theme CSS
if theme:
    st.markdown("""<style>.stApp { background-color: black; color: white; }</style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>.stApp { background-color: white; color: black; }</style>""", unsafe_allow_html=True)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        h1 { font-size: 36px; text-align: center; margin-bottom: 10px; }
        .objectives { text-align: center; font-size: 20px; font-weight: bold; }
        h2 { text-align: center; margin-top: 30px; }
        .stButton > button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white; font-weight: bold; border: none;
            border-radius: 10px; padding: 12px; width: 100%;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #005bea, #00c6ff);
            transform: scale(1.05);
        }
        .stTextInput > div {
            border-radius: 8px; border: 2px solid white;
            background: rgba(255, 255, 255, 0.1); color: white;
        }
        .card {
            background: rgba(255,255,255,0.05);
            border-left: 5px solid #00ffff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 18px;
        }
        .centered-block {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 30px;
        }
        .topic-label {
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            margin-bottom: 0px;
        }
        .custom-text-input textarea {
            height: 100px !important;
            font-size: 16px !important;
        }
        .custom-text-input {
            width: 75% !important;
            margin: 0 auto;
            margin-top: 1px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("🧠 About This App")
    st.markdown("An AI-powered tool to **simplify complex quantum physics** concepts.")
    st.markdown("---")
    st.markdown("📚 **Most frequently asked topics:**")
    st.markdown("- Quantum Entanglement")
    st.markdown("- Superposition")
    st.markdown("- Schrödinger's Cat")
    st.markdown("- Heisenberg Principle")
    st.markdown("---")
    st.markdown("🎯 **Goal**: Learn quantum physics the smart way!")
    st.markdown("---")
    st.markdown("💬 **Quantum Quote**")
    st.markdown("> *“If you think you understand quantum mechanics, you don’t understand quantum mechanics.”*<br>— Richard Feynman", unsafe_allow_html=True)
    st.markdown("---")
    fun_facts = [
        "Quantum teleportation has been demonstrated with photons!",
        "Heisenberg’s uncertainty principle sets a limit to precision.",
        "Schrödinger’s cat is both alive and dead until observed!",
        "Qubits can exist in superposition — unlike classical bits.",
        "Quantum entanglement links particles across space instantly!"
    ]
    st.markdown("💡 **Did You Know?**")
    st.info(random.choice(fun_facts))
    st.markdown("---")
    st.write("👨‍💻 Created by: `GROUP A2`")
    st.markdown(" [📧 Email](mailto:your@email.com)")

# --- Main Container ---
with st.container():
    st.markdown("<h1>⚛️ AI-Based Quantum Physics Explainer</h1>", unsafe_allow_html=True)

    def render_lottie_html(lottie_url, dark_mode):
        bg_color = "#000000" if dark_mode else "#ffffff"
        html_str = f"""
        <div style='display: flex; justify-content: center;'>
            <lottie-player
                src="{lottie_url}"
                background="{bg_color}"
                speed="1"
                style="width: 300px; height: 300px;"
                loop autoplay>
            </lottie-player>
        </div>
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        """
        html(html_str, height=320)

    lottie_url = "https://lottie.host/fb83bd5e-6541-496c-be87-db0aa9094809/adXr4pTq0S.json"
    render_lottie_html(lottie_url, theme)

    st.markdown("<h2>🌟 Objectives</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class='objectives'>
            <p>🔹 Simplify complex quantum physics concepts using AI.</p>
            <p>🔹 Provide accurate, easy-to-understand explanations for students and researchers.</p>
            <p>🔹 Offer interactive learning through AI-generated content.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='centered-block'>
            <div class='topic-label'>🔍 <b>Enter a Quantum Physics Topic</b> (e.g., Quantum Entanglement):</div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-text-input">', unsafe_allow_html=True)
        topic = st.text_area("", height=100, key="topic_input")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Explain with AI"):
        if topic.strip():
            with st.spinner("Fetching simplified explanation..."):
                prompt = f"Simplify this quantum physics concept in easy terms: {topic}."
                explanation_text = get_explanation(prompt)

                st.success("✅ Here's the explanation:")
                st.markdown(f"<div class='card'>{explanation_text}</div>", unsafe_allow_html=True)

                # Clean and export to PDF
                explanation_text_clean = clean_text_for_pdf(explanation_text)
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, explanation_text_clean)

                pdf_file_path = "explanation.pdf"
                pdf.output(pdf_file_path)

                with open(pdf_file_path, "rb") as f:
                    st.download_button("📄 Download Explanation as PDF", f, file_name="explanation.pdf")

    # Predefined Topics
    st.subheader("📌 Explore Quantum Topics")
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    quantum_topics = [
        "Quantum Entanglement", "Schrödinger's Cat", "Quantum Superposition",
        "Heisenberg Uncertainty Principle", "Quantum Tunneling", "Wave-Particle Duality"
    ]

    cols = st.columns(len(quantum_topics))
    for i, quantum_topic in enumerate(quantum_topics):
        with cols[i]:
            if st.button(quantum_topic):
                with st.spinner(f"🔍 Fetching details on {quantum_topic}..."):
                    explanation = get_explanation(quantum_topic)
                    st.success(f"✨ {quantum_topic}")
                    st.markdown(f"<div class='card'>{explanation}</div>", unsafe_allow_html=True)
