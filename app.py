import streamlit as st
import google.generativeai as genai

# הגדרות דף ועיצוב RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL;
        text-align: right;
    }
    input {
        direction: RTL !important;
        text-align: right !important;
    }
    div.stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# משיכת מפתח ה-API מה-Secrets
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    # הגדרת ה-SDK עם המפתח שלך
    genai.configure(api_key=api_key)
    # שימוש במודל יציב עם תמיכה רחבה
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🍲 שף כשר - גרסה יציבה")
ingredients = st.text_input("מה נבשל היום?", placeholder="הכנס מצרכים כאן...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API בהגדרות ה-Secrets!")
    elif ingredients:
        try:
            with st.spinner('מתחבר לשרת גוגל...'):
                # פנייה למודל
                response = model.generate_content(f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור המצרכים הבאים: {ingredients}")
                st.success("הצלחנו!")
                st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">{response.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            # טיפול בשגיאת המכסה שראינו בצילומי המסך
            if "429" in str(e):
                st.error("הגענו למכסה המקסימלית. גוגל מגבילה את המודל בגרסה החינמית. נסה שוב בעוד דקה.")
            else:
                st.error(f"חלה שגיאה: {e}")
    else:
        st.warning("נא להזין מצרכים קודם.")
