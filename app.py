import streamlit as st
import os
import google.generativeai as genai

# Load your API key from Streamlit secrets or environment
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API key not configured. Please add it to your environment variables or Streamlit secrets.")
    st.stop()

# Configure the SDK with the modern API
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI Code Review Assistant", layout="centered")
st.title("🤖 Code Review Assistant (Gemini 1.5 Flash)")
st.write("Get quick AI feedback on your code before submitting for review.")

code = st.text_area("Paste your code here", height=250)
language = st.selectbox("Select Language", ["Python", "Java", "JavaScript", "SQL", "C++", "Other"])

if st.button("Review Code"):
    if not code.strip():
        st.warning("Please enter some code.")
    else:
        # Construct the prompt
        prompt = f"""
        You are a senior software engineer reviewing a short {language} code snippet.

        Analyze the code for:
        1. Readability
        2. Structure
        3. Maintainability

        Output:
        - 1 positive comment
        - 3 specific improvements
        - A concise refactor suggestion

        Code:
        {code}
        """

        try:
            with st.spinner("Analyzing with Gemini 1.5 Flash..."):
                # Initialize the model
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # Generate content
                response = model.generate_content(prompt)

            st.success("Analysis Complete!")
            # Use .text to get the string content from the response object
            st.markdown(response.text)

        except Exception as e:
            st.error("Error communicating with the Gemini API.")
            st.exception(e)