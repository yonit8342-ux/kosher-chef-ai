import streamlit as st
import requests

# 1. עיצוב RTL מלא (אנטילקס)
st.set_page_config(page_title="שף כשר AI - בודק מודלים", page_icon="🍲")
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3, div {
        direction: RTL;
        text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

# רשימת מודלים לניסיון כדי למנוע 404
MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.0-pro"
]

st.title("🍲 שף כשר - מעקף שגיאת 404")
ingredients = st.text_input("מה נבשל היום?", placeholder="הכנס מצרכים...")

if st.button("נסה ליצור מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        success = False
        with st.status("בודק מודלים פנויים...") as status:
            for model_name in MODELS:
                status.write(f"מנסה להתחבר למודל: {model_name}...")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        recipe = data['candidates'][0]['content']['parts'][0]['text']
                        status.update(label=f"הצלחה עם {model_name}!", state="complete")
                        st.success("הנה המתכון:")
                        st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
                        success = True
                        break
                    elif response.status_code == 404:
                        status.write(f"❌ מודל {model_name} לא נמצא (404). עובר לבא...")
                    elif response.status_code == 429:
                        status.write(f"⚠️ מודל {model_name} עמוס (429).")
                except Exception as e:
                    status.write(f"⚠️ שגיאה בחיבור ל-{model_name}.")
            
            if not success:
                status.update(label="כל הניסיונות נכשלו", state="error")
                st.error("לא נמצא מודל זמין. בדוק אם המפתח תקין או נסה שוב מאוחר יותר.")
    else:
        st.warning("נא להזין מצרכים.")
