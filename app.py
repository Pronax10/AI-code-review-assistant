import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Code Review Assistant", layout="centered")

st.title("🤖 Code Review Assistant")
st.write("Get quick AI feedback on your code before submitting for review.")

code = st.text_area("Paste your code here", height=250)

if st.button("Review Code"):
    if not code.strip():
        st.warning("Please enter some code.")
    else:
        prompt = f"""
        You are a senior software engineer reviewing a short code snippet.

        Analyze the code for:
        1. Readability
        2. Structure
        3. Maintainability

        Output format:

        ✅ Positive Note:
        - 1 good thing

        ⚠️ Improvements:
        1. ...
        2. ...
        3. ...

        💡 Suggested Fix (optional):

        Code:
        {code}
        """

        with st.spinner("Analyzing..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

        st.success("Done!")
        st.markdown(response['choices'][0]['message']['content'])