import streamlit as st
from openai import OpenAI

# Load API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Code Review Assistant", layout="centered")

st.title("🤖 Code Review Assistant")
st.write("Get quick AI feedback on your code before submitting for review.")

# Input box
code = st.text_area("Paste your code here", height=250)

# Language selector (nice upgrade)
language = st.selectbox(
    "Select Language",
    ["Java", "Python", "JavaScript", "SQL", "Other"]
)

if st.button("Review Code"):
    if not code.strip():
        st.warning("Please enter some code.")
    else:
        prompt = f"""
You are a senior software engineer reviewing a short code snippet.

Analyze the following {language} code for:
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

Keep feedback concise and practical.

Code:
{code}
"""

        try:
            with st.spinner("Analyzing..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

            result = response.choices[0].message.content

            st.success("Done!")
            st.markdown(result)

        except Exception as e:
            st.error("Something went wrong while analyzing the code.")
            st.exception(e)