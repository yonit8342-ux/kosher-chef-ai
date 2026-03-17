import streamlit as st
import requests

# 1. הגדרות דף ועיצוב
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
</style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: בשר, תפוחי אדמה, בצל...")

def call_gemini(model_name, api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    return requests.post(url, json=payload)

if st.button("צור מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('השף בודק מכסות ומכין מתכון...'):
            prompt = f"אתה שף מומחה לכשרות. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"
            
            # ניסיון ראשון: המודל הקל (Lite) - לרוב המכסה שלו פנויה
            response = call_gemini("gemini-2.0-flash-lite", api_key, prompt)
            
            # אם המכסה נגמרה (429), ננסה את המודל השני
            if response.status_code == 429:
                st.info("מודל ראשון עמוס, מנסה מודל גיבוי...")
                response = call_gemini("gemini-1.5-flash-latest", api_key, prompt)
            
            if response.status_code == 200:
                data = response.json()
                recipe = data['candidates'][0]['content']['parts'][0]['text']
                st.success("הנה המתכון:")
                st.markdown(f'<div style="direction: RTL; text-align: right;">{recipe}</div>', unsafe_allow_html=True)
            else:
                st.error(f"כל המודלים עמוסים כרגע. נסה שוב בעוד דקה.")
    else:
        st.warning("הכנס מצרכים קודם.")
