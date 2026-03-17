import streamlit as st
import requests

# הגדרות דף ועיצוב RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
</style>""", unsafe_allow_html=True)

# משיכת המפתח מה-Secrets
api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו מצרכים וקבלו מתכון כשר מהמודל החדש:")

ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, תפוחי אדמה, סילאן...")

if st.button("צור מתכון"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('השף (Gemini 2.0) מגבש מתכון...'):
            # שימוש במודל gemini-2.0-flash מתוך הרשימה שלך
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{"parts": [{"text": f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]
            }
            
            try:
                response = requests.post(url, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"שגיאה: {data.get('error', {}).get('message', 'Unknown Error')}")
            except Exception as e:
                st.error("חלה שגיאה בחיבור.")
    else:
        st.warning("הכנס מצרכים קודם.")
