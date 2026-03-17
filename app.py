import streamlit as st
import google.generativeai as genai

# הגדרות RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
</style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # השם 'gemini-1.5-flash-latest' הוא הכי יציב למניעת שגיאות 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("🍲 שף כשר - תיקון שגיאת מודל")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים...")

if st.button("צור מתכון"):
    if ingredients and api_key:
        try:
            with st.spinner('מתחבר למודל המעודכן...'):
                response = model.generate_content(f"כתוב מתכון כשר בעברית עבור: {ingredients}")
                st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"שגיאה: {e}")
