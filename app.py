import streamlit as st
import requests

# הגדרות דף ועיצוב RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# משיכת המפתח
api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, תפוחי אדמה...")

if st.button("צור מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('השף מגבש מתכון...'):
            # התיקון: שימוש ב-v1beta ובנתיב המלא
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right;">{recipe}</div>', unsafe_allow_html=True)
                else:
                    # מציג את השגיאה המדויקת מהשרת
                    st.error(f"שגיאת API: {data.get('error', {}).get('message', 'Unknown Error')}")
            except Exception as e:
                st.error("חלה שגיאה בחיבור.")
    else:
        st.warning("הכנס מצרכים קודם.")
