import streamlit as st
import requests

# עיצוב ממשק RTL (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
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
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# משיכת המפתח מה-Secrets
api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף כשר AI")
st.write("הזינו מצרכים לקבלת מתכון כשר ומהיר:")

ingredients = st.text_input("מה נבשל?", placeholder="למשל: עוף, אורז, בצל...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('השף בעבודה...'):
            # הכתובת היציבה ביותר של גוגל למניעת שגיאות 404
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": f"אתה שף כשר מומחה. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון שמצאתי:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f1f3f4; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
                elif response.status_code == 429:
                    st.error("הגענו למכסה היומית (Quota Exceeded). נסה שוב בעוד דקה או החלף מפתח.")
                else:
                    st.error(f"שגיאה מהשרת ({response.status_code}). וודא שהמפתח תקין.")
            except Exception as e:
                st.error(f"חלה שגיאה בחיבור: {e}")
