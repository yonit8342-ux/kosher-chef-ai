import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>.main { direction: RTL; text-align: right; }</style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # המודל הכי יציב

st.title("🍲 שף כשר - ניסיון עם מפתח חדש")
ingredients = st.text_input("מה המצרכים?")

if st.button("בשל לי מתכון"):
    try:
        with st.spinner('מנסה את המפתח החדש...'):
            response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
            st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"שגיאה: {e}")
