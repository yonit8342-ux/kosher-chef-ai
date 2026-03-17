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

st.title("🍲 שף כשר - פתרון עומסים")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים...")

# רשימת מודלים - שמנו את ה-8b (הקל ביותר) בראש
MODELS = ["gemini-1.5-flash-8b", "gemini-1.5-flash-latest", "gemini-2.0-flash-lite"]

if st.button("נסה לייצר מתכון"):
    if not api_key:
        st.error("חסר מפתח API!")
    elif ingredients:
        success = False
        for model in MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]}
            
            with st.spinner(f"מנסה מודל {model}..."):
                try:
                    response = requests.post(url, json=payload, timeout=10)
                    if response.status_code == 200:
                        recipe = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"הצלחנו! (באמצעות {model})")
                        st.markdown(f'<div style="direction: RTL; text-align: right;">{recipe}</div>', unsafe_allow_html=True)
                        success = True
                        break
                    elif response.status_code == 429:
                        st.warning(f"מודל {model} עמוס.")
                        time.sleep(1) # המתנה קצרה בין ניסיונות
                except:
                    continue
        
        if not success:
            st.error("כל המודלים עמוסים. בבקשה חכה 5 דקות בלי ללחוץ ונסה שוב.")
    else:
        st.warning("הכנס מצרכים קודם.")
