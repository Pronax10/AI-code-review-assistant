import streamlit as st
from google import genai

# Initialize Gemini client
client = genai.Client()

st.set_page_config(page_title="AI Code Review Assistant", layout="centered")
st.title("🤖 Code Review Assistant (Gemini)")
st.write("Get quick AI feedback on your code before submitting for review.")

code = st.text_area("Paste your code here", height=250)

language = st.selectbox("Select Language", ["Java", "Python", "JavaScript", "SQL", "Other"])

if st.button("Review Code"):
    if not code.strip():
        st.warning("Please enter some code.")
    else:
        prompt = f"""
You are a senior software engineer reviewing a short code snippet in {language}.

Analyze the code for:
1. Readability
2. Structure
3. Maintainability

Output:
- 1 positive note
- 3 improvements
- optional refactor suggestions

Code:
{code}
"""

        try:
            with st.spinner("Analyzing..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            result = response.text

            st.success("Done!")
            st.markdown(result)

        except Exception as e:
            st.error("There was an issue with the Gemini API.")
            st.exception(e)