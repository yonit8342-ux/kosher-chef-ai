import streamlit as st
import requests

# הגדרות RTL (הצמדה לימין)
st.set_page_config(page_title="בדיקת מערכת AI", page_icon="🔍")
st.markdown("""<style> .main {direction: RTL; text-align: right;} </style>""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_KEY")

st.title("🔍 אבחון מודל ו-API")

if st.button("הרץ בדיקת תקשורת"):
    if not api_key:
        st.error("המפתח (API Key) לא מוגדר ב-Secrets!")
    else:
        # שימוש במודל ובנתיב הכי יציבים למניעת 404
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": "תגיד שלום"}]}]}
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("✅ המודל עובד! ה-API והספריה תקינים.")
                st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
            elif response.status_code == 404:
                st.error("❌ שגיאת 404: המודל לא נמצא בכתובת זו.")
            elif response.status_code == 429:
                st.error("❌ שגיאת 429: המפתח תקין אך המכסה נגמרה.")
            else:
                st.error(f"❌ שגיאה {response.status_code}: בעיה במפתח ה-API.")
        except Exception as e:
            st.error(f"❌ תקלה טכנית: {e}")
