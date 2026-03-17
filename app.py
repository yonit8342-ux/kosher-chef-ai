import streamlit as st
import requests
import time

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# עיצוב RTL
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף כשר - פתרון סופי לעומס")
ingredients = st.text_input("מה נבשל היום?", placeholder="הכנס מצרכים...")

def call_gemini_with_retry(ingredients, key):
    # ננסה קודם את המודל הכי קל (8b) - הוא הכי פחות עמוס
    models = ["gemini-1.5-flash-8b", "gemini-1.5-flash-latest"]
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json(), model
            elif response.status_code == 429:
                continue # עובר למודל הבא אם זה עמוס
        except:
            continue
    return None, None

if st.button("צור מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('מתחבר לשרת...'):
            data, used_model = call_gemini_with_retry(ingredients, api_key)
            
            if data:
                recipe = data['candidates'][0]['content']['parts'][0]['text']
                st.success(f"הצלחנו! (באמצעות {used_model})")
                st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
            else:
                st.error("השרת עדיין חוסם אותנו. בבקשה חכה 5 דקות שלמות בלי ללחוץ על כלום ונסה שוב.")
    else:
        st.warning("הכנס מצרכים קודם.")
