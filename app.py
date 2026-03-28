import streamlit as st
import os
from google.ai import generativeai

# Load your API key from Streamlit secrets or environment
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API key not configured.")
    st.stop()

generativeai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI Code Review Assistant (Gemini)", layout="centered")
st.title("🤖 Code Review Assistant (Google Gemini)")
st.write("Get quick AI feedback on your code before submitting for review.")

code = st.text_area("Paste your code here", height=250)
language = st.selectbox("Select Language", ["Java", "Python", "JavaScript", "SQL", "Other"])

if st.button("Review Code"):
    if not code.strip():
        st.warning("Please enter some code.")
    else:
        prompt = f"""
You are a senior software engineer reviewing a short {language} code snippet.

Analyze the code for:
1. Readability
2. Structure
3. Maintainability

Output:
- 1 positive comment
- 3 specific improvements
- optional refactor suggestion

Code:
{code}
"""

        try:
            with st.spinner("Analyzing with Gemini..."):
                response = generativeai.generate_text(
                    model="gemini-prototype-1.0",  # example model name
                    prompt=prompt,
                    max_output_tokens=512
                )

            st.success("Done!")
            st.markdown(response.text)

        except Exception as e:
            st.error("Error using Gemini API")
            st.exception(e)