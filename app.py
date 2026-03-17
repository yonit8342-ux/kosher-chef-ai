import streamlit as st
import requests

# 1. עיצוב RTL (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף כשר - ניסיון אחרון וחסין")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים...")

if st.button("צור מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('השף בעבודה...'):
            # שימוש בכתובת הישירה עם המודל הכי יציב (gemini-1.5-flash)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"כתוב מתכון כשר וטעים בעברית עבור המצרכים: {ingredients}"}]}]}
            
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right;">{recipe}</div>', unsafe_allow_html=True)
                elif response.status_code == 429:
                    st.error("הגענו למכסה היומית. גוגל מגבילה את המפתח בחינם, כדאי לחכות כמה דקות.")
                else:
                    st.error(f"שגיאה מהשרת: {response.status_code}")
            except Exception as e:
                st.error(f"חלה שגיאה בחיבור: {e}")
