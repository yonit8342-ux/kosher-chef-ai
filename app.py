import streamlit as st
import requests

st.set_page_config(page_title="שף כשר AI - בדיקת עומסים", page_icon="🍲")

# עיצוב RTL
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף כשר - סורק מודלים פנויים")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים...")

# רשימת מודלים פוטנציאליים לניסיון (לפי הרשימה שלך)
MODELS_TO_TRY = [
    "gemini-2.0-flash-lite", 
    "gemini-1.5-flash-latest",
    "gemini-2.0-flash",
    "gemini-pro-latest"
]

def call_model(model_name, key, text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": f"כתוב מתכון כשר וטעים בעברית עבור: {text}"}]}]}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response
    except:
        return None

if st.button("נסה למצוא מודל פנוי ולייצר מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        success = False
        with st.status("מחפש מודל פנוי...") as status:
            for model in MODELS_TO_TRY:
                status.write(f"בודק את מודל {model}...")
                resp = call_model(model, api_key, ingredients)
                
                if resp and resp.status_code == 200:
                    data = resp.json()
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    status.update(label="נמצא מודל פנוי!", state="complete")
                    st.success(f"המתכון נוצר בהצלחה באמצעות {model}:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
                    success = True
                    break
                elif resp and resp.status_code == 429:
                    status.write(f"❌ מודל {model} עמוס כרגע.")
                else:
                    status.write(f"❓ שגיאה אחרת במודל {model}.")
            
            if not success:
                status.update(label="כל המודלים עמוסים כרגע", state="error")
                st.error("לצערי כל המודלים בגרסה החינמית עמוסים כרגע. נסה שוב בעוד 2-3 דקות.")
    else:
        st.warning("הכנס מצרכים קודם.")
